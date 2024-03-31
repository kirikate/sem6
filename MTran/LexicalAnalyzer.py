import re


class IStringable:
    def toString(self, i: int):
        pass


class VariableTableCell(IStringable):
    def __init__(self, id: int, name: str, mytype, scopeStart: int):
        self.id = id
        self.name = name
        self.mytype: MyType = mytype
        self.scopeStart = scopeStart

    def toString(self, i: int):
        return f"v{self.id}"


keywordIdCounter = 0


class MyKeyword(IStringable):
    def __init__(self, word: str):
        global keywordIdCounter

        self.word = word
        self.id = keywordIdCounter

        keywordIdCounter += 1

    def toString(self, i: int) -> str:
        return f"k{self.id}"


bracketsIdCounter = 0


class MyBrackets(IStringable):
    def __init__(self, symbols: str, prior: int):
        global bracketsIdCounter

        self.symbols = symbols
        self.openSymbol = symbols[0]
        self.closeSymbol = symbols[1]

        self.id = bracketsIdCounter
        self.prior = prior
        self.openClose = dict()

        bracketsIdCounter += 1

    def open(self, i: int):
        self.openClose[i] = None

    def close(self, i: int, end: int):
        self.openClose[i] = end

    def toString(self, i: int) -> str:
        if i in self.openClose.keys():
            return f"b{self.id}o{i}"
        elif i in self.openClose.values():
            for key, val in self.openClose.items():
                if val == i:
                    return f"b{self.id}c{key}"
        raise Exception(f"wtf dude bracket token {i} is undefined")


separatorsCountId = 0


class MySeparator(IStringable):
    def __init__(self, symbol: str):
        global separatorsCountId
        self.symbol = symbol
        self.id = separatorsCountId
        separatorsCountId += 1

    def toString(self, i: int):
        return f"s{self.id}"


operatorsCountId = 0


# lambda на понять какое приоритет
# определить на унарный и с каких сторон можно брать значения
# direction : left, right, both
# arg count: unar, binar, ternar
class MyOperator(IStringable):
    def __init__(
        self, symbol: str, prior: int, argCount: str = "binar", direction: str = None
    ):
        global operatorsCountId

        self.symbol = symbol
        self.id = operatorsCountId
        self.prior = prior

        self.argCount = argCount
        self.direction = direction
        operatorsCountId += 1

    def toString(self, i: int):
        return f"o{self.id}"


typeid: int = 0


class MyType(IStringable):
    def __init__(self, name, **kwargs):
        global typeid
        self.name = name
        self.id = typeid
        typeid += 1

    def toString(self, i: int):
        return f"t{self.id}"


class Ptr(MyType):
    def __init__(self, mytype: type, level: int):
        MyType.__init__(self, mytype.Name + "*" * level)
        self.pointersTo = mytype
        self.level = level


literalCountId = 0


class MyLiteral(IStringable):
    def __init__(self, text: str, tokenIndex: int) -> None:
        global literalCountId
        self.text = text
        self.tokenIndex = tokenIndex
        self.id = literalCountId
        literalCountId += 1

    def toString(self, i: int):
        return f"l{self.id}"


keywordsList: list[MyKeyword] = [
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
for i in range(len(keywordsList)):
    kwStr += re.escape(keywordsList[i].word)
    if i != len(keywordsList) - 1:
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
    MyOperator("++", 2, argCount="unar", direction="both"),
    MyOperator("--", 2, argCount="unar", direction="both"),
    MyOperator("->", 2, argCount="unar", direction="right"),
    MyOperator("*", 5),
    MyOperator("/", 5),
    MyOperator("+", 6),
    MyOperator("==", 9),
    MyOperator("-", 6),
    MyOperator("<", 8),
    MyOperator(">", 8),
    MyOperator("<=", 8),
    MyOperator(">=", 8),
    MyOperator("&&", 13),
    MyOperator("||", 14),
    MyOperator("&=", 15),
    MyOperator("|=", 15),
    MyOperator("=", 15),
    MyOperator("&", 3),
    MyOperator(".", 2),
    MyOperator("?", 15),
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
]
separatorsStr: str = "("
ttmp: str = ""
for i in range(len(separators)):
    ttmp += re.escape(separators[i].symbol)
    if i != len(separators) - 1:
        ttmp += "|"

separatorsStr += ttmp + ")"
separatorsPattern = re.compile(separatorsStr)

brackets: list[MyBrackets] = [
    MyBrackets("()", 2),
    MyBrackets("[]", 2),
    MyBrackets("{}", None),
]
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
        if table[i].name == name:
            return i
    return None


