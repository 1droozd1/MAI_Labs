#include "deck.h"
#include "sort.c"



int main(int argc, char *argv[])
{
    int n, a;
    deque deck;
    deque_create(&deck);

    printf("Enter the deque size:\n");
    scanf("%d", &n);

    /*printf("Enter deque elements:\n");
    for (int i = 0; i < n; i++) {
	    scanf("%d", &a);
	    push_back(&deck, a);
    }*/

    for (int i = 0; i < n; i++) {
        a = rand() % 100;
        printf("%d ", a);
        push_back(&deck, a);
    }

    merge_sort(&deck);
    printf("\nSorted deque:\n");
    
    while(!empty(&deck)) {
	    printf("%d ", first_front(&deck));
	    pop_front(&deck);
    }
    printf("\n");
    return 0;
}