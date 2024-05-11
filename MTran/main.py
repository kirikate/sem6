from LexicalAnalyzer import *
from SyntaxAnalyzer import *


if __name__ == "__main__":
    # print("hui")
    file = open("test.c")
    text: str = file.read()
    file.close()
    text = clearComments(text)
    print(text)
    (tokens, type_table, vars_table, literals_table) = analyze(text)
    program = Program(tokens, type_table, vars_table, literals_table)
    program.ValidateTypes()
    program.execute()
    tostr = program.toString(0)
    file = open("res2.txt", "w")
    file.truncate()
    print(tostr, file=file)
    file.close()
