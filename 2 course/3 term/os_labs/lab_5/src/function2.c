#include "stdio.h"
#include "stdlib.h"
#include "fun.h"

void swap(int* a, int* b)
{
    int t = *a;
    *a = *b;
    *b = t;
}

int partition(int array[], int low, int high)
{
    int pivot = array[high];
    int i = (low - 1);
    for (int j = low; j <= high - 1; j++) {
        if (array[j] < pivot) {
            i++;
            swap(&array[i], &array[j]);
        }
    }
    swap(&array[i + 1], &array[high]);
    return (i + 1);
}

void quickSort(int* array, int low, int high)
{
    if (low < high) {
        int pi = partition(array, low, high);
        quickSort(array, low, pi - 1);
        quickSort(array, pi + 1, high);
    }
}

extern os_int *Sort(int* array)
{
    int n = sizeof(array) / sizeof(array[0]);
    int low = 0;
    int high = n - 1;

    quickSort(array, low, high);
}

extern os_int *GCD(int x, int y) {
    if (x > y) {
        swap_int(&x, &y);
    }
    for (int i = x; i > 1; --i) {
        if (x % i == 0 && y % i == 0) {
            return i;
        }
    }
    return 1;
}