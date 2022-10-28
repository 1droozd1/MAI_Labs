#include <stdio.h>
#include "massive.h"

int main(int argc, const char * argv[]) {

    map *v = NULL;
    
    bool sorted = false;
    bool working = true;

    while(working) {
        int input = 0;
        char h[] = "";
        while(input == 0){
            printf("Working with map. Enter code of command.\nCode 1: Create map\t\tCode 2: Add unit\t\tCode 3: Print map\nCode 4: Generate map\t\tCode 5: Sort map\t\tCode 6: Search\nCode 7: End of programm\nEnter: ");
            scanf("%s", h);

            if(strcmp("1",h) == 0){
                input = 1;
            }else if(strcmp("2",h) == 0) {
                input = 2;
            }else if(strcmp("3",h) == 0) {
                input = 3;
            }else if(strcmp("4",h) == 0) {
                input = 4;
            }else if(strcmp("5",h) == 0) {
                input = 5;
            }else if(strcmp("6",h) == 0) {
                input = 6;
			}else if(strcmp("7",h) == 0) {
                input = 7;
            }else {
                printf("Incomprehensible input\n");
            }
        }
        switch(input){
            case 1:
            {
                if(v != NULL)
                    printf("Map already exists\n");
                else {
                    v = map_create();
                    sorted = false;
                    printf("Map created\n");
                }
                break;
            }
            case 2:
            {
                if(v != NULL){
                    char value[MAXLEN] = "";
                    int key = 0;
                    printf("Enter  key of new unit: ");
                    scanf("%d", &key);
                    sorted = false;
                    printf("Enter  value of new unit: ");
                    scanf("%s", value);
                    
                    map_add(v, key, value);
                }
                else printf("List not exists\n");
                break;
            }
            case 3:
            {
                if(v != NULL) {
                    map_print(v);
                }
                else {
                    printf("Map not exists\n");
                }
                break;
            }
            case 4: {
                map_generate(v);
                sorted = false;
                break;
            }
            case 5:
                if(v != NULL) {
                    map_print(v);
                    map_sort(v);
                    sorted = true;
                    map_print(v);
                    printf("Map sorted\n");
                }
                else {
                    printf("Map not exists\n");
                }
                break;
            case 6:
                if(v != NULL && sorted) {
                    int key = 0;
                    printf("Enter  key of unit: ");
                    scanf("%d", &key);
                    unit *u = search(v, key, 0, v->size-1);
                    if(u == NULL) {
                        printf("Not found\n");
                    }
                    else printf("Unit value %s\n", u->v);
                   
                }
                else {
                    printf("Map not exists or not sorted\n");
                }
                break;
			case 7: {
                printf("End program\n");
                working = false;
				sorted = true;
                break;
			}
        }
    }
    return 0;
}