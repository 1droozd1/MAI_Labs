#include <iostream>

using namespace std;

struct item {
    int value[3];
    int ind;
};

const int strLen = 1e8;
const int vectorLen = 1e6;

void Sort(item *array, int len, int p) {

    const int size = 10000;
    int count[size + 1] = { 0 };
    item *res = new item[len];

    for (int i = 0; i < len; i++) {
        count[array[i].value[p]]++;
    }

    for (int i = 1; i <= size; i++) {
        count[i] += count[i - 1];
    }
    for (int i = len - 1; i >= 0; i--) {
        int key = array[i].value[p];
        int j = count[key] - 1;
        res[j] = array[i];
        count[key]--;
    }

    for (int i = 0; i < len; i++) {
        array[i] = res[i];
    }

    delete[] res;
}

// Sorts an array using the Radix Sort algorithm
void RadixSort(item *v, int len) {
    for (size_t i = 0; i <3; ++i) {
        Sort(v, len, i);
    }
}


int main() {

    char* data = new char[strLen];
    item* vector = new item[vectorLen];

    char c;
    int size = 0;

    item current = { 0 };
    current.ind = 0;

    int t = 0;
    int currentInd = 0;
    char last = '\n';
    int f = 0;

    while ((c = getchar_unlocked()) != EOF) {
        if (c == '\n') {
            if (last == '\n') {
                continue;
            }

            vector[size++] = current;
            current = { 0 };
            current.ind = t + 1;
            currentInd = 0;
            f = 0;
        }

        if (c == '.') {
            ++currentInd;
            f = 0;
            
        } else if (c >= '0' && c <= '9' && f < 4) {
            current.value[currentInd] = current.value[currentInd] * 10 + (c - '0');
            ++f;
        }

        if (c == '\t' || c == ' ') {
            f = 10;
        }

        data[t++] = c;
        last = c;
    }

    data[t] = '\n';

    RadixSort(vector, size);

    for (size_t i = 0; i < size; ++i) {
        size_t j = vector[i].ind;

        do {
            putchar_unlocked(data[j]);
        } while (data[j++] != '\n');
    }

    delete[] data;
    delete[] vector;
    return 0;
}
