/*Задание: двухсторонний линейный список с барьерным элементом,
а также добавить функцию: добавления в список элементов переданного значения до нужного размера списка
*/
#include "list.h"


int main(int argc, const char * argv[]) {
    list *v = NULL;
    
    bool working = true;
    while(working) {
        int input = 0;
        char h[] = "";
        while(input == 0) {
            printf("Working with list. Enter code of command.\nCode 1: Create list\t\tCode 2: Add unit\t\tCode 3: Delete unit\nCode 4: Print list\t\tCode 5: List length\t\tCode 6: Expand list\nCode 7: Exit\t\t\tCode 8: Random int List\nEnter: ");
            scanf("%s", h);
            if(strcmp("1",h) == 0){
                input = 1;
            }
            else if(strcmp("2",h) == 0) {
                input = 2;
            }
            else if(strcmp("3",h) == 0) {
                input = 3;
            }
            else if(strcmp("4",h) == 0) {
                input = 4;
            }else if(strcmp("5",h) == 0) {
                input = 5;
            }else if(strcmp("6",h) == 0) {
                input = 6;
            }else if(strcmp("7",h) == 0) {
                input = 7;
            }else if(strcmp("8",h) == 0) {
                input = 8;
            }else {
                printf("Wrong input\n");
            }
        }
        switch(input) {
            case 1:
            {
                if(v != NULL) {
                    printf("List already exists\n");
                } else {
                    v = create_list();
                    printf("List created\n");
                }
                break;
            }
            case 2:
            {
                if (v != NULL) {

                    char value[MAXLEN] = "";
                    printf("Enter  value of new unit: ");
                    scanf("%s", value);
                    add_list(v, value);
                    printf("Unit created\n");
                   
                } else {
                    printf("List not exists\n");
                }
                break;
            }
            case 4:
            {
                if(v != NULL) {
                    print_list(v);
                }
                else {
                    printf("List not exists\n");
                }
                break;
            }
            case 3: {
                if(v != NULL) {
                    char value[MAXLEN] = "";
                    
                    printf("Enter  value of unit, that you want to delete: ");
                    scanf("%s", value);
                    
                   
                        delete_list(v, value);
                        printf("Unit deleted\n");
                   
                }
                else {
                    printf("List not exists\n");
                }
                break;
            }
            case 5:
                if(v != NULL) {
                    printf("List length %d\n", len_list(v));
                }
                else {
                    printf("Matrix not exists\n");
                }
                break;
            case 6:
                if(v != NULL) {
                    char value[100] = "";
                    char k[100] = "";
                    
                    printf("Enter  value of units: ");
                    scanf("%s", value);
                    
                    printf("Enter  new list size: ");
                    scanf("%s", k);
                    
                    if(isInt(k)){
                        expand_list(v, value, atoi(k));
                    } else printf("Not a number\n");
                }
                else {
                    printf("List not exists\n");
                }
                break;
            case 7:
                printf("End program\n");
                working = false;
                break;
            
            case 8:
            {
                printf("Random adding\n");
                printf("Write amount of numbers in list\n");
                if (v != NULL) {
                    int n;
                    scanf("%d", &n);
                    printf("%d", n);

                    for (int i = 0; i < n; i++) {
                        char value[MAXLEN];
                        sprintf(value, "%d", rand() % 100);
                        add_list(v, value);
                    }

                    printf("Units created\n");
                } else {
                    printf("List not exists\n");
                }
                break;
            }
        }
    }
    return 0;
}