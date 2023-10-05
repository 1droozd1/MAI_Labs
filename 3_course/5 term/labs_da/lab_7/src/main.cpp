#include <iostream>
#include <vector>

using namespace std;

int main() {
    int n;
    cin >> n;

    vector<int> cost(n + 1, 0);  // Массив для хранения стоимостей преобразования чисел от 1 до n
    vector<int> prevAction(n + 1, 0);  // Массив для хранения предыдущего действия

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

    cout << cost[n] << endl;

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

    // Выводим последовательность действий в обратном порядке
    for (int i = 0; i <= actions.size() - 1; i++) {
        cout << (actions[i] == -1 ? "-1" : (actions[i] == 2 ? "/2" : "/3")) << " ";
    }
    cout << endl;

    return 0;
}