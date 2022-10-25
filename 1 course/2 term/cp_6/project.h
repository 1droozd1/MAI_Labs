#ifndef PROJECT_H
#define PROJECT_H

#include "stdio.h"
#include "stdlib.h"
#include "stdbool.h"
#include "string.h"
#include "time.h"
#define MAXCHAR 128

typedef struct test {
    char name[MAXCHAR];
    int score;
}test;

typedef struct Student{
    char surname[MAXCHAR];
    char initials[MAXCHAR];
    char sex[MAXCHAR];
    char group[MAXCHAR];
    struct test ** tests;
    int count;
}Student;

void adding_to_file();
int str_write(char * s, FILE *f);
int int_write(int * i, FILE *f);
int str_read(char * s, FILE *f);
int int_read(int *i, FILE *f);
int add_student(Student *s, FILE *f);
int add_test(test*t, FILE *f);
int get_student(Student *s, FILE *f);
int get_test(test *t, FILE *f);
void add_test_to_student(test *t, Student *s);

#endif