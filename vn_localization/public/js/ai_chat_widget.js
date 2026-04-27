(function () {
	if (window.vnLocalizationAiChatLoaded) {
		return;
	}
	window.vnLocalizationAiChatLoaded = true;

	const METHOD = "vn_localization.ai.chat.send_message";
	const STREAM_METHOD = "vn_localization.ai.chat.stream_message";
	const STORAGE_KEY = "vn_localization_ai_chat_history";
	const MAX_HISTORY_ITEMS = 12;
	const WIDGET_VERSION = "20260428-translations";

	console.info("VN AI chat widget loaded", WIDGET_VERSION);

	function boot() {
		if (!window.frappe || !frappe.session || frappe.session.user === "Guest") {
			return;
		}
		if (document.getElementById("vn-ai-chat-root")) {
			return;
		}

		const root = document.createElement("div");
		root.id = "vn-ai-chat-root";
		root.innerHTML = getWidgetTemplate();
		document.body.appendChild(root);

		const toggle = root.querySelector(".vn-ai-chat-toggle");
		const panel = root.querySelector(".vn-ai-chat-panel");
		const close = root.querySelector(".vn-ai-chat-close");
		const form = root.querySelector(".vn-ai-chat-form");
		const input = root.querySelector(".vn-ai-chat-input");
		const messagesEl = root.querySelector(".vn-ai-chat-messages");
		const sendButton = root.querySelector(".vn-ai-chat-send");
		const history = loadHistory();

		if (!history.length) {
			history.push({
				role: "assistant",
				content: "Chào bạn, mình có thể hướng dẫn nhanh cách dùng ERPNext bằng tiếng Việt.",
			});
		}
		renderMessages(messagesEl, history);

		toggle.addEventListener("click", function () {
			panel.hidden = !panel.hidden;
			if (!panel.hidden) {
				input.focus();
				scrollToBottom(messagesEl);
			}
		});

		close.addEventListener("click", function () {
			panel.hidden = true;
		});

		input.addEventListener("keydown", function (event) {
			if (event.key === "Enter" && !event.shiftKey) {
				event.preventDefault();
				form.requestSubmit();
			}
		});

		form.addEventListener("submit", function (event) {
			event.preventDefault();
			const content = input.value.trim();
			if (!content || sendButton.disabled) {
				return;
			}
			input.value = "";
			sendMessage({ content, history, messagesEl, sendButton, input });
		});
	}

	function sendMessage({ content, history, messagesEl, sendButton, input }) {
		history.push({ role: "user", content });
		renderMessages(messagesEl, history);
		setLoading(sendButton, true);

		const apiHistory = history
			.filter((item) => item.role === "user" || item.role === "assistant")
			.slice(-8);
		const pageContext = getPageContext();

		if (window.fetch && window.ReadableStream) {
			streamMessage({ content, history, apiHistory, messagesEl, pageContext })
				.catch(function (error) {
					console.warn("VN AI chat stream failed, falling back to RPC.", error);
					return sendMessageFallback({ content, history, apiHistory, messagesEl, pageContext });
				})
				.finally(function () {
					setLoading(sendButton, false);
					input.focus();
				});
			return;
		}

		sendMessageFallback({ content, history, apiHistory, messagesEl, pageContext }).finally(function () {
			setLoading(sendButton, false);
			input.focus();
		});
	}

	async function streamMessage({ content, history, apiHistory, messagesEl, pageContext }) {
		const assistantMessage = createWaitingMessage();
		messagesEl.appendChild(assistantMessage);
		scrollToBottom(messagesEl);

		const formData = new URLSearchParams();
		formData.set("message", content);
		formData.set("history", JSON.stringify(apiHistory));
		appendPageContext(formData, pageContext);

		const response = await fetch(`/api/method/${STREAM_METHOD}`, {
			method: "POST",
			body: formData.toString(),
			credentials: "same-origin",
			headers: {
				"Accept": "text/event-stream",
				"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
				"X-Frappe-CSRF-Token": frappe.csrf_token || "",
			},
		});

		if (!response.ok || !response.body) {
			throw new Error("Streaming response is unavailable");
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder();
		let buffer = "";
		let assistantContent = "";

		while (true) {
			const { value, done } = await reader.read();
			if (done) {
				break;
			}

			buffer += decoder.decode(value, { stream: true });
			const parts = buffer.split("\n\n");
			buffer = parts.pop() || "";

			for (const part of parts) {
				const event = parseSseEvent(part);
				if (!event) {
					continue;
				}

				if (event.event === "token" && event.data.content) {
					assistantContent += event.data.content;
					updateStreamingMessage(assistantMessage, sanitizeAssistantText(assistantContent));
				}

				if (event.event === "error") {
					throw new Error(event.data.message || "AI stream failed");
				}
			}
		}

		if (!assistantContent.trim()) {
			throw new Error("AI stream returned no content");
		}

		history.push({ role: "assistant", content: sanitizeAssistantText(assistantContent).trim() });
		trimHistory(history);
		saveHistory(history);
		renderMessages(messagesEl, history);
	}

	function sendMessageFallback({ content, history, apiHistory, messagesEl, pageContext }) {
		renderMessages(messagesEl, history, true);

		return new Promise(function (resolve) {
			const args = {
				message: content,
				history: JSON.stringify(apiHistory),
			};
			Object.assign(args, pageContext);

			frappe.call({
				method: METHOD,
				args,
				callback(response) {
					const data = response.message || {};
					history.push({
						role: "assistant",
						content: sanitizeAssistantText(data.message || "Mình chưa nhận được phản hồi phù hợp."),
					});
					trimHistory(history);
					saveHistory(history);
					renderMessages(messagesEl, history);
				},
				error() {
					history.push({
						role: "assistant",
						content: "Mình chưa kết nối được AI local. Bạn kiểm tra Ollama và model đang chạy nhé.",
					});
					renderMessages(messagesEl, history);
				},
				always() {
					resolve();
				},
			});
		});
	}

	function getPageContext() {
		const route = frappe.get_route ? frappe.get_route() : [];
		const form = window.cur_frm;
		const context = {
			route: JSON.stringify(route || []),
		};

		if (form && form.doctype && form.docname && !form.is_new()) {
			context.doctype = form.doctype;
			context.docname = form.docname;
		}

		return context;
	}

	function appendPageContext(formData, pageContext) {
		Object.keys(pageContext || {}).forEach(function (key) {
			if (pageContext[key]) {
				formData.set(key, pageContext[key]);
			}
		});
	}

	function parseSseEvent(rawEvent) {
		const lines = rawEvent.split("\n");
		let eventName = "message";
		let data = "";

		lines.forEach(function (line) {
			if (line.startsWith("event:")) {
				eventName = line.slice(6).trim();
			}
			if (line.startsWith("data:")) {
				data += line.slice(5).trim();
			}
		});

		if (!data) {
			return null;
		}

		try {
			return {
				event: eventName,
				data: JSON.parse(data),
			};
		} catch (error) {
			return null;
		}
	}

	function getWidgetTemplate() {
		return `
			<button class="vn-ai-chat-toggle" type="button" aria-label="Mở trợ lý AI" title="Trợ lý AI">
				<span>AI</span>
			</button>
			<section class="vn-ai-chat-panel" aria-label="Trợ lý AI" hidden>
				<header class="vn-ai-chat-header">
					<div>
						<strong>Trợ lý AI</strong>
						<span>Hướng dẫn ERPNext</span>
					</div>
					<button class="vn-ai-chat-close" type="button" aria-label="Đóng">×</button>
				</header>
				<div class="vn-ai-chat-messages"></div>
				<form class="vn-ai-chat-form">
					<textarea class="vn-ai-chat-input" rows="2" placeholder="Hỏi cách dùng ERPNext..." maxlength="2000"></textarea>
					<button class="vn-ai-chat-send" type="submit">Gửi</button>
				</form>
			</section>
		`;
	}

	function updateStreamingMessage(message, content) {
		message.classList.remove("vn-ai-message-loading");
		message.textContent = content;
		scrollToBottom(message.parentElement);
	}

	function sanitizeAssistantText(text) {
		const replacements = {
			"menu\\s+Workspace\\s+Sidebar": "menu bên trái",
			"Workspace\\s+Sidebar": "menu bên trái",
			"Purchase\\s+Receipt": "Phiếu nhập kho",
			"Sales\\s+Invoice": "Hóa đơn bán hàng",
			"Purchase\\s+Invoice": "Hóa đơn mua hàng",
			"Stock\\s+Entry": "Phiếu nhập xuất kho",
			"Stock\\s+Reconciliation": "Kiểm kê kho",
			"Journal\\s+Entry": "Bút toán",
			"Payment\\s+Entry": "Phiếu thu chi",
			"Delivery\\s+Note": "Phiếu giao hàng",
			"Sales\\s+Order": "Đơn bán hàng",
			"Purchase\\s+Order": "Đơn đặt hàng",
		};
		let value = String(text || "");
		Object.keys(replacements).forEach(function (source) {
			value = value.replace(new RegExp(source, "gi"), replacements[source]);
		});
		return value;
	}

	function renderMessages(container, history, isWaiting) {
		container.innerHTML = "";
		history.forEach(function (item) {
			const message = document.createElement("div");
			message.className = `vn-ai-message vn-ai-message-${item.role}`;
			message.textContent = item.content;
			container.appendChild(message);
		});
		if (isWaiting) {
			container.appendChild(createWaitingMessage());
		}
		scrollToBottom(container);
	}

	function createWaitingMessage() {
		const message = document.createElement("div");
		message.className = "vn-ai-message vn-ai-message-assistant vn-ai-message-loading";
		message.setAttribute("aria-label", "AI đang chuẩn bị phản hồi");
		message.innerHTML = `
			<span class="vn-ai-loading-dot"></span>
			<span class="vn-ai-loading-dot"></span>
			<span class="vn-ai-loading-dot"></span>
			<span class="vn-ai-loading-text">Đang suy nghĩ</span>
		`;
		return message;
	}

	function setLoading(button, isLoading) {
		button.disabled = isLoading;
		button.textContent = isLoading ? "..." : "Gửi";
	}

	function trimHistory(history) {
		if (history.length > MAX_HISTORY_ITEMS) {
			history.splice(0, history.length - MAX_HISTORY_ITEMS);
		}
	}

	function loadHistory() {
		try {
			const value = window.localStorage.getItem(STORAGE_KEY);
			const parsed = value ? JSON.parse(value) : [];
			return Array.isArray(parsed) ? parsed : [];
		} catch (error) {
			return [];
		}
	}

	function saveHistory(history) {
		try {
			window.localStorage.setItem(STORAGE_KEY, JSON.stringify(history.slice(-MAX_HISTORY_ITEMS)));
		} catch (error) {
			// Storage can be unavailable in private browsing.
		}
	}

	function scrollToBottom(container) {
		requestAnimationFrame(function () {
			container.scrollTop = container.scrollHeight;
		});
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", boot);
	} else {
		boot();
	}
})();
