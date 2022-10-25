#include "project.h"

#define MAXCHAR 128


int main()
{
    remove("BD.bin");

    FILE *f;

    if ((f = fopen("BD.bin", "wb")) == NULL) {
        printf("Error: can't open file\n");
        exit(1);
    }

    char surnames[][MAXCHAR] = {"Dubrovin", "Ivanov", "Sidorov", "Gorbunova", "Avdeeva", "Katucheva", "Kirilov", "Sokolov", "Baranov", "Makarov", "Sirov"};
    char initials[][MAXCHAR] = {"DV", "MD", "PV", "ES", "MS", "DG", "KA", "VV", "DS", "MM", "TO"};
    char sex[][MAXCHAR] = {"M", "W"};
    char group[][MAXCHAR] = {"107", "108", "109"};
    char exam[][MAXCHAR] = {"MATH", "RUS", "HISTORY", "PYTHON", "DICKR"};

    srand(time(NULL));

    int a[11] = { 0 };

    for (unsigned i = 0; i < 11; ++i) {
        unsigned j = rand() % (i + 1);
        a[i] = a[j];
        a[j] = i + 1;
    }

    for (int i = 0; i < 11; i++) {
        a[i] -= 1;
    }

    for(int i = 0; i < 11; i++) {
        
        Student *s = malloc(sizeof(Student));
       
        strcpy(s->surname, surnames[a[i]]);
        strcpy(s->initials, initials[rand()%11]);
        strcpy(s->sex, sex[rand()%2]);
        strcpy(s->group, group[rand()%3]);

        int count = rand()%4+1;

        for(int i = 0; i<count; i++) {
            test *t = malloc(sizeof(test));
            
            strcpy(t->name, exam[rand()%5]);

            t->score = rand()%6;
            if (t -> score == 0) {
                t -> score += 2;
            }
            if (t -> score == 1) {
                t -> score += 1;
            }
            add_test_to_student(t, s);
        }
        s->count = count;
        add_student(s, f);
    }
    
    fclose(f);
    return 0;
}