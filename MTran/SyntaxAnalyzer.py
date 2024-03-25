from LexicalAnalyzer import *
from LexicalAnalyzer import IStringable, MyLiteral, MyType, VariableTableCell

keywordsdict = {kw.word: kw for kw in keywordsdict}
bracketsdict = {br.symbols: br for br in brackets}
separatorsDict = {s.symbol: s for s in separators}
operatorsDict = {op.symbol: op for op in operators}


def find(iterable, func):
    for it in iterable:
        if func(it):
            return it


class INode:
    def __init__(self, parent: INode):
        self.parent: INode = parent

    def execute(self):
        pass

    # returns index of last scanned token
    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:
        pass

    def getVariable(self, name: str):
        pass


class UnarOperatorNode(INode):
    def __init__(self, parent, operator: MyOperator):
        super().__init__(parent)
        self.operator = operator
        self.variable = None

    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:
        i = index
        op = self.operator
        if (
            tokens[i + 1] in vars_table
            and op.direction == "both"
            or op.direction == "right"
        ):
            self.variable = tokens[i + 1]
            i += 1
        elif (
            tokens[i - 1] in vars_table
            and op.direction == "left"
            or op.direction == "both"
        ):
            self.variable = tokens[i - 1]
        else:
            raise Exception(
                f"Syntax error at token {i}: unar operator require identifier as argument"
            )

        return i


class BinarOperatorNode(INode):
    def __init__(self, parent: INode, operator: MyOperator):
        super().__init__(parent)
        self.operator = operator
        self.left = None
        self.right = None

    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:
        i = index
        if tokens[index - 1] in brackets:
            # check for closed and get open and for function call
            pass
        elif tokens[index - 1] in vars_table:
            vn = GetVariableValueNode(self)
            vn.buildTree(tokens, index - 1, type_table, vars_table, literals_table)
            self.left = vn
        elif tokens[index - 1 in literals_table]:
            ln = GetLiteralValueNode(self)
            ln.buildTree(tokens, index - 1, type_table, vars_table, literals_table)
            self.left = ln
        else:
            raise Exception(
                f"Syntax error at token {i-1}: this token cant be an operator argument"
            )

        if tokens[index + 1] in brackets:
            br = find(brackets, lambda br: br == tokens[index + 1])
            if br.openClose(index + 1) is None:
                raise Exception(
                    f"Syntax error at token {i}: binar operator before bracket"
                )

            cn = CalculatedValueNode(self, index + 1, br.openClose[index + 1])
            cn.buildTree(tokens, index, type_table, vars_table, literals_table)
            self.right = cn
        if tokens[index + 1] in vars_table:
            if tokens[i + 2] in brackets:
                pass
            else:
                vn = GetVariableValueNode(self)
                vn.buildTree(tokens, index - 1, type_table, vars_table, literals_table)
                self.right = vn


class GetLiteralValueNode(INode):
    def __init__(parent):
        super().__init__(parent)

    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:
        if not (tokens[index] in literals_table):
            raise Exception(f"Syntax error at token {i}: Unkown literal")
        self.literal: MyLiteral = tokens[index]


class GetVariableValueNode(INode):
    def __init__(self, parent):
        super().__init__(parent)

    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:

        scopeStart = tokens[index].scopeStart
        if not (
            scopeStart < index and bracketsdict["{}"].openClose[scopeStart] > index
        ):
            raise Exception(f"Syntax error at token {i}: Unknown variable")

        self.variable = tokens[i]


# NEED to know its boundaries
class CalculatedValueNode(INode):
    def __init__(self, parent, begin: int, end: int):
        super().__init__(parent)
        self.begin = begin
        self.end = end

    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:
        self.value
        i = index
        currentPriorOperatorIndex = -1
        currentPrior = 0

        while i < len(tokens):
            if tokens[i] in operators:
                if tokens[i].prior > currentPrior:
                    currentPriorOperatorIndex = i
                    currentPrior = tokens[i].prior
            elif tokens[i] in vars_table:
                if tokens[i + 1] in brackets:
                    if tokens[i + 1] is bracketsdict["{}"]:
                        raise Exception(
                            f"Syntax error at token {i+1}: incorrect operator"
                        )
                    if 2 > currentPrior:
                        currentPrior = 2
                        currentPriorOperatorIndex = i
                    i = tokens[i + 1].openClose[i + 1]
            elif tokens[i] in brackets:
                if 2 > currentPrior:
                    currentPrior = 2
                    currentPriorOperatorIndex = i
                i = tokens[i].openClose[i]

            i += 1

        if currentPrior == 0:
            if index + 1 != i:
                raise Exception(
                    f"Syntax error at token {i}: Incorrect initial value declaration"
                )
            if tokens[index] in literals_table:
                vn = GetLiteralValueNode(self)
                vn.buildTree(tokens, index, type_table, vars_table, literals_table)
                self.value = vn
            elif tokens[index] in vars_table:
                vn = GetVariableValueNode(self)
                vn.buildTree(tokens, index, type_table, vars_table, literals_table)
                self.value = vn
            elif tokens[index] in operators:
                op = find(operators, lambda op: op == tokens[i])
                if op.argCount == "unar":
                    uo = UnarOperatorNode(self, op)
                    i = uo.buildTree(tokens, i, type_table, vars_table, literals_table)
                    self.value = uo
                if op.argCount == "binar":
                    pass
            elif tokens[index] in brackets:
                pass
            else:
                raise Exception(
                    f"Syntax error at token {i}: Unkown type to identify operator"
                )

        return i

    def getVariable(self, name: str):
        self.parent.getVariable(name)


class DeclarationNode(INode):
    def __init__(self, parent: INode):
        super().__init__(parent)

    def buildTree(
        self,
        tokens: list[IStringable],
        index: int,
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ) -> int:
        i = index
        self.varType = tokens[i]
        i += 1

        if not isinstance(tokens[i], VariableTableCell):
            raise Exception(f"Incorrect var declaration syntax at token {i}")

        self.varName = tokens[i].name
        self.initialValue: CalculatedValueNode | None = None
        i += 1
        if tokens[i] is not separatorsDict[";"] or tokens[i] is not operators["="]:
            raise Exception(
                f"Syntax Error: incorrect var declaration syntax at token {i}"
            )

        if tokens[i] is separatorsDict[";"]:
            return i

    def getVariable(self, name: str):
        return self.parent.getVariable(name)

    def execute(self):
        pass


class FunctionNode(INode):
    def __init__(self, parent: INode):
        pass


class Program(INode):
    def __init__(
        self,
        tokens: list[IStringable],
        type_table: list[MyType],
        vars_table: list[VariableTableCell],
        literals_table: list[MyLiteral],
    ):
        super().__init__(None)
        self.functions = dict[str, FunctionNode]()
        self.variables = dict[str, DeclarationNode]()

        i: int = 0
        while i < len(tokens):
            if tokens[i] == keywordsdict["#include"]:
                pass
            elif tokens[i] in type_table:
                if tokens[i + 1] not in vars_table:
                    raise Exception(f"Expected identifier at token {i+1}")
                name = tokens[i + 1]
                if tokens[i + 2] == bracketsdict["()"]:
                    fn = FunctionNode(self)
                    i = fn.buildTree(tokens, i)
                    self.functions[name] = fn
                else:
                    dn = DeclarationNode(self)
                    i = dn.buildTree(tokens, i)
                    self.variables[name] = dn
            else:
                raise Exception(
                    "Error at token i: On;y function declarations, global variables and include directives can be in global scope"
                )
            i += 1
