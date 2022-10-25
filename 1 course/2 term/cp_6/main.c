#include "project.h"

void print_in_table()
{
    FILE *f;
    
    if ((f = fopen("BD.bin", "rb")) == NULL) {
        printf("Error: can't open file\n");
        exit(1);
    }
    fprintf(stdout, "+---------------+--------+---+----------+-----\n");
    fprintf(stdout, "|    Surname    |initials|sex|  group   |exams\n");
    Student s;
    while (get_student(&s, f) == 0) {
        fprintf(stdout, "+---------------+--------+---+----------+");
        if(s.tests != NULL) {
        for(int i = 0; i < s.count; i++) {
            for(int j = 0; j < strlen(s.tests[i]->name); j++) fprintf(stdout, "-");
            fprintf(stdout, "--+");
        }
        }
        fprintf(stdout, "\n");
        fprintf(stdout, "|%-15s|   %c.%c  | %s |%-10s|", s.surname, s.initials[0], s.initials[1], s.sex, s.group);
        if(s.tests != NULL) {
        for(int i = 0; i < s.count; i++) fprintf(stdout, "%s %d|", s.tests[i]->name, s.tests[i]->score);
        }
        fprintf(stdout, "\n");
            fprintf(stdout, "+---------------+--------+---+----------+");
        if(s.tests != NULL) {
        for(int i = 0; i < s.count; i++) {
            for(int j = 0; j < strlen(s.tests[i]->name); j++) fprintf(stdout, "-");
            fprintf(stdout, "--+");
        }
            fprintf(stdout, "\n");
        }
    }
    fclose(f);
}

void print_student(Student *s) {
    fprintf(stdout, "+---------------+--------+---+----------+");
    if(s->tests != NULL) {
    for(int i = 0; i < s->count; i++) {
        for(int j = 0; j < strlen(s->tests[i]->name); j++) fprintf(stdout, "-");
        fprintf(stdout, "--+");
    }
    }
    fprintf(stdout, "\n");
    fprintf(stdout, "|%-15s|   %c.%c  | %s |%-10s|", s->surname, s->initials[0], s->initials[1], s->sex, s->group);
    if(s->tests != NULL) {
    for(int i = 0; i < s->count; i++) fprintf(stdout, "%s %d|", s->tests[i]->name, s->tests[i]->score);
    }
    fprintf(stdout, "\n");
    fprintf(stdout, "+---------------+--------+---+----------+");
    if(s->tests != NULL) {
    for(int i = 0; i < s->count; i++) {
        for(int j = 0; j < strlen(s->tests[i]->name); j++) fprintf(stdout, "-");
        fprintf(stdout, "--+");
    }
        fprintf(stdout, "\n");
    }
}

int main(int argc, const char * argv[]) {

    print_in_table();

    FILE *f;
    if ((f = fopen("BD.bin", "rb")) == NULL) {
        printf("Error: can't open file\n");
        exit(1);
    }

    char p[20];
    printf("Write number of group:\n");
    fgets(p, 20, stdin);

    if (p[strlen(p) - 1] == '\n') {
        p[strlen(p) - 1] = '\0';
    }

    Student s;

    printf("That student: \n");
    int count = 0;
    while(get_student(&s, f) == 0) {
        if(strcmp(s.sex, "W") == 0 && strcmp(s.group, p) == 0) {
            int five_count = 0;
            for(int i = 0; i < s.count; i ++) {
                if(s.tests[i]->score == 5) {
                    five_count+=1;
                }
            }
            if(five_count == 1) {
                count+=1;
                if(true) print_student(&s);
            }
        }
    }

    fprintf(stdout, "Count of females with one five score in tests or exams: %d\n", count);
    fclose(f);

    return 0;
}