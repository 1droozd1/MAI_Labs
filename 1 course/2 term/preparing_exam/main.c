#include "sort.h"

int main()
{
    int num;
    printf("amount of numbers: \n");
    scanf("%d", &num);

    int *massive;
    massive = (int*) malloc(num * sizeof(int));
    srand(time(NULL));

    for (int i = 0; i < num; i++) {
        massive[i] = rand() % 100;
    }

    for (int i = 0; i < strlen(massive) - 1; i++) {
        printf("%d ", massive[i]);
    }
    printf("\n");

    bubble_sort(*massive);

    free(massive);

}