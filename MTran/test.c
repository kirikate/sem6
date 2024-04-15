int func(int a, int b)
{
    b = a + b;

    return b;
}

char f()
{
    return 3.5f;
}

int main(){
    char a;
    int b = 7;

    int* name;
    int *name2;

    a = (7 + b) * (3 / 8 + 7);
    while (56 - 7 > 8){
        ++a;
    }
    while (5 || 8 && a || b)
        ++b;

    for (int c = 0; c < 9; ++c){
        ++c;
    }
    for (int c = 0;;){
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
    
    func(a, b);
    a = func(4, b + 5);

    char t = 'a';
    char* str = "str";
    *name2 = (78);
    int** n = name;


    return a;
}
// comment at the end
/*
made it multiline
*/