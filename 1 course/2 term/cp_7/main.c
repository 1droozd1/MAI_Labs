#include "vector.h"
#include <stdlib.h>

//Найти строку, содержащую наибольшее количество ненулевых элементов - напечатать ее номер и сумму


int main(int args, char argv[])
{
    vector *v = malloc(sizeof(vector));

    printf("Write file name:\n");

    matrix_input(v);
    task_print(v);
    natural_print(v);

    function(v);

    return 0;
}