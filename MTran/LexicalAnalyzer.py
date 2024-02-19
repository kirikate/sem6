import re


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


class MyType:
    def __init__(self, name, **kwargs):
        self.name = name
        for key, value in kwargs:
            self.__dict__[key] = value


class Ptr(MyType):
    def __init__(self, mytype: type, level: int):
        MyType.__init__(self, mytype.Name + "*" * level)
        self.pointersTo = mytype
        self.level = level


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


def analyze(text: str):
    # print(text)
    tokens = separate(text)
    for token in tokens:
        print(token)


if __name__ == "__main__":
    # print("hui")
    file = open("test.c")
    text: str = file.read()
    file.close()
    analyze(text)
