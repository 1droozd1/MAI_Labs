#include "sort.h"

void swap(int a, int b)
{
    int n;

    n = a;
    a = b;
    b = n;
}

void print_mas(int *massive)
{
    for (int i = 0; i < strlen(massive) - 1; i++) {
        printf("%d ", massive[i]);
    }
    printf("\n");
}

void bubble_sort(int *list)
{
    print_mas(*list);

    int listLength = strlen(list);

    while(listLength--)
	{
		bool swapped = false;
		
		for(int i = 0; i < listLength; i++)
		{
			if(list[i] > list[i + 1])
			{
				swap(list[i], list[i + 1]);
				swapped = true;
			}
		}
		
		if(swapped == false)
			break;
	}

    print_mas(list);

}