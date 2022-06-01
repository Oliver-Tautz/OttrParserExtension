from antlr4 import Parser, RecognitionException
from antlr4.error.ErrorStrategy import DefaultErrorStrategy
from antlr4.error.Errors import InputMismatchException


# Other Variation of BailErrorStrategy
class NoGenerationErrorStrategy(DefaultErrorStrategy):
	# Instead of recovering from exception {@code e}, re-throw it wrapped
	#  in a {@link ParseCancellationException} so it is not caught by the
	#  rule function catches.  Use {@link Exception#getCause()} to get the
	#  original {@link RecognitionException}.
	#
	def recover(self, recognizer: Parser, e: RecognitionException):
		# printing the error
		super(NoGenerationErrorStrategy, self).recover(recognizer, e)
		raise e

	# Make sure we don't attempt to recover inline; if the parser
	#  successfully recovers, it won't throw an exception.
	#
	def recoverInline(self, recognizer: Parser):
		self.recover(recognizer, InputMismatchException(recognizer))

	# Make sure we don't attempt to recover from problems in subrules.#
	def sync(self, recognizer: Parser):
		pass