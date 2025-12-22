# Generated from Pseudocode.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PseudocodeParser import PseudocodeParser
else:
    from PseudocodeParser import PseudocodeParser

# This class defines a complete generic visitor for a parse tree produced by PseudocodeParser.

class PseudocodeVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PseudocodeParser#program.
    def visitProgram(self, ctx:PseudocodeParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#statement.
    def visitStatement(self, ctx:PseudocodeParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#assignment.
    def visitAssignment(self, ctx:PseudocodeParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#RangeArray.
    def visitRangeArray(self, ctx:PseudocodeParser.RangeArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#SizeArray.
    def visitSizeArray(self, ctx:PseudocodeParser.SizeArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#ValueArray.
    def visitValueArray(self, ctx:PseudocodeParser.ValueArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#functionDecl.
    def visitFunctionDecl(self, ctx:PseudocodeParser.FunctionDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#paramList.
    def visitParamList(self, ctx:PseudocodeParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#forEachLoop.
    def visitForEachLoop(self, ctx:PseudocodeParser.ForEachLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#ifStatement.
    def visitIfStatement(self, ctx:PseudocodeParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#whileLoop.
    def visitWhileLoop(self, ctx:PseudocodeParser.WhileLoopContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#returnStatement.
    def visitReturnStatement(self, ctx:PseudocodeParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#breakStatement.
    def visitBreakStatement(self, ctx:PseudocodeParser.BreakStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#block.
    def visitBlock(self, ctx:PseudocodeParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#expression.
    def visitExpression(self, ctx:PseudocodeParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#OrExpr.
    def visitOrExpr(self, ctx:PseudocodeParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#OrPass.
    def visitOrPass(self, ctx:PseudocodeParser.OrPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#AndExpr.
    def visitAndExpr(self, ctx:PseudocodeParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#AndPass.
    def visitAndPass(self, ctx:PseudocodeParser.AndPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#CompareExpr.
    def visitCompareExpr(self, ctx:PseudocodeParser.CompareExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#ComparisonPass.
    def visitComparisonPass(self, ctx:PseudocodeParser.ComparisonPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#AddExpr.
    def visitAddExpr(self, ctx:PseudocodeParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#AdditivePass.
    def visitAdditivePass(self, ctx:PseudocodeParser.AdditivePassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#MulExpr.
    def visitMulExpr(self, ctx:PseudocodeParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#MultiplicativePass.
    def visitMultiplicativePass(self, ctx:PseudocodeParser.MultiplicativePassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#PowExpr.
    def visitPowExpr(self, ctx:PseudocodeParser.PowExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#PowerPass.
    def visitPowerPass(self, ctx:PseudocodeParser.PowerPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#UnaryMinusExpr.
    def visitUnaryMinusExpr(self, ctx:PseudocodeParser.UnaryMinusExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#UnaryPass.
    def visitUnaryPass(self, ctx:PseudocodeParser.UnaryPassContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#ParenExpression.
    def visitParenExpression(self, ctx:PseudocodeParser.ParenExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#FunctionCallExpression.
    def visitFunctionCallExpression(self, ctx:PseudocodeParser.FunctionCallExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#ArrayAccessExpression.
    def visitArrayAccessExpression(self, ctx:PseudocodeParser.ArrayAccessExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#AtomExpression.
    def visitAtomExpression(self, ctx:PseudocodeParser.AtomExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#expressionList.
    def visitExpressionList(self, ctx:PseudocodeParser.ExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PseudocodeParser#atom.
    def visitAtom(self, ctx:PseudocodeParser.AtomContext):
        return self.visitChildren(ctx)



del PseudocodeParser