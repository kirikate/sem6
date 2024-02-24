import re


class VariableTableCell:
    def __init__(self, id: int, name: str, mytype):
        self.id = id
        self.name = name
        self.mytype = mytype


class MyKeyword:
    def __init__(self, word: str):
        self.word = word


class MyBrackets:
    def __init__(self, symbols: str):
        self.symbols = symbols
        self.openSymbol = symbols[0]
        self.closeSymbol = symbols[1]


class MySeparator:
    def __init__(self, symbol: str):
        self.symbol = symbol


class MyOperator:
    def __init__(self, symbol: str):
        self.symbol = symbol


typeid: int = 0


class MyType:
    def __init__(self, name, **kwargs):
        global typeid
        self.name = name
        self.id = typeid
        typeid += 1


class Ptr(MyType):
    def __init__(self, mytype: type, level: int):
        MyType.__init__(self, mytype.Name + "*" * level)
        self.pointersTo = mytype
        self.level = level


class MyZone:
    def __init__(self, beginIndex, endIndex, parentZone):
        if parentZone == None:
            pass
        self.beginIndex = beginIndex
        self.endIndex = endIndex
        pass


keywords: list[MyKeyword] = [
    MyKeyword("for"),
    MyKeyword("while"),
    MyKeyword("do"),
    MyKeyword("return"),
    MyKeyword("const"),
    MyKeyword("switch"),
    MyKeyword("case"),
    MyKeyword("if"),
    MyKeyword("union"),
    MyKeyword("struct"),
    MyKeyword("signed"),
    MyKeyword("unsigned"),
    MyKeyword("default"),
    MyKeyword("else"),
    MyKeyword("#include"),
]

kwStr = ""
for i in range(len(keywords)):
    kwStr += re.escape(keywords[i].word)
    if i != len(keywords) - 1:
        kwStr += "|"

keywordsPattern = re.compile("(" + kwStr + ")")

literalsPatterns = [
    ("float", re.compile("\d+\.\d+")),
    ("int", re.compile("\d+")),
    ("char", re.compile("('.'|'\\[\w0])")),
    ("string", re.compile('".*"')),
]

types: list[MyType] = [
    MyType("int"),
    MyType("char"),
    MyType("short"),
    MyType("long"),
    MyType("void"),
    MyType("double"),
    MyType("float"),
]

operators: list[MyOperator] = [
    MyOperator("++"),
    MyOperator("--"),
    MyOperator("*"),
    MyOperator("/"),
    MyOperator("+"),
    MyOperator("="),
    MyOperator("-"),
]

operatorsStr: str = "("
ttmp: str = ""
for i in range(len(operators)):
    ttmp += re.escape(operators[i].symbol)

    if i != len(operators) - 1:
        ttmp += "|"

operatorsStr += ttmp + ")"
operatorsPattern = re.compile(operatorsStr)

separators: list[MySeparator] = [
    MySeparator(";"),
    MySeparator(","),
    MySeparator(":"),
    MySeparator("?"),
]
separatorsStr: str = "("
ttmp: str = ""
for i in range(len(separators)):
    ttmp += re.escape(separators[i].symbol)
    if i != len(separators) - 1:
        ttmp += "|"

separatorsStr += ttmp + ")"
# print(separatorsStr)
separatorsPattern = re.compile(separatorsStr)

brackets: list[MyBrackets] = [MyBrackets("()"), MyBrackets("[]"), MyBrackets("{}")]
bracketsStr = ""
for i in range(len(brackets)):
    bracketsStr += (
        re.escape(brackets[i].openSymbol) + "|" + re.escape(brackets[i].closeSymbol)
    )
    if i != len(brackets) - 1:
        bracketsStr += "|"

bracketsPattern = re.compile("(" + bracketsStr + ")")

identifierPattern = re.compile("[A-Za-z_]\w*")


def separateByMatches(matches, string):
    separated = [string]
    for j in range(len(matches)):
        last = separated.pop()
        split_results: re.Match = re.search(re.escape(matches[j]), last)

        beg = split_results.start()
        end = split_results.end()

        if last[0:beg] != "":
            separated.append(last[0:beg])
        if last[beg:end] != "":
            separated.append(last[beg:end])
        if last[end:] != "":
            separated.append(last[end:])
    return separated


def separate(text) -> list[str]:
    pattern = re.compile(r"(\".*\"|\S+)")
    res = re.findall(pattern, text)

    # need to check for commas brackets operators
    i: int = 0
    while i < len(res):
        piece = res[i]
        # print(res[i])
        tmp = re.findall(operatorsPattern, piece)
        if tmp:
            separated = separateByMatches(tmp, res[i])
            res = res[0:i] + separated + res[i + 1 :]

        tmp = re.findall(separatorsPattern, res[i])

        if tmp:
            separated = separateByMatches(tmp, res[i])
            res = res[0:i] + separated + res[i + 1 :]

        tmp = re.findall(bracketsPattern, res[i])
        if tmp:
            separated = separateByMatches(tmp, res[i])
            res = res[0:i] + separated + res[i + 1 :]
        i += 1

    return res


def findInTableById(table: list, id: int):
    for i in range(len(table) - 1, -1, -1):
        if table[i].id == id:
            return i
    return None


def findInTableByName(table: list, name: str) -> int:
    for i in range(len(table) - 1, -1, -1):
        print(i)
        if table[i].name == name:
            return i
    return None


def findInTypeTableByName(table: list[MyType], name: str):
    for i in range(len(table) - 1, -1, -1):
        print(i)
        if table[i].name == name:
            return i
    return None


vars_id_counter: int = 0


def createTables(tokens: list[str]):
    global vars_id_counter
    global types
    # name id
    vars_table: list[VariableTableCell] = []

    type_table: list[MyType] = []
    for mytype in types:
        type_table.append(mytype)

    for i in range(len(tokens)):
        print(tokens[i])
        isLiteral: bool = False
        # if not keyword operator or literal or sep then identificator
        for typename, pattern in literalsPatterns:
            isLiteral = isLiteral or re.match(pattern, tokens[i])

        isType: bool = False
        for mytype in type_table:
            isType = isType or re.match(re.escape(mytype.name), tokens[i])
        if not (
            re.match(keywordsPattern, tokens[i])
            or re.match(operatorsPattern, tokens[i])
            or re.match(separatorsPattern, tokens[i])
            or isLiteral
            or isType
        ):
            if not re.match(identifierPattern, tokens[i]):
                print("Lexical error")
                continue

            if tokens[i - 1] == "struct":
                print("it's new type!!!")
                index = findInTypeTableByName(type_table, tokens[i])
                if index == None:
                    type_table.append(MyType(tokens[i]))

            print("it's variable!!!")
            index = findInTypeTableByName(type_table, tokens[i])
            if index != None:
                continue

            index = findInTableByName(vars_table, tokens[i])
            if index == None:
                vars_table.append(
                    VariableTableCell(
                        vars_id_counter,
                        tokens[i],
                        type_table[findInTypeTableByName(type_table, tokens[i - 1])],
                    )
                )
                vars_id_counter += 1

    for i in range(len(vars_table)):
        print(f"var{vars_table[i].id} {vars_table[i].name} {vars_table[i].mytype.name}")

    for i in range(len(type_table)):
        print(f"t{type_table[i].id} {type_table[i].name}")


def analyze(text: str):
    # print(text)
    tokens = separate(text)
    for token in tokens:
        print(token)

    print()
    print("----------------------------------")
    print()
    print()
    createTables(tokens)


if __name__ == "__main__":
    # print("hui")
    file = open("test.c")
    text: str = file.read()
    file.close()
    analyze(text)
