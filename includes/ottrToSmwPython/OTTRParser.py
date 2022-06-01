from antlr4 import ParserRuleContext, NoViableAltException, RecognitionException

from includes.ottrToSmwPython.stOTTR.stOTTRParser import stOTTRParser


class OTTRParser(stOTTRParser):

    class ConstantContext(stOTTRParser.ConstantContext):
        def __init__(self, parser, parent: ParserRuleContext = None, invokingState: int = -1):
            super().__init__(parser, parent, invokingState)
            self.inner_constant_ref = None

    class TermContext(stOTTRParser.TermContext):
        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parser, parent, invokingState)
            self.term = None
            self.inner_constant = None

    def constant(self):
        localctx = OTTRParser.ConstantContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_constant)
        try:
            self.state = 214
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [stOTTRParser.IRIREF, stOTTRParser.PNAME_NS, stOTTRParser.PNAME_LN]:
                self.enterOuterAlt(localctx, 1)
                self.state = 209
                self.iri()
                pass
            elif token in [stOTTRParser.T__1, stOTTRParser.BLANK_NODE_LABEL]:
                self.enterOuterAlt(localctx, 2)
                self.state = 210
                self.blankNode()
                pass
            elif token in [stOTTRParser.BooleanLiteral, stOTTRParser.String, stOTTRParser.INTEGER, stOTTRParser.DECIMAL, stOTTRParser.DOUBLE]:
                self.enterOuterAlt(localctx, 3)
                self.state = 211
                self.literal()
                pass
            elif token in [stOTTRParser.T__17]:
                self.enterOuterAlt(localctx, 4)
                self.state = 212
                self.none()
                pass
            elif token in [stOTTRParser.T__11]:
                self.enterOuterAlt(localctx, 5)
                self.state = 213
                self.constantList()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx

    def term(self):
        localctx = OTTRParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_term)
        try:
            self.state = 207
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,17,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 204
                self.match(stOTTRParser.Variable)
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 205
                self.constant()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 206
                self.termList()
                pass

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx
