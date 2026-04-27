"""Provider error types."""


class ProviderError(Exception):
	def __init__(self, message, retryable=True, retry_after=None):
		super().__init__(message)
		self.retryable = retryable
		self.retry_after = retry_after  # seconds to wait before retrying

