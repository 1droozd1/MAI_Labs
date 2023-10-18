#include <iostream>
#include <fstream>
#include <vector>
#include <math.h>
#include <chrono>

using namespace std;

int main() {
    ifstream inputFile("/Users/dr0ozd/coding/MAI_Labs/3_course/5 term/labs_da/lab_8/testing/tests/test10.txt");  // Открываем файл для чтения входных данных
    ofstream outputFile("output.txt", ios::app);  // Открываем файл для записи выходных данных
    auto start_time = chrono::high_resolution_clock::now();  // Засекаем начальное время выполнения
    
    long long nomin, money;
    inputFile >> nomin >> money;

    long long amount;
    inputFile >> amount;
    long long amount_def = amount;

    vector<long long> kol_money(nomin, 0);

    while (amount != 0) {
        if (amount - pow(money, nomin - 1) >= 0) {
            amount -= pow(money, nomin - 1);
            kol_money[nomin - 1] += 1;
        } else {
            nomin -= 1;
        }
    }

    // Засекаем время выполнения в этой точке
    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;

    // Записываем информацию о времени выполнения в отдельный файл
    outputFile << amount_def << " "<< execution_time.count() << endl;

    inputFile.close();  // Закрываем файлы
    outputFile.close();

    return 0;
}