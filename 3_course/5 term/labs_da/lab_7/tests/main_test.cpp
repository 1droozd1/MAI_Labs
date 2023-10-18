#include <iostream>
#include <vector>
#include <fstream>
#include <chrono>

using namespace std;

int main() {
    ifstream input("/Users/dr0ozd/coding/MAI_Labs/3_course/5 term/labs_da/lab_7/tests/test_data/test10.txt"); // Чтение входных данных из файла input.txt
    ofstream output("output.txt", ios::app); // Запись результата в файл output.txt

    int n;
    input >> n;

    vector<int> cost(n + 1, 0);  // Массив для хранения стоимостей преобразования чисел от 1 до n
    vector<int> prevAction(n + 1, 0);  // Массив для хранения предыдущего действия

    // Засекаем время выполнения начиная с этой точки
    auto start_time = chrono::high_resolution_clock::now();

    for (int i = 2; i <= n; i++) {
        cost[i] = cost[i - 1] + i;  // Начальная стоимость - вычитание 1
        prevAction[i] = 1;  // 1 представляет вычитание 1
        if (i % 2 == 0 && cost[i / 2] + i < cost[i]) {
            cost[i] = cost[i / 2] + i;  // Если деление на 2 дешевле
            prevAction[i] = 2;  // 2 представляет деление на 2
        }
        if (i % 3 == 0 && cost[i / 3] + i < cost[i]) {
            cost[i] = cost[i / 3] + i;  // Если деление на 3 дешевле
            prevAction[i] = 3;  // 3 представляет деление на 3
        }
    }

    // Восстанавливаем последовательность действий
    vector<int> actions;
    int num = n;
    while (num != 1) {
        if (prevAction[num] == 1) {
            actions.push_back(-1);
            num--;
        } else if (prevAction[num] == 2) {
            actions.push_back(2);
            num /= 2;
        } else if (prevAction[num] == 3) {
            actions.push_back(3);
            num /= 3;
        }
    }

    // Засекаем время выполнения в этой точке
    auto end_time = chrono::high_resolution_clock::now();
    chrono::duration<double> execution_time = end_time - start_time;

    // Записываем время выполнения в файл output.txt
    output << n << " Execution Time: " << execution_time.count() << " seconds" << endl;

    return 0;
}
