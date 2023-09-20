#include <iostream>

using namespace std;

// Структура для хранения каждой даты и её индекса в исходных данных
struct item {
    int value[3]; // Хранение частей даты: [0] - день, [1] - месяц, [2] - год
    int ind; // Индекс строки с этой датой в исходных данных
};

// Глобальные константы для размеров массивов
const int strLen = 1e8;
const int vectorLen = 1e6;

// Функция для сортировки по одной части даты (дню, месяцу или году)
void Sort(item *array, int len, int p) {

    const int size = 10000; // Определяет размер массива для подсчета числа элементов с каждым ключом
    int count[size + 1] = { 0 }; // Массив для подсчета числа элементов с каждым ключом (все нули)
    item *res = new item[len]; // Временный массив, в котором будет храниться отсортированный результат

    for (int i = 0; i < len; i++) { // Подсчет элементов
        count[array[i].value[p]]++;
    }

    /* Этот цикл делает массив count кумулятивным, 
    что означает, что count[i] теперь хранит количество элементов, 
    которые меньше или равны i. */ 

    for (int i = 1; i <= size; i++) {
        count[i] += count[i - 1];
    }

    /* Этот цикл проходит по входному массиву в обратном порядке и 
    размещает каждый элемент в правильной позиции в массиве res, 
    используя информацию из массива count. */

    for (int i = len - 1; i >= 0; i--) {
        int key = array[i].value[p];
        int j = count[key] - 1;
        res[j] = array[i];
        count[key]--;
    }
    // Копирование отсортированных данных обратно
    for (int i = 0; i < len; i++) {
        array[i] = res[i];
    }

    delete[] res;
}

// Функция для сортировки массива дат с использованием поразрядной сортировки
void RadixSort(item *v, int len) {
    // Проходим по всем частям даты (день, месяц, год)
    for (size_t i = 0; i < 3; ++i) {
        Sort(v, len, i);
    }
}


int main() {

    char* data = new char[strLen];
    item* vector = new item[vectorLen];

    char c; // переменная для хранения текущего считанного символа
    int size = 0; // счетчик для числа обработанных дат

    item current = { 0 }; // текущий обрабатываемый элемент (дата)
    current.ind = 0; // начальный индекс для текущего элемента

    int t = 0; // счетчик для индекса текущего символа в массиве data
    int currentInd = 0; // индекс для текущей части даты (0 - день, 1 - месяц, 2 - год)
    char last = '\n'; // последний считанный символ (инициализирован как перевод строки)
    int f = 0; // счетчик цифр в текущей части даты

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
