#include "stdio.h"
#include "stdlib.h"
#include "fun.h"

void swap(int* a, int* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

extern os_int *Sort(int* array) {
    int size = sizeof(array) / sizeof(array[0]);
    int i, j;
    int tmp;
    for (i = 1; i < size; i++) {
        for (j = 1; j < size; j++) {
            if (array[j] > array[j-1]) {
                tmp = array[j];
                array[j] = array[j-1];
                array[j-1] = tmp;
            }
        }
    }
}

extern os_int *GCD(int x, int y) {
    while (y > 0) {
        if (x >= y) {
            x = x % y;
        }
        swap(&x, &y);
    }
    return x;
}