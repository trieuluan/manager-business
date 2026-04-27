"""Provider error types."""


class ProviderError(Exception):
	def __init__(self, message, retryable=True):
		super().__init__(message)
		self.retryable = retryable

