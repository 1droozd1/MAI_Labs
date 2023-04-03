#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/*
Если в таблице могут существовать полностью одинаковые даты, то мы можем использовать механизм цепочек для обработки коллизий. 
Когда мы добавляем элемент в таблицу, мы будем проверять, есть ли уже элемент с таким же ключом (т.е. датой), и если есть, то мы 
добавляем новый элемент в конец списка, связанного с этим ключом.
*/

#define MAX_TABLE_SIZE 10000

typedef struct {
    char key[11];  // дата в формате day.month.year + '\0'
    char value[256];
} TableEntry;

typedef struct {
    TableEntry* entries[MAX_TABLE_SIZE];
} HashTable;

unsigned long hash_function(const char* str) {
    unsigned long hash = 5381;
    int c;

    while ((c = *str++)) {
        hash = ((hash << 5) + hash) + c; /* hash * 33 + c */
    }

    return hash % MAX_TABLE_SIZE;
}

void add_to_table(HashTable* table, const char* key, const char* value) {
    // вычисляем хеш для ключа (даты)
    unsigned long hash = hash_function(key);

    // проверяем, есть ли уже элемент с таким же ключом (датой)
    TableEntry* entry = table->entries[hash];
    while (entry != NULL) {
        if (strcmp(entry->key, key) == 0) {
            // нашли элемент с таким же ключом, добавляем новое значение в конец списка
            strcat(entry->value, "\n");
            strcat(entry->value, value);
            return;
        }

        entry = entry->next;
    }

    // создаем новый элемент и добавляем его в начало связанного списка для этого ключа
    TableEntry* new_entry = (TableEntry*)malloc(sizeof(TableEntry));
    strcpy(new_entry->key, key);
    strcpy(new_entry->value, value);
    new_entry->next = table->entries[hash];
    table->entries[hash] = new_entry;
}

const char* get_from_table(const HashTable* table, const char* key) {
    // вычисляем хеш для ключа (даты)
    unsigned long hash = hash_function(key);

    // ищем элемент с таким же ключом (датой) в связанном списке для этого хеша
    TableEntry* entry = table->entries[hash];
    while (entry != NULL) {
        if (strcmp(entry->key, key) == 0) {
            return entry->value;
        }

        entry = entry->next;
    }

    return NULL;  // элемент не найден
}
/*Обратите внимание на то, что мы добавляем новое значение в конец строки значения элемента, разделяя его символом переноса строки. 
При получении элемента из таблицы мы возвращаем всю строку значений, разделенных символами переноса строки. Таким образом, в связанном 
списке для каждой даты мы можем хранить любое количество значений.*/