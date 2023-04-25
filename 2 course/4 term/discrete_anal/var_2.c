#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_LENGTH 64
#define MAX_KEY_LENGTH 11
#define MAX_DIGITS 4
#define MAX_COUNT 1000000

typedef struct {
    int day;
    int month;
    int year;
    char key_def[MAX_KEY_LENGTH];
} Date;

typedef struct {
    Date key;
    char value[MAX_LENGTH+1];
} Pair;

int count[MAX_COUNT];

void counting_sort(Pair* pairs, int n, int digit) {

    int i, j, k;
    memset(count, 0, sizeof(count));
    for (i = 0; i < n; i++) {
        switch (digit) {
            case 1: k = pairs[i].key.day; break;
            case 2: k = pairs[i].key.month; break;
            case 3: k = pairs[i].key.year; break;
        }
        count[k]++;
    }
    for (i = 1; i < MAX_COUNT; i++) {
        count[i] += count[i-1];
    }
    Pair* tmp = malloc(n * sizeof(Pair));
    for (i = n-1; i >= 0; i--) {
        switch (digit) {
            case 1: k = pairs[i].key.day; break;
            case 2: k = pairs[i].key.month; break;
            case 3: k = pairs[i].key.year; break;
        }
        tmp[--count[k]] = pairs[i];
    }
    for (i = 0; i < n; i++) {
        pairs[i] = tmp[i];
    }
    free(tmp);
}

void radix_sort(Pair* pairs, int n) {
    int i;
    for (i = 1; i <= MAX_DIGITS; i++) {
        counting_sort(pairs, n, i);
    }
}

int main() {

    int capacity = 10; // начальная емкость массива
    int size = 0; // текущее количество элементов в массиве
    Pair* pairs = (Pair*) malloc(capacity * sizeof(Pair)); // выделение памяти под динамический массив

    int i = 0;

    while (scanf("%s\t%s", pairs[i].key.key_def, pairs[i].value) != EOF) {

        if (size == capacity) {
            // увеличиваем емкость массива в два раза
            capacity *= 2;
            pairs = (Pair*) realloc(pairs, capacity * sizeof(Pair));
        }

        sscanf(pairs[i].key.key_def, "%d.%d.%d", &pairs[i].key.day, &pairs[i].key.month, &pairs[i].key.year);

        // увеличиваем счетчик пар
        i++;
    }

    radix_sort(pairs, i);

    for (int j = 0; j < i; j++) {
        
        if (strlen(pairs[j].value) > 0) {
            printf("%s\t%s\n", pairs[j].key.key_def, pairs[j].value);
        }
        
        //printf("%s\t%s\n", pairs[j].key.key_def, pairs[j].value);
    }

    free(pairs);
    return 0;
}

/*
1.1.1	n399tann9nnt3ttnaaan9nann93na9t3a3t9999na3aan9antt3tn93aat3naatt
01.02.2008	n399tann9nnt3ttnaaan9nann93na9t3a3t9999na3aan9antt3tn93aat3naat
1.1.1	n399tann9nnt3ttnaaan9nann93na9t3a3t9999na3aan9antt3tn93aat3naa
01.02.2008	n399tann9nnt3ttnaaan9nann93na9t3a3t9999na3aan9antt3tn93aat3na
*/