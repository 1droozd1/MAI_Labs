#include "list.h"

bool isInt(const char*str) {
    while(*str)  {
        if((*str< '0' || *str > '9') && *str != '-')
            return false;
        *str++;
    }
    return true;
}

void add_unit_to_start(unit *u, unit *start){
        u->next = start->next;
        u->prev = start;
        start -> next -> prev = u;
        start -> next = u;
}


list * create_list() { //создание и выделение памяти под список l
    list *l = malloc(sizeof(list));
    l->border = malloc(sizeof(unit));
    
    strcpy(l->border->value, "");
    l->border->next = NULL;
    l->border->prev = NULL;
    return l;
}

void add_list(list *l, char *value) { //добавление нового элемента в unit
    unit *u = malloc(sizeof(unit));
    strcpy(u->value, value);

    if(l->border->prev == NULL) {
        l->border->next = u;
        l->border->prev = u;
        u->next = l->border;
        u->prev = l->border;
        
    }
    else add_unit_to_start(u, l->border->prev);
}

void delete_list(list *l, char *value) { //удаление списка со значением value
    unit *curent = l->border->next;

    while(curent != l->border) {
        if(strcmp(curent->value, value) == 0){
            curent->prev->next = curent->next;
            curent->next->prev = curent->prev;
            curent->next = NULL;
            curent->prev = NULL;
            free(curent);
            break;
        }
        else {
            curent = curent->next;
        }
    }
}

int len_list(list *l) { //длина списка
    int count = 0;
    unit *curent = l->border->next;

    while (curent != l->border) {
        count++;
        curent = curent->next;
    }
    return count;
}

void expand_list(list *l, char *value, int k) { // добавление в список элементов переданного
                                                // значения до нужного размера списка
    if(k <= len_list(l)) {
        printf("List has k length or more\n");
    } else {
        int count = k - len_list(l);
        for(int i = 0; i < count; i++) add_list(l, value);
    }
}

void print_list(list *l) { // печать списка
    unit *curent = l->border->next;

    while (curent != l->border) {
        printf("%s ", curent->value);
        curent = curent->next;
    }
    printf("\n");
}
