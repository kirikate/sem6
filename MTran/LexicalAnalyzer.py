import re


class VariableTableCell:
    def __init__(self, id: int, name: str, mytype, scopeStart: int):
        self.id = id
        self.name = name
        self.mytype = mytype
        self.scopeStart = scopeStart


keywordIdCounter = 0


class MyKeyword:
    def __init__(self, word: str):
        global keywordIdCounter

        self.word = word
        self.id = keywordIdCounter

        keywordIdCounter += 1


bracketsIdCounter = 0


class MyBrackets:
    def __init__(self, symbols: str):
        global bracketsIdCounter

        self.symbols = symbols
        self.openSymbol = symbols[0]
        self.closeSymbol = symbols[1]

        self.id = bracketsIdCounter

        bracketsIdCounter += 1


separatorsCountId = 0


class MySeparator:
    def __init__(self, symbol: str):
        global separatorsCountId
        self.symbol = symbol
        self.id = separatorsCountId
        separatorsCountId += 1


operatorsCountId = 0


class MyOperator:
    def __init__(self, symbol: str):
        global operatorsCountId

        self.symbol = symbol
        self.id = operatorsCountId

        operatorsCountId += 1


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


literalCountId = 0


class MyLiteral:
    def __init__(self, text: str, tokenIndex: int) -> None:
        global literalCountId
        self.text = text
        self.tokenIndex = tokenIndex
        self.id = literalCountId
        literalCountId += 1


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
    MyOperator("=="),
    MyOperator("-"),
    MyOperator("<"),
    MyOperator(">"),
    MyOperator("<="),
    MyOperator(">="),
    MyOperator("&&"),
    MyOperator("||"),
    MyOperator("&="),
    MyOperator("|="),
    MyOperator("="),
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

# type vars literals ops kws separators brackets


def createTables(tokens: list[str]):
    global vars_id_counter
    global types

    # name id
    vars_table: list[VariableTableCell] = []

    scope_starts = [0]
    type_table: list[MyType] = []

    literals_table: list = []
    for mytype in types:
        type_table.append(mytype)

    for i in range(len(tokens)):
        if tokens[i] == "{" or tokens[i] == "for":
            scope_starts.append(i)
        if tokens[i] == "}":
            scope_starts.pop()

        print(tokens[i])
        isLiteral: bool = False
        # if not keyword operator or literal or sep then identificator
        for typename, pattern in literalsPatterns:
            isLiteral = isLiteral or re.match(pattern, tokens[i])

        isType: bool = False
        for mytype in type_table:
            isType = isType or re.match(re.escape(mytype.name), tokens[i])

        isBracket: bool = False
        for bracket in brackets:
            isBracket = isBracket or (
                bracket.openSymbol == tokens[i] or bracket.closeSymbol == tokens[i]
            )

        if not (
            re.match(keywordsPattern, tokens[i])
            or re.match(operatorsPattern, tokens[i])
            or re.match(separatorsPattern, tokens[i])
            or isLiteral
            or isType
            or isBracket
        ):
            if not re.match(identifierPattern, tokens[i]):
                file = open("res.txt", "w")
                print(f"Lexical error at token {i}: {tokens[i]}", file=file)
                file.close()
                exit(0)
                continue

            # if new type
            if tokens[i - 1] == "struct":
                print("it's new type!!!")
                index = findInTypeTableByName(type_table, tokens[i])
                if index == None:
                    type_table.append(MyType(tokens[i]))

            print("it's variable!!!")
            # if type before var declaration
            index = findInTableByName(type_table, tokens[i])
            if index != None:
                continue

            # if not declaration
            if findInTypeTableByName(type_table, tokens[i - 1]) is None:
                if tokens[i] not in [var.name for var in vars_table]:
                    file = open("res.txt", "w")
                    print(
                        f"Lexical error at token {i}: {tokens[i]}. What's this?",
                        file=file,
                    )
                    file.close()
                    exit(0)
                continue

            vars_table.append(
                VariableTableCell(
                    vars_id_counter,
                    tokens[i],
                    type_table[findInTypeTableByName(type_table, tokens[i - 1])],
                    scope_starts[-1],
                )
            )
            vars_id_counter += 1
        else:
            if isLiteral:
                literals_table.append(MyLiteral(tokens[i], i))

    for i in range(len(vars_table)):
        print(
            f"var{vars_table[i].id} {vars_table[i].name} {vars_table[i].mytype.name} {vars_table[i].scopeStart}"
        )

    for i in range(len(type_table)):
        print(f"t{type_table[i].id} {type_table[i].name}")
    return (type_table, vars_table, literals_table)


