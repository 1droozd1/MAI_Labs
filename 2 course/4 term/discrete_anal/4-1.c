#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LINE_LENGTH 100

struct pair {
    char *key;
    char *value;
};

struct hashtable {
    struct pair **pairs;
    int size;
};

struct hashtable *create_hashtable(int size) {
    struct hashtable *ht = malloc(sizeof(struct hashtable));
    ht->pairs = malloc(sizeof(struct pair*) * size);
    ht->size = size;
    
    for (int i = 0; i < size; i++) {
        ht->pairs[i] = NULL;
    }
    
    return ht;
}

void free_hashtable(struct hashtable *ht) {
    for (int i = 0; i < ht->size; i++) {
        if (ht->pairs[i] != NULL) {
            free(ht->pairs[i]->key);
            free(ht->pairs[i]->value);
            free(ht->pairs[i]);
        }
    }
    
    free(ht->pairs);
    free(ht);
}

int hash_function(struct hashtable *ht, const char *key) {
    int sum = 0;

    for (int i = 0; i < strlen(key); i++) {
        sum += key[i];
    }

    return sum % ht->size;
}

void insert(struct hashtable *ht, char *key, char *value) {
    struct pair *p = malloc(sizeof(struct pair));
    p->key = strdup(key);
    p->value = strdup(value);
    
    int index = hash_function(ht, key);
    
    while (ht->pairs[index] != NULL) {
        index++;
        index %= ht->size;
    }
    
    ht->pairs[index] = p;
}

char *get(struct hashtable *ht, const char *key) {
    int index = hash_function(ht, key);
    int i = 0;

    while (ht->pairs[index] != NULL && i < ht->size) {
        if (strcmp(ht->pairs[index]->key, key) == 0) {
            return ht->pairs[index]->value;
        }

        index++;
        index %= ht->size;
        i++;
    }

    return NULL;
}

int main() {
    char line[MAX_LINE_LENGTH];
    char *day, *month, *year, *value;
    struct hashtable *ht = create_hashtable(100);

    while (fgets(line, MAX_LINE_LENGTH, stdin) != NULL) {
        // Разбиваем строку на день, месяц, год и значение
        day = strtok(line, ".");
        month = strtok(NULL, ".");
        year = strtok(NULL, "\t");
        value = strtok(NULL, "\n");

        // Формируем ключ в виде строки "day.month.year"
        char key[MAX_LINE_LENGTH];
        snprintf(key, MAX_LINE_LENGTH, "%s.%s.%s", day, month, year);

        // Добавляем пару ключ-значение в хеш-таблицу
        insert(ht, key, value);
    }

    // Проверяем, что данные добавлены в хеш-таблицу
    char *val = get(ht, "01.02.2008");
    printf("Value for key '01.02.2008': %s\n", val);

    // Очищаем хеш-таблицу
    free_hashtable(ht);

    return 0;
}
