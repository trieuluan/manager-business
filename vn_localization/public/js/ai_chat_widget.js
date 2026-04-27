(function () {
	if (window.vnLocalizationAiChatLoaded) {
		return;
	}
	window.vnLocalizationAiChatLoaded = true;

	const METHOD = "vn_localization.ai.chat.send_message";
	const STORAGE_KEY = "vn_localization_ai_chat_history";
	const MAX_HISTORY_ITEMS = 12;

	function boot() {
		if (!window.frappe || !frappe.session || frappe.session.user === "Guest") {
			return;
		}
		if (document.getElementById("vn-ai-chat-root")) {
			return;
		}

		injectStyles();

		const root = document.createElement("div");
		root.id = "vn-ai-chat-root";
		root.innerHTML = `
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
		renderMessages(messagesEl, history, true);
		setLoading(sendButton, true);

		const apiHistory = history
			.filter((item) => item.role === "user" || item.role === "assistant")
			.slice(-8);

		frappe.call({
			method: METHOD,
			args: {
				message: content,
				history: JSON.stringify(apiHistory),
			},
			callback(response) {
				const data = response.message || {};
				history.push({
					role: "assistant",
					content: data.message || "Mình chưa nhận được phản hồi phù hợp.",
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
				setLoading(sendButton, false);
				input.focus();
			},
		});
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

	function injectStyles() {
		if (document.getElementById("vn-ai-chat-styles")) {
			return;
		}

		const style = document.createElement("style");
		style.id = "vn-ai-chat-styles";
		style.textContent = `
			#vn-ai-chat-root {
				position: fixed;
				right: 20px;
				bottom: 20px;
				z-index: 1050;
				font-family: Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
			}

			.vn-ai-chat-toggle {
				width: 52px;
				height: 52px;
				border: 0;
				border-radius: 50%;
				background: #14532d;
				color: #fff;
				box-shadow: 0 12px 32px rgba(15, 23, 42, 0.22);
				font-weight: 700;
				cursor: pointer;
			}

			.vn-ai-chat-panel {
				position: absolute;
				right: 0;
				bottom: 64px;
				width: min(380px, calc(100vw - 32px));
				height: min(560px, calc(100vh - 120px));
				background: #fff;
				border: 1px solid #d9e2dc;
				border-radius: 8px;
				box-shadow: 0 18px 48px rgba(15, 23, 42, 0.22);
				overflow: hidden;
				display: flex;
				flex-direction: column;
			}

			.vn-ai-chat-panel[hidden] {
				display: none;
			}

			.vn-ai-chat-header {
				display: flex;
				align-items: center;
				justify-content: space-between;
				padding: 12px 14px;
				border-bottom: 1px solid #e5e7eb;
				background: #f8fafc;
			}

			.vn-ai-chat-header strong,
			.vn-ai-chat-header span {
				display: block;
			}

			.vn-ai-chat-header span {
				color: #64748b;
				font-size: 12px;
				margin-top: 2px;
			}

			.vn-ai-chat-close {
				width: 28px;
				height: 28px;
				border: 0;
				background: transparent;
				color: #475569;
				font-size: 22px;
				line-height: 1;
				cursor: pointer;
			}

			.vn-ai-chat-messages {
				flex: 1;
				overflow-y: auto;
				padding: 14px;
				background: #f8fafc;
			}

			.vn-ai-message {
				width: fit-content;
				max-width: 88%;
				white-space: pre-wrap;
				overflow-wrap: anywhere;
				border-radius: 8px;
				padding: 9px 11px;
				margin-bottom: 10px;
				line-height: 1.45;
				font-size: 13px;
			}

			.vn-ai-message-user {
				margin-left: auto;
				background: #166534;
				color: #fff;
			}

			.vn-ai-message-assistant {
				margin-right: auto;
				background: #fff;
				color: #0f172a;
				border: 1px solid #e5e7eb;
			}

			.vn-ai-message-loading {
				display: flex;
				align-items: center;
				gap: 5px;
				color: #64748b;
			}

			.vn-ai-loading-dot {
				width: 6px;
				height: 6px;
				border-radius: 50%;
				background: #94a3b8;
				animation: vn-ai-loading-pulse 1.2s ease-in-out infinite;
			}

			.vn-ai-loading-dot:nth-child(2) {
				animation-delay: 0.15s;
			}

			.vn-ai-loading-dot:nth-child(3) {
				animation-delay: 0.3s;
			}

			.vn-ai-loading-text {
				margin-left: 4px;
				font-size: 12px;
			}

			@keyframes vn-ai-loading-pulse {
				0%, 80%, 100% {
					opacity: 0.35;
					transform: translateY(0);
				}
				40% {
					opacity: 1;
					transform: translateY(-3px);
				}
			}

			.vn-ai-chat-form {
				display: flex;
				gap: 8px;
				padding: 10px;
				border-top: 1px solid #e5e7eb;
				background: #fff;
			}

			.vn-ai-chat-input {
				flex: 1;
				min-height: 40px;
				max-height: 96px;
				resize: vertical;
				border: 1px solid #cbd5e1;
				border-radius: 8px;
				padding: 8px 10px;
				font-size: 13px;
				line-height: 1.35;
			}

			.vn-ai-chat-send {
				width: 56px;
				height: 40px;
				border: 0;
				border-radius: 8px;
				background: #14532d;
				color: #fff;
				font-weight: 600;
				cursor: pointer;
			}

			.vn-ai-chat-send:disabled {
				opacity: 0.65;
				cursor: wait;
			}
		`;
		document.head.appendChild(style);
	}

	if (document.readyState === "loading") {
		document.addEventListener("DOMContentLoaded", boot);
	} else {
		boot();
	}
})();