def find_var_by_name_and_scope(
    vars_table: list[VariableTableCell], name: str, scopeStart: int
):
    for cell in vars_table:
        if cell.name == name and cell.scopeStart == scopeStart:
            return cell
    return None


def change_to_ids(
    type_table: list[MyType],
    vars_table,
    literals_table: list[MyLiteral],
    original_tokens: list[str],
):
    new_tokens = original_tokens.copy()
    scope_starts: dict[str, list[int]] = {}
    for br in brackets:
        scope_starts[br.symbols] = []

    scope_starts["{}"].append(0)

    for i in range(len(new_tokens)):
        var_cell = find_var_by_name_and_scope(
            vars_table, new_tokens[i], scope_starts["{}"][-1]
        )
        if var_cell is not None:
            new_tokens[i] = f"v{var_cell.id}"
            continue
        type_index = findInTypeTableByName(type_table, new_tokens[i])

        if type_index is not None:
            new_tokens[i] = f"t{type_table[type_index].id}"
            continue

        if i in [it.tokenIndex for it in literals_table]:
            for literal in literals_table:
                if literal.tokenIndex == i:
                    new_tokens[i] = f"l{literal.id}"
        elif new_tokens[i] in [op.symbol for op in operators]:
            for op in operators:
                if new_tokens[i] == op.symbol:
                    new_tokens[i] = f"o{op.id}"
        elif new_tokens[i] in [kw.word for kw in keywords]:
            for kw in keywords:
                if kw.word == new_tokens[i]:
                    new_tokens[i] = f"k{kw.id}"
        elif new_tokens[i] in [sep.symbol for sep in separators]:
            for sep in separators:
                if sep.symbol == new_tokens[i]:
                    new_tokens[i] = f"s{sep.id}"
        elif new_tokens[i] in [br.openSymbol for br in brackets]:
            for br in brackets:
                if br.openSymbol == new_tokens[i]:
                    scope_starts[br.symbols].append(i)
                    new_tokens[i] = f"b{br.id}o{scope_starts[br.symbols][-1]}"
        elif new_tokens[i] in [br.closeSymbol for br in brackets]:
            for br in brackets:
                if br.closeSymbol == new_tokens[i]:
                    poped = scope_starts[br.symbols].pop()
                    new_tokens[i] = f"b{br.id}c{poped}"

    return new_tokens


def analyze(text: str):
    # print(text)
    tokens = separate(text)
    # for token in tokens:
    #     print(token)
    (type_table, vars_table, literals_table) = createTables(tokens)
    new_tokens = change_to_ids(type_table, vars_table, literals_table, tokens)
    file = open("res.txt", "w")
    file.truncate()

    print("tokens:\n", file=file)
    for i in range(len(new_tokens)):
        print(f"{new_tokens[i]}  ==  {tokens[i]}", file=file)

    print("\n-------------\n", file=file)
    print("table of types(t):\n", file=file)
    for type in type_table:
        print(f"{type.id} {type.name}", file=file)

    print("\n-------------\n", file=file)
    print("table of vars(v):\n", file=file)
    for var in vars_table:
        print(f"{var.id} {var.name} {var.mytype.name} {var.scopeStart}", file=file)

    print("\n-------------\n", file=file)
    print("table of keywords(k):\n", file=file)
    for kw in keywords:
        print(f"{kw.id} {kw.word}", file=file)

    print("\n-------------\n", file=file)
    print("table of separators(s):\n", file=file)
    for sep in separators:
        print(f"{sep.id} {sep.symbol}", file=file)

    print("\n-------------\n", file=file)
    print("table of brackets(b{id}[oc]{firstToken}):\n", file=file)
    for br in brackets:
        print(f"{br.id} {br.symbols}", file=file)

    print("\n-------------\n", file=file)
    print("table of operators(o):\n", file=file)
    for op in operators:
        print(f"{op.id} {op.symbol}", file=file)
    file.close()


if __name__ == "__main__":
    # print("hui")
    file = open("test.c")
    text: str = file.read()
    file.close()
    analyze(text)
