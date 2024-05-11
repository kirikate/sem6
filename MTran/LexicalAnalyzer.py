import re


def find(iterable, func):
    for it in iterable:
        if func(it):
            return it


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
        self, symbol: str, prior: int, argCount: str = "binar", direction: str = None, verificator = None,
        handler = None
    ):
        global operatorsCountId

        self.symbol = symbol
        self.id = operatorsCountId
        self.prior = prior

        self.argCount = argCount
        self.direction = direction
        self.verificator = verificator
        operatorsCountId += 1
        self.handler = None

    def toString(self, i: int):
        return f"o{self.id}"


typeid: int = 0


class MyType(IStringable):
    # def __init__(self, name, prior: int, size:int, isConst=False):
    def __init__(self, name, prior: int, isConst=False):
        global typeid
        self.name = name
        self.id = typeid
        typeid += 1
        self.prior = prior
        self.isConst = isConst
        # self.size = size

    def toString(self, i: int):
        return f"t{self.id}"


class MyPtr(MyType):
    def __init__(self, type_table:list[MyType], token:str):
        MyType.__init__(self, token, -1)
        level = token.count('*')
        print(f'LOLOLL {token}  level: {level}')
        typename = token[:-(level)]
        self.pointersTo = [t for t in type_table if t.name == typename][0]
        self.level = level


literalCountId = 0


class MyLiteral(IStringable):
    def __init__(self, text: str, tokenIndex: int) -> None:
        global literalCountId
        self.text = text
        self.tokenIndex = tokenIndex
        self.id = literalCountId
        self.mytype: MyType = None
        literalCountId += 1

        for t, p in literalsPatterns:
            if p.match(text):
                self.mytype: MyType = t
                break
        
        if self.mytype.name == 'char*':
            self.value = self.text[1:-1]
            self.value += chr(0)
        if self.mytype.name == 'char':
            self.value = self.text[1:-1]
        if self.mytype.name == 'int':
            self.value = int(self.text)
        if self.mytype.name == 'float':
            self.value = float(self.text)

    def toString(self, i: int):
        return f"l{self.id}"


def BinarArithmetic(op: MyOperator, tl: MyType, tr: MyType):
    if find(types, lambda t: t == tl) is None:
        raise Exception(f"Semantic error: cant {op.symbol} to left operand type ({tl.name})")
    if find(types, lambda t: t == tr) is None:
        raise Exception(f"Semantic error: cant {op.symbol} to right operand type ({tr.name})")

    if tl == find(types, lambda t: t.name == "void"):
        raise Exception(f"Semantic error: cant {op.symbol} to void on left operand ({tl.name})")
    if tr == find(types, lambda t: t.name == "void"):
        raise Exception(f"Semantic error: cant {op.symbol} to void on right operand ({tr.name})")
    
    if op.prior == 15:
        if tl.isConst:
            raise Exception(f'Semantic error: attempt to change const value')


def UnarArithmetic(op: MyOperator, t: MyType, t2):
    if type(t) == MyPtr:
        return
    if t.isConst:
        raise Exception(f'Semantic error: Attempt to change const value')
    if find(types, lambda tlamb: tlamb == t) is None:
        raise Exception(f"Semantic error: cant {op.symbol} to left operand type")

    if t == find(types, lambda t: t.name == "void"):
        raise Exception(f"Semantic error: cant {op.symbol} to void on left operand")


def UnarStar(op: MyOperator, t: MyType, t2):
    if type(t) == MyPtr:
        return
    raise Exception(f"Semantic error: cant * to not ptr var of type {t.name}")


keywordsList: list[MyKeyword] = [
    MyKeyword("for"),
    MyKeyword("while"),
    MyKeyword("do"),
    MyKeyword("return"),
    MyKeyword("switch"),
    MyKeyword("case"),
    MyKeyword("if"),
    MyKeyword("struct"),
    MyKeyword("else"),
    MyKeyword("#include"),
]

kwStr = ""
for i in range(len(keywordsList)):
    kwStr += re.escape(keywordsList[i].word)
    if i != len(keywordsList) - 1:
        kwStr += "|"

keywordsPattern = re.compile("(" + kwStr + ")")


