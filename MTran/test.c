int func(int a, int b)
{
    b = a + b;

    return b;
}

char f()
{
    float j;
    return 3.5f;
}

int main(){
    char a = '9';
    int b = 7;
    // func(a, &a);
    // a = 9;
    // const int* ptr = &a;
    //*ptr = 78;
    // j = 3.5f;

    int* name;
    int *name2;

    a = (7 + b) * (3 / 8 + 7);
    while (56 - 7 > 8){
        ++a;
    }
    while (5 || 8 && a || b)
        ++b;
    int c =9;
    for (c = 0; c < 9; ++c){
        ++c;
    }
    c=10;
    for (c = 0;;){
        ++c;
    }
    for (;;){
        ++a;
    }
    if (a > 9 || b < 7){
        ++a;
    }
    else
        --a;
    
    a = func(4, b + 5);

    char t = 'a';
    char* str = "str";
    *name2 = (78);
    // int** n = 34;


    return a;
}
// comment at the end
/*
made it multiline
*/