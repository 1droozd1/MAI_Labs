#include "massive.h"
//valgrind --tool=memcheck ./a.out

bool isInt(const char*str) {
    while(*str)  {
        if((*str< '0' || *str > '9') && *str != '-')
            return false;
        *str++;
    }
    return true;
}

bool contain(int n, int a[]) {
    for(int i = 0; i < 14; i++) {
        if(a[i] == n) return true;
    }
    return false;
}


void map_sort_xor(map *m, int start, int end) {
    int i = start;
    int j = end;
    int mid = m->units[(start+end)/2]->k;
    
    do {
        while(m->units[i]->k < mid) i++;
        while(m->units[j]->k > mid) j--;
        
        if(i <= j) {
            if (m->units[i]->k > m->units[j]->k) {
                unit *a = m->units[i];
                m->units[i] = m->units[j];
                m->units[j] = a;
            }
            i++;
            j--;
        }
    }while (i <= j);
    
    if( i < end) map_sort_xor(m, i, end);
    if(start < j) map_sort_xor(m, start, j);
}

map * map_create(){
    map *m = malloc(sizeof(map));
    m->max_size = 14;
    m->size = 0;
    m->units = (unit**)malloc(sizeof(unit*) * m->max_size);
    return m;
}

void map_add(map *m, int k, char *v) {
    if(m->size < m->max_size){
        unit *u = malloc(sizeof(unit));
        u->k = k;
        strcpy(u->v, v);
        m->units[m->size] = u;
        m->size++;
    } else {
        printf("Map is full!\n");
    }
}

void map_sort(map *m) {
    map_sort_xor(m, 0, m->size-1);
}

void map_generate(map *m) {

    char surnames[][MAXLEN] = {"У лукоморья дуб зелёный;", "Златая цепь на дубе том:", "И днём и ночью кот учёный", 
	"Всё ходит по цепи кругом;", "Идёт направо — песнь заводит,", "Налево — сказку говорит.", "Там чудеса: там леший бродит,", 
	"Русалка на ветвях сидит;", "Там на неведомых дорожках", "Следы невиданных зверей;", "Избушка там на курьих ножках", 
	"Стоит без окон, без дверей;", "Там лес и дол видений полны;"};

    int a[14];
    for(int i = 0; i < 14; i++) {
        a[i] = -1;
    }
    int j = 0;
    for(int i = 0; i<m->max_size-1; i++) {
        int r = rand()%13;
        while(contain(r, a)) {
            r = rand()%13;
        }
        a[j] = r;
        j++;
        map_add(m, r, surnames[r]);
    }
}

void map_print(map *m) {
    for(int i = 0; i < m->size; i++) {
		printf("%d: %s\n", m->units[i]->k, m->units[i]->v);
	}
    printf("\n");
}

unit * search(map *m, int key, int left, int right) {
    int mid = (right + left) / 2;
	if(left > right) {
    	return NULL;
	} else if(m->units[mid]->k < key) {
        return search(m, key, mid+1, right);
    } else if(m->units[mid]->k > key) {
        return search(m, key, left, mid-1);
    } if(m->units[mid]->k == key) {
        return m->units[mid];
    }
   
    return NULL;
}