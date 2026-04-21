# Generated from Pseudocode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PseudocodeParser import PseudocodeParser
else:
    from PseudocodeParser import PseudocodeParser

# This class defines a complete listener for a parse tree produced by PseudocodeParser.
class PseudocodeListener(ParseTreeListener):

    # Enter a parse tree produced by PseudocodeParser#program.
    def enterProgram(self, ctx:PseudocodeParser.ProgramContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#program.
    def exitProgram(self, ctx:PseudocodeParser.ProgramContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#statement.
    def enterStatement(self, ctx:PseudocodeParser.StatementContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#statement.
    def exitStatement(self, ctx:PseudocodeParser.StatementContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#assignment.
    def enterAssignment(self, ctx:PseudocodeParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#assignment.
    def exitAssignment(self, ctx:PseudocodeParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#RangeArray.
    def enterRangeArray(self, ctx:PseudocodeParser.RangeArrayContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#RangeArray.
    def exitRangeArray(self, ctx:PseudocodeParser.RangeArrayContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#SizeArray.
    def enterSizeArray(self, ctx:PseudocodeParser.SizeArrayContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#SizeArray.
    def exitSizeArray(self, ctx:PseudocodeParser.SizeArrayContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#ValueArray.
    def enterValueArray(self, ctx:PseudocodeParser.ValueArrayContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#ValueArray.
    def exitValueArray(self, ctx:PseudocodeParser.ValueArrayContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#functionDecl.
    def enterFunctionDecl(self, ctx:PseudocodeParser.FunctionDeclContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#functionDecl.
    def exitFunctionDecl(self, ctx:PseudocodeParser.FunctionDeclContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#functionCallStatement.
    def enterFunctionCallStatement(self, ctx:PseudocodeParser.FunctionCallStatementContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#functionCallStatement.
    def exitFunctionCallStatement(self, ctx:PseudocodeParser.FunctionCallStatementContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#paramList.
    def enterParamList(self, ctx:PseudocodeParser.ParamListContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#paramList.
    def exitParamList(self, ctx:PseudocodeParser.ParamListContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#forEachLoop.
    def enterForEachLoop(self, ctx:PseudocodeParser.ForEachLoopContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#forEachLoop.
    def exitForEachLoop(self, ctx:PseudocodeParser.ForEachLoopContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#regularForLoop.
    def enterRegularForLoop(self, ctx:PseudocodeParser.RegularForLoopContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#regularForLoop.
    def exitRegularForLoop(self, ctx:PseudocodeParser.RegularForLoopContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#forUpdate.
    def enterForUpdate(self, ctx:PseudocodeParser.ForUpdateContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#forUpdate.
    def exitForUpdate(self, ctx:PseudocodeParser.ForUpdateContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#ifStatement.
    def enterIfStatement(self, ctx:PseudocodeParser.IfStatementContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#ifStatement.
    def exitIfStatement(self, ctx:PseudocodeParser.IfStatementContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#whileLoop.
    def enterWhileLoop(self, ctx:PseudocodeParser.WhileLoopContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#whileLoop.
    def exitWhileLoop(self, ctx:PseudocodeParser.WhileLoopContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#returnStatement.
    def enterReturnStatement(self, ctx:PseudocodeParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#returnStatement.
    def exitReturnStatement(self, ctx:PseudocodeParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#breakStatement.
    def enterBreakStatement(self, ctx:PseudocodeParser.BreakStatementContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#breakStatement.
    def exitBreakStatement(self, ctx:PseudocodeParser.BreakStatementContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#block.
    def enterBlock(self, ctx:PseudocodeParser.BlockContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#block.
    def exitBlock(self, ctx:PseudocodeParser.BlockContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#expression.
    def enterExpression(self, ctx:PseudocodeParser.ExpressionContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#expression.
    def exitExpression(self, ctx:PseudocodeParser.ExpressionContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#OrExpr.
    def enterOrExpr(self, ctx:PseudocodeParser.OrExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#OrExpr.
    def exitOrExpr(self, ctx:PseudocodeParser.OrExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#OrPass.
    def enterOrPass(self, ctx:PseudocodeParser.OrPassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#OrPass.
    def exitOrPass(self, ctx:PseudocodeParser.OrPassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#AndExpr.
    def enterAndExpr(self, ctx:PseudocodeParser.AndExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#AndExpr.
    def exitAndExpr(self, ctx:PseudocodeParser.AndExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#AndPass.
    def enterAndPass(self, ctx:PseudocodeParser.AndPassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#AndPass.
    def exitAndPass(self, ctx:PseudocodeParser.AndPassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#CompareExpr.
    def enterCompareExpr(self, ctx:PseudocodeParser.CompareExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#CompareExpr.
    def exitCompareExpr(self, ctx:PseudocodeParser.CompareExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#ComparisonPass.
    def enterComparisonPass(self, ctx:PseudocodeParser.ComparisonPassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#ComparisonPass.
    def exitComparisonPass(self, ctx:PseudocodeParser.ComparisonPassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#AddExpr.
    def enterAddExpr(self, ctx:PseudocodeParser.AddExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#AddExpr.
    def exitAddExpr(self, ctx:PseudocodeParser.AddExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#AdditivePass.
    def enterAdditivePass(self, ctx:PseudocodeParser.AdditivePassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#AdditivePass.
    def exitAdditivePass(self, ctx:PseudocodeParser.AdditivePassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#MulExpr.
    def enterMulExpr(self, ctx:PseudocodeParser.MulExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#MulExpr.
    def exitMulExpr(self, ctx:PseudocodeParser.MulExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#MultiplicativePass.
    def enterMultiplicativePass(self, ctx:PseudocodeParser.MultiplicativePassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#MultiplicativePass.
    def exitMultiplicativePass(self, ctx:PseudocodeParser.MultiplicativePassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#PowExpr.
    def enterPowExpr(self, ctx:PseudocodeParser.PowExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#PowExpr.
    def exitPowExpr(self, ctx:PseudocodeParser.PowExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#PowerPass.
    def enterPowerPass(self, ctx:PseudocodeParser.PowerPassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#PowerPass.
    def exitPowerPass(self, ctx:PseudocodeParser.PowerPassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#UnaryMinusExpr.
    def enterUnaryMinusExpr(self, ctx:PseudocodeParser.UnaryMinusExprContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#UnaryMinusExpr.
    def exitUnaryMinusExpr(self, ctx:PseudocodeParser.UnaryMinusExprContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#UnaryPass.
    def enterUnaryPass(self, ctx:PseudocodeParser.UnaryPassContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#UnaryPass.
    def exitUnaryPass(self, ctx:PseudocodeParser.UnaryPassContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#ParenExpression.
    def enterParenExpression(self, ctx:PseudocodeParser.ParenExpressionContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#ParenExpression.
    def exitParenExpression(self, ctx:PseudocodeParser.ParenExpressionContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#FunctionCallExpression.
    def enterFunctionCallExpression(self, ctx:PseudocodeParser.FunctionCallExpressionContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#FunctionCallExpression.
    def exitFunctionCallExpression(self, ctx:PseudocodeParser.FunctionCallExpressionContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#ArrayAccessExpression.
    def enterArrayAccessExpression(self, ctx:PseudocodeParser.ArrayAccessExpressionContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#ArrayAccessExpression.
    def exitArrayAccessExpression(self, ctx:PseudocodeParser.ArrayAccessExpressionContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#AtomExpression.
    def enterAtomExpression(self, ctx:PseudocodeParser.AtomExpressionContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#AtomExpression.
    def exitAtomExpression(self, ctx:PseudocodeParser.AtomExpressionContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#expressionList.
    def enterExpressionList(self, ctx:PseudocodeParser.ExpressionListContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#expressionList.
    def exitExpressionList(self, ctx:PseudocodeParser.ExpressionListContext):
        pass


    # Enter a parse tree produced by PseudocodeParser#atom.
    def enterAtom(self, ctx:PseudocodeParser.AtomContext):
        pass

    # Exit a parse tree produced by PseudocodeParser#atom.
    def exitAtom(self, ctx:PseudocodeParser.AtomContext):
        pass



del PseudocodeParser