import sys
import traceback


from antlr4 import FileStream, CommonTokenStream, ParseTreeWalker, RecognitionException

from includes.ottrToSmwPython.OTTRParser import OTTRParser
from includes.ottrToSmwPython.OTTRToSMWConverter import OTTRToSMWConverter
from includes.ottrToSmwPython.NoGenerationErrorStrategy import NoGenerationErrorStrategy
from includes.ottrToSmwPython.stOTTR.stOTTRLexer import stOTTRLexer


def main(argv):
    #print(argv)
    
    try:
        if len(argv) < 2:
            print("<--No second argument for file name that contains ottr data-->")
        else:
            input_stream = FileStream(argv[1], encoding='utf-8')
            lexer = stOTTRLexer(input_stream)
            stream = CommonTokenStream(lexer)
            parser = OTTRParser(stream)
            parser._errHandler = NoGenerationErrorStrategy()
            tree = parser.stOTTRDoc()
            printer = OTTRToSMWConverter()
            walker = ParseTreeWalker()
            walker.walk(printer, tree)
    except KeyError as e:
        print("{{ottr:ErrorMsg|The string '''%s''' is not one of the defined arguments in the signature|code=-3}" % e.args[0])
    except RecognitionException as e:
        print("{{ottr:ErrorMsg|Parser Error, see above|code=0}}")
    except Exception as e:
        traceback.print_exc()   
def run():
    main(sys.argv)

if __name__ == '__main__':
    run()

