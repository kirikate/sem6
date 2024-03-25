from LexicalAnalyzer import *
from SytaxAnalyzer import *


if __name__ == "__main__":
    # print("hui")
    file = open("test.c")
    text: str = file.read()
    file.close()
    text = clearComments(text)
    print(text)
    res = analyze(text)