def findInTypeTableByName(table: list[MyType], name: str):
    for i in range(len(table) - 1, -1, -1):
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

    literals_table: list[MyLiteral] = []
    for mytype in types:
        type_table.append(mytype)

    for i in range(len(tokens)):
        if tokens[i] == "{" or tokens[i] == "for":
            scope_starts.append(i)
        if tokens[i] == "}":
            scope_starts.pop()

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
                # print("it's new type!!!")
                index = findInTypeTableByName(type_table, tokens[i])
                if index == None:
                    type_table.append(MyType(tokens[i]))

            # print("it's variable!!!")
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

    # for i in range(len(vars_table)):
    #     print(
    #         f"var{vars_table[i].id} {vars_table[i].name} {vars_table[i].mytype.name} {vars_table[i].scopeStart}"
    #     )

    # for i in range(len(type_table)):
    #     print(f"t{type_table[i].id} {type_table[i].name}")
    return (type_table, vars_table, literals_table)


def find_var_by_name_and_scope(
    vars_table: list[VariableTableCell], name: str, scopeStart: int, symbols: str = "{}"
):
    variants: list[VariableTableCell] = list()
    scope_brackets = [bracket for bracket in brackets if bracket.symbols == symbols][0]
    for cell in vars_table:
        if cell.name == name and (
            cell.scopeStart <= scopeStart
            and scope_brackets.openClose.get(scopeStart) is None
        ):
            variants.append(cell)

    if len(variants):
        return variants.pop()

    return None


def change_to_ids(
    type_table: list[MyType],
    vars_table,
    literals_table: list[MyLiteral],
    original_tokens: list[str],
):
    new_tokens: list[IStringable] = original_tokens.copy()
    scope_starts: dict[str, list[int]] = {}
    for br in brackets:
        scope_starts[br.symbols] = []

    scope_starts["{}"].append(0)

    for i in range(len(new_tokens)):
        var_cell = find_var_by_name_and_scope(
            vars_table, new_tokens[i], scope_starts["{}"][-1]
        )
        print(
            f'token {new_tokens[i]} var_cell {var_cell} scopestart {scope_starts["{}"][-1]}'
        )

        if var_cell is None and len(scope_starts["()"]):
            var_cell = find_var_by_name_and_scope(
                vars_table, new_tokens[i], scope_starts["()"][-1], symbols="()"
            )

        if var_cell is not None:
            new_tokens[i] = var_cell
            continue
        type_index = findInTypeTableByName(type_table, new_tokens[i])

        if type_index is not None:
            new_tokens[i] = type_table[type_index]
            continue

        if i in [it.tokenIndex for it in literals_table]:
            for literal in literals_table:
                if literal.tokenIndex == i:
                    new_tokens[i] = literal
        elif new_tokens[i] in [op.symbol for op in operators]:
            for op in operators:
                if new_tokens[i] == op.symbol:
                    new_tokens[i] = op
        elif new_tokens[i] in [kw.word for kw in keywordsList]:
            for kw in keywordsList:
                if kw.word == new_tokens[i]:
                    new_tokens[i] = kw
        elif new_tokens[i] in [sep.symbol for sep in separators]:
            for sep in separators:
                if sep.symbol == new_tokens[i]:
                    new_tokens[i] = sep
        elif new_tokens[i] in [br.openSymbol for br in brackets]:
            for br in brackets:
                if br.openSymbol == new_tokens[i]:
                    scope_starts[br.symbols].append(i)
                    br.open(i)
                    new_tokens[i] = br
        elif new_tokens[i] in [br.closeSymbol for br in brackets]:
            for br in brackets:
                if br.closeSymbol == new_tokens[i]:
                    poped = scope_starts[br.symbols].pop()
                    br.close(poped, i)
                    new_tokens[i] = br

    return new_tokens


def analyze(text: str):
    tokens = separate(text)
    for token in tokens:
        print(token)
    (type_table, vars_table, literals_table) = createTables(tokens)

    for var in vars_table:
        print(f"{var.mytype.name} {var.name} {var.scopeStart}")
    new_tokens = change_to_ids(type_table, vars_table, literals_table, tokens)
    file = open("res.txt", "w")
    file.truncate()

    print("tokens:\n", file=file)
    for i in range(len(new_tokens)):
        print(f"{new_tokens[i].toString(i)}  ==  {tokens[i]}", file=file)

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
    for kw in keywordsList:
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

    return (new_tokens, type_table, vars_table, literals_table)


def clearComments(text: str) -> str:
    new_text = str()
    i: int = 0
    while i < len(text):
        if text[i] == "/":
            if text[i + 1] == "/":
                while i < len(text) and text[i] != "\n":
                    i += 1
            elif text[i + 1] == "*":
                while i < len(text) and text[i - 2] + text[i - 1] != "*/":
                    i += 1
        if i >= len(text):
            continue
        new_text += text[i]
        i += 1
    return new_text