types: list[MyType] = [
    MyType("int", 4),
    MyType("char", 6),
    MyType("short", 5),
    MyType("long", 3),
    MyType("void", -1),
    MyType("double", 0),
    MyType("float", 1),
    MyType("const int", 4, isConst=True),
    MyType("const char", 6, isConst=True),
    MyType("const short", 5, isConst=True),
    MyType("const long", 3, isConst=True),
    MyType("const void", -1, isConst=True),
    MyType("const double", 0, isConst=True),
    MyType("const float", 1,  isConst=True),
]

literalsPatterns: list[tuple] = [
    (find(types, lambda t: t.name == "float"), re.compile(r"\d+\.\d+")),
    (find(types, lambda t: t.name == "int"), re.compile(r"\d+")),
    (find(types, lambda t: t.name == "char"), re.compile(r"('.'|'\[\w])")),
    (MyPtr(types, "char*"), re.compile('".*"')),
]

operators: list[MyOperator] = [
    MyOperator(
        "++",
        2,
        argCount="unar",
        direction="both",
        verificator=UnarArithmetic,
        handler=lambda x: x + 1,
    ),
    MyOperator(
        "--",
        2,
        argCount="unar",
        direction="both",
        verificator=UnarArithmetic,
        handler=lambda x: x - 1,
    ),
    MyOperator("->", 2, argCount="unar", direction="right"),
    MyOperator(
        "*",
        5,
        direction="right",
        verificator=BinarArithmetic,
        handler=lambda x, y: x * y,
    ),
    MyOperator("/", 5, verificator=BinarArithmetic, handler=lambda x, y: x / y),
    MyOperator("+", 6, verificator=BinarArithmetic, handler=lambda x, y: x + y),
    MyOperator("==", 9, verificator=BinarArithmetic, handler=lambda x, y: x == y),
    MyOperator("-", 6, verificator=BinarArithmetic, handler=lambda x, y: x - y),
    MyOperator("<", 8, verificator=BinarArithmetic, handler=lambda x, y: x < y),
    MyOperator(">", 8, verificator=BinarArithmetic, handler=lambda x, y: x > y),
    MyOperator("<=", 8, verificator=BinarArithmetic, handler=lambda x, y: x <= y),
    MyOperator(">=", 8, verificator=BinarArithmetic, handler=lambda x, y: x >= y),
    MyOperator("&&", 13, verificator=BinarArithmetic, handler=lambda x, y: x and y),
    MyOperator("||", 14, verificator=BinarArithmetic, handler=lambda x, y: x or y),
    MyOperator("&=", 15, verificator=BinarArithmetic, handler=lambda x, y: x and y),
    MyOperator("|=", 15, verificator=BinarArithmetic, handler=lambda x, y: x or y),
    MyOperator("=", 15, verificator=BinarArithmetic),
    MyOperator("&", 10, direction="right", verificator=BinarArithmetic, handler=lambda x,y : x&y),
    MyOperator(".", 2),
    MyOperator("%", 5)
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

identifierPattern = re.compile(r"[A-Za-z_]\w*")


def separateByMatches(matches, string):
    print(matches)
    print(string)
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
        if res[i] == "const":
            res[i] = res[i] + ' ' + res[i+1]
            res = res[:i+1] + res[i+2:]

        tmp = re.findall(separatorsPattern, res[i])
        if tmp:
            separated = separateByMatches(tmp, res[i])
            res = res[0:i] + separated + res[i + 1 :]

        tmp = re.findall(bracketsPattern, res[i])
        if tmp:
            separated = separateByMatches(tmp, res[i])
            res = res[0:i] + separated + res[i + 1 :]

        tmp = re.findall(operatorsPattern, res[i])
        if tmp:
            separated = separateByMatches(tmp, res[i])
            res = res[0:i] + separated + res[i + 1 :]
        if re.match(r"\d+", res[i]) and res[i+1] =='.':
            res[i] = res[i] + res[i+1] + res[i+2]
            res = res[:i+1] + res[i+3:]
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
    type_table.append(literalsPatterns[3][0])

    i = 0
    isFor:bool = False
    isStruct = False
    while i < len(tokens):
        if tokens[i] == "{" or tokens[i] == "for":
            if tokens[i] == "for":
                isFor = True
            scope_starts.append(i)

        if tokens[i] == ')' and isFor:
            scope_starts.pop()
            isFor = False
        if tokens[i] == "}":
            scope_starts.pop()
            if isStruct:
                isStruct = False

        if tokens[i] == "struct" and scope_starts[-1] == 0:
            isStruct = True
        ############################
        isLiteral: bool = False
        # if not keyword operator or literal or sep then identificator
        for t, pattern in literalsPatterns:
            isLiteral = isLiteral or re.match(pattern, tokens[i])

        isType: bool = False
        for mytype in type_table:
            isType = isType or re.match(re.escape(mytype.name), tokens[i])
        if(isType):
            if tokens[i+1] == '*':
                while tokens[i+1] == '*':
                    tokens[i] += '*'
                    tokens = tokens[:i+1] + tokens[i+2:]
                if tokens[i] not in [t.name for t in type_table]:
                    type_table.append(MyPtr(type_table, tokens[i]))

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
                raise Exception(f"Lexical error at token {i}: {tokens[i]}")

            # if new type
            if tokens[i - 1] == "struct":
                # print("it's new type!!!")
                index = findInTypeTableByName(type_table, tokens[i])
                if index == None:
                    type_table.append(MyType(tokens[i], -1))
                    type_table.append(MyType('const ' + tokens[i], -1, isConst=True))
            # if ptr

            print("it's variable!!!")
            # if type before var declaration
            index = findInTableByName(type_table, tokens[i])
            if index != None:
                i += 1
                continue

            # if not declaration
            if findInTypeTableByName(type_table, tokens[i - 1]) is None:
                if tokens[i] not in [var.name for var in vars_table]:
                    raise Exception(f"Lexical error at token {i} ({tokens[i]}): what's this")
                i += 1
                continue

            var = find_var_by_name_and_scope(vars_table, tokens[i], scope_starts[-1])

            if var is not None:
                if var.scopeStart == scope_starts[-1]:
                    raise Exception(f'Semantic error at token {i}: double delcaration of var {var.name}')
            if isStruct:
                i += 1
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

        i += 1

    return (type_table, vars_table, literals_table, tokens)


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
            f'token {new_tokens[i]} scopestart {scope_starts["{}"][-1]}'
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


def clearStupidStructs(tokens) -> str:
    i: int = 0
    scope_start: list[int] = [0]
    print(len(tokens))
    while i < len(tokens):
        if tokens[i] == 'struct' and scope_start[-1] != 0:
            tokens = tokens[:i] + tokens[i+1:]
        if tokens[i] == '{':
            scope_start.append(i)
        if tokens[i] == '}':
            scope_start.pop()
        i += 1
        print(i)
    
    return tokens


def analyze(text: str):
    tokens = separate(text)
    tokens = clearStupidStructs(tokens)
    i = 0
    for token in tokens:
        print(f'{i} {token}')
        i += 1
    (type_table, vars_table, literals_table, tokens) = createTables(tokens)

    for var in vars_table:
        print(f"{var.mytype.name} {var.name} {var.scopeStart}")

    for t in type_table:
        print(f'{t.id} {t.name}')
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
    print("table of literals(l):\n", file=file)
    for l in literals_table:
        print(f"{l.id} {l.mytype.name} {l.text}", file=file)

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

    sub = new_text.find("#include")
    while sub != -1:
        newline = new_text[sub:].find("\n") + sub + 1
        new_text = new_text[0:sub] + new_text[newline:]
        sub = new_text.find("#include")

    sub = new_text.find('printf')
    while sub != -1:
        newline = new_text[sub:].find("\n") + sub + 1
        new_text = new_text[0:sub] + new_text[newline+1:]
        sub = new_text.find("printf")

    sub = new_text.find('malloc')
    while sub != -1:
        pos = sub + 1
        st = 0
        flag = True
        while st != 0 or flag:
            print(new_text[pos])
            if new_text[pos] == '(':
                flag = False
                st+=1
            if new_text[pos] == ')':
                st -= 1
            pos += 1
        new_text = new_text[:sub - 1] + new_text[pos -1:]
        sub = new_text.find('malloc')

    sub = new_text.find("free")
    while sub != -1:
        newline = new_text[sub:].find("\n") + sub + 1
        new_text = new_text[0:sub] + new_text[newline + 1 :]
        sub = new_text.find("free")

    return new_text
