#ifndef massive_h
#define massive_h

#include <stdio.h>
#include "stdlib.h"
#include "stdbool.h"
#include "string.h"

#define MAXLEN 1024

typedef struct unit {
    int k;
    char v[MAXLEN];
}unit;

typedef struct map{
    int max_size;
    int size;
    struct unit **units;
}map;

bool isInt(const char*str);
map * map_create();
unit * search(map *m, int key, int left, int right);
void map_add(map *m, int k, char *v);
void map_sort(map *m);
void map_generate(map *m);
void map_print(map *m);

#endif