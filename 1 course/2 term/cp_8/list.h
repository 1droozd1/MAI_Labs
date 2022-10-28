#ifndef LIST_H
#define LIST_H

#include <stdio.h>
#include <stdlib.h>
#include "stdbool.h"
#include "string.h"

#define MAXLEN 256

typedef struct unit {
    char value[MAXLEN];
    struct unit *next;
    struct unit *prev;
}unit;

typedef struct list {
    struct unit *border;
}list;



bool isInt(const char*str);
list * create_list();
void add_list(list * l, char *value);
void delete_list(list *l, char *value);
int len_list(list *l);
void expand_list(list *l, char *value, int k);
void print_list(list *l);

#endif