import sys
import traceback

from antlr4.error.ErrorStrategy import BailErrorStrategy, DefaultErrorStrategy
from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker, RecognitionException, Parser
from antlr4.error.Errors import InputMismatchException, ParseCancellationException

from OTTRParser import OTTRParser
from OTTRToSMWConverter import OTTRToSMWConverter
from NoGenerationErrorStrategy import NoGenerationErrorStrategy
from stOTTR.stOTTRLexer import stOTTRLexer

try:
	def main(argv):
		# input_stream = FileStream("test_examples/ottr_test_strings.txt")
		# input_stream = FileStream("test_examples/all_test_examples")
		input_stream = FileStream("test_examples/anno_test")
		# input_stream = FileStream("test_examples/form_test")
		lexer = stOTTRLexer(input_stream)
		stream = CommonTokenStream(lexer)
		parser = OTTRParser(stream)
		parser._errHandler = NoGenerationErrorStrategy()
		tree = parser.stOTTRDoc()
		printer = OTTRToSMWConverter()
		walker = ParseTreeWalker()
		walker.walk(printer, tree)


	if __name__ == '__main__':
		main(sys.argv)

except KeyError as e:
	print("{{ottr:ErrorMsg|The string '''%s''' is not one of the defined arguments in the signature|code=-3}" % e.args[0])
except RecognitionException as e:
	print("{{ottr:ErrorMsg|Parser Error, see above|code=0}}")
except Exception as e:
	traceback.print_exc()
