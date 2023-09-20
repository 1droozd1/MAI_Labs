#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<int> Zfunction(const string & s) {
    int n = s.size(); // Получаем размер строки
    vector<int> z (n, 0); // Инициализируем вектор Z-функции
    int l = -1, r = -1; // Инициализируем границы Z-блока
    z[0] = n; // Устанавливаем Z[0] равным размеру строки

    for (int i = 1; i < n; ++i) {
        if (i <= r) { 
            z[i] = min(r - i, z[i - l]);
        }

        while ( i + z[i] < n && s[z[i]] == s[i + z[i]]) {
            ++z[i]; // Увеличиваем z[i], если символы совпадают
        }

        if (i + z[i] > r) { // Обновляем границы Z-блока
            r = i + z[i];
            l = i;
        }
    }
    return z;
}


int main() {
    ios_base::sync_with_stdio(false);
    cout.tie(nullptr);
    cin.tie(nullptr); // Оптимизация ввода-вывода

    string pattern, text;
    cin >> text >> pattern; // Считываем текст и шаблон
    text = pattern + "$" + text; // Конкатенируем шаблон, разделитель и текст
    vector<int> zVector = Zfunction(text); // Вычисляем Z-функцию

    for (int i = 0; i < text.size(); ++i) {
        if (zVector[i] == pattern.size()) { // Нашли шаблон в тексте
            cout << i - pattern.size() - 1 << "\n"; // Выводим начальную позицию
        }
    }
    return 0;
}