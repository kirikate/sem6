#include "stdio.h"

struct MyStruct
{
    int f;
    float l;
}

int main()
{
    int a=5+4+6;
    int g = a+++5;
    float pi=3.14;
    for (int i = 0; i < 15; ++i){
        char a='b';
    }
    const char *b = "string string";
    print("%s", b);

    return 0;
}