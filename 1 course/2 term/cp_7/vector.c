#include "stdbool.h"
#include <stdio.h>
#include <stdlib.h>

#include "vector.h"


void vector_create(vector* v, int size) //определение размера созданного вектора
{
    v->size = size;
    v->data = (int*)malloc(sizeof(int) * v->size);
    v->elements_count = 0;
}

int size(vector* v)
{
    return v->size;
}

bool empty(vector* v)
{
    return v->size == 0;
}

void size_pp(vector* v)
{
    v->size++;
    v->data = realloc(v->data, sizeof(int) * v->size);
}

void push_back(vector* v, int value)
{
    if (v->size == v->elements_count) {
        size_pp(v);
    }
    v->data[v->elements_count++] = value;
}

void destroy(vector* v)
{
    v->size = 0;
    v->elements_count = 0;
    free(v->data);
}


//---------------------------------------------------------------------------------------------
//MATRIX PART
//---------------------------------------------------------------------------------------------


int el_count(char name[20])
{
    int a = 0;
    int count = 0;
    FILE* f;
    if ((f = fopen(name, "r")) == NULL) {
        printf("The file not exists\n");
        exit(1);
    }

    while(fscanf(f, "%d", &a) && !feof(f)) {
        count++;
    }
    fclose(f);
    return count + 1;
}

int lines_count(char name[20])
{
    int count = 0;

    FILE* f;
    if ((f = fopen(name, "r")) == NULL) {
        printf("The file not exists\n");
        exit(1);
    }
    
    while (!feof(f)) {
        if (fgetc(f) == '\n')
            count++;
    }
    fclose(f);
    return count + 1;
}

vector* matrix_input(vector* v)
{
    int a;
    char name[20];
    int n, m;

    vector_create(v, 1);
    scanf("%s", name);
    
    FILE* f = fopen(name, "r");
    if (f == NULL) {
        printf("The file not exists\n");
        exit(1);
    }
    n = lines_count(name);
    m = el_count(name) / n;

    int c[n][m];

    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            fscanf(f, "%d", &a);
            c[i][j] = a;
        }
    }
    int g = 0;
    for (int p = 0; p < n; p++) {
        int k = 0;
        for (int g = 0; g < m; g++) {
            if (c[p][g] != 0) {
                if (k == 0) {
                    push_back(v, p + 1);
                    k++;
                }
                push_back(v, g + 1);
                push_back(v, c[p][g]);
            }
        }
        if (k != 0) {
            push_back(v, 0);
        }
    }

    push_back(v, 0);
    push_back(v, n);
    push_back(v, m);
    fclose(f);
    return v;
}

void task_print(vector* v)
{
    if (v == NULL) {
        return;
    }
    printf("Matrix pattern placing\n");
    for (int i = 0; i < v->size - 2; i++) {
        printf("%d ", v->data[i]);
    }
    printf("\n");
}

void function(vector* v)
{
    printf("Lines with the most non-zero elements and the sum ot their elements:\n");
    int count = 0;
    int k = 0;
    vector a;
    vector* q = &a;
    if (v->data[0] == 0) {
        for (int r = 0; r < v->data[v->size - 2]; r++) {
            printf("%d 0\n", r + 1);
        }
        exit(0);
    }
    vector_create(q, v->data[v->size - 2]);
    
    for (int i = 0; i < v->size - 3; i++) {
        if (v->data[i] != 0) {
            count++;
        } else {
            q->data[k] = (count - 1) / 2;
            k++;
            count = 0;
        }  
    }
    vector s;
    vector* w = &s;
    int sum = 0;
    k = 0;
    vector_create(&s, v->data[v->size - 2]);
    for (int j = 0; j < v->size - 3;) {
        if (sum == 0) {
            sum = v->data[j + 2];
            if (v->data[j + 3] == 0) {
                j = j + 4;
                w->data[k] = sum;
                sum = 0;
                k++;
            } else {
                j = j + 3;
            }
        } else {
            sum = sum + v->data[j + 1];
            if (v->data[j + 2] == 0) {
                j = j + 3;
                w->data[k] = sum;
                sum = 0;
                k++;
            } else {
                j = j + 2;
            }
        }
    }
    int max = 0;
    for (int i = 0; i < q->size; i++) {
        if (max < q->data[i]) {
            max = q->data[i];
        }
    }
    for (int j = 0; j < s.size; j++) {
        if (q->data[j] == max) {
            printf("%d %d", j + 1, w->data[j]);
            printf("\n");
        }
    }
}

void natural_print(vector* v)
{
    int n = v->data[v->size - 2];
    int m = v->data[v->size - 1];
    int a[n][m];
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            a[i][j] = 0;
        }
    }
    if (v->size == 0) {
        return;
    }
    int l = 0;
    int k = 0;
    int count = 0;
    int value;
    for (int i = 0; i < v->size - 5;) {
        if (count == 0) {
            l = v->data[i] - 1;
            k = v->data[i + 1] - 1;
            value = v->data[i + 2];
            a[l][k] = value;
            count++;
            if (v->data[i + 3] == 0) {
                count--;
                i = i + 4;
            } else {
                i = i + 3;
            }
        } else {
            k = v->data[i] - 1;
            value = v->data[i + 1];
            a[l][k] = value;
            if (v->data[i + 2] == 0) {
                count--;
                i = i + 3;
            } else {
                i = i + 2;
            }
        }
    }
    printf("Natural form of matrix\n");
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < m; j++) {
            printf("%d ", a[i][j]);
        }
        printf("\n");
    }
}