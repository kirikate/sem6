#include <stdio.h>

// int func(int a, int b)
// {
//     b = a + b;

//     return b;
// }

// char f()
// {
//     float j;
//     return 3.5;
// }

// struct MyStruct
// {
//     int a;
//     float b;
// };

// int main(){
//     char a = '9';
//     int b = 7;
//     struct MyStruct obj;
//     obj.a = 56;
//     (&obj)->b = 3.89;
//     b = obj.a + 6;
//     // func(a, &a);
//     // a = 9;
//     // const int* ptr = &a;
//     //*ptr = 78;
//     // j = 3.5f;

//     int* name;
//     int *name2;

//     a = (7 + b) * (3 / 8 + 7);
//     while (56 - 7 > 8){
//         ++a;
//     }
//     while (5 || 8 && a || b)
//         ++b;
//     int c =9;
//     for (c = 0; c < 9; ++c){
//         ++c;
//     }
//     c=10;
//     for (c = 0;;){
//         ++c;
//     }
//     for (;;){
//         ++a;
//     }
//     if (a > 9 || b < 7){
//         ++a;
//     }
//     else
//         --a;
    
//     a = func(4, b + 5);

//     char t = 'a';
//     char* str = "str";
//     *name2 = (78);
//     // int** n = 34;


//     return a;
// }
// // comment at the end
// /*
// made it multiline
// */

int func(int a, int b)
{
    b = a + b;

    return b;
}

char f()
{
    float j;
    return 3.5;
}

struct MyStruct
{
    int a;
    float b;
};
int next = 45;

int rand()
{
    next = next * 1103515245 + 12345;
    return (int)(next / 65536) % 32768;
}


#include "stdio.h"
int main()
{
    int d[3][3][3];
    int e[3][3][3];
    int f[3][3][3];
    d[0][0][0] = 1;

    for(int i = 0; i < 3; ++i)
    {
        for(int j = 0; j < 3; ++j)
        {
            for(int k = 0; k < 3; ++k)
            {
                d[i][j][k] = rand() + 1;
                e[i][j][k] = rand() + 1;
                f[i][j][k] = rand() + 1;
            }
        }
    }
    // если первый больше 2 3 то первый умножаем на второй делим на третий
    // eckb 2> 1 3 то 2 = (2+3 ) * 1
    // 3 то 1 обнуляем а 2 = 3
    // и выводим
    int sd = 0;
    int se = 0;
    int sf = 0;
    for(int i = 0; i < 3; ++i)
    {
        sd += d[i][i][i];
        se += e[i][i][i];
        sf += f[i][i][i];
    }
    printf("first mass\n");
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            for (int k = 0; k < 3; ++k)
            {
                printf("%i ", d[i][j][k]);
            }
        }
    }
    printf("\n");

    printf("second mass\n");
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            for (int k = 0; k < 3; ++k)
            {
                printf("%i ", e[i][j][k]);
            }
        }
    }
    printf("\n");
    printf("third mass\n");
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            for (int k = 0; k < 3; ++k)
            {
                printf("%i ", f[i][j][k]);
            }
        }
    }
    printf("\n");
    if (sd >= se && sd >= sf)
    {
        printf("first scenar\n");
        for(int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                for (int k = 0; k < 3; ++k)
                {
                    d[i][j][k] = d[i][j][k] * e[i][j][k];
                    d[i][j][k] = d[i][j][k] / f[i][j][k];
                }
            }
        }
    }

    if (se >= sd && se >= sf)
    {
        printf("second scenar\n");

        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                for (int k = 0; k < 3; ++k)
                {
                    e[i][j][k] = f[i][j][k] + e[i][j][k];
                    e[i][j][k] = e[i][j][k] * d[i][j][k];
                }
            }
        }
    }

    if (sf >= sd && sf >= se)
    {
        printf("third scenar\n");
        for (int i = 0; i < 3; ++i)
        {
            for (int j = 0; j < 3; ++j)
            {
                for (int k = 0; k < 3; ++k)
                {
                    d[i][j][k] = 0;
                    e[i][j][k] = f[i][j][k];
                }
            }
        }
    }

    printf("RESULT------------\n");

    printf("first mass\n");
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            for (int k = 0; k < 3; ++k)
            {
                printf("%i ", d[i][j][k]);
            }
        }
    }
    printf("\n");

    printf("second mass\n");
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            for (int k = 0; k < 3; ++k)
            {
                printf("%i ", e[i][j][k]);
            }
        }
    }
    printf("\n");
    printf("third mass\n");
    for (int i = 0; i < 3; ++i)
    {
        for (int j = 0; j < 3; ++j)
        {
            for (int k = 0; k < 3; ++k)
            {
                printf("%i ", f[i][j][k]);
            }
        }
    }
    printf("\n");
     return 0;
}
