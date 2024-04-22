#include <iostream> // Подключение библиотеки ввода-вывода
#include <vector> // Подключение библиотеки для использования вектора
#include <cmath> // Подключение математической библиотеки
#include <algorithm> // Подключение библиотеки алгоритмов
#include <string> // Подключение библиотеки строк

using namespace std; // Использование стандартного пространства имен

struct Point { // Определение структуры для точки
    int coordX; // Координата X
    int coordY; // Координата Y
};

// Функция для оценки расстояния между двумя точками (эвристика)
int distanceEstimate(const Point &origin, const Point &destination) {
    return abs(origin.coordX - destination.coordX) + abs(origin.coordY - destination.coordY);
}

// Основная функция поиска пути
int pathFinder(const Point &origin, const Point &destination, vector<vector<int>>& map, int width, int height, vector<vector<int>> &pathCost, vector<vector<int>> &explored, vector<vector<Point>> &frontier) {
    pathCost[origin.coordX][origin.coordY] = 0; // Инициализация начальной стоимости пути
    int layer = 0; // Текущий слой для исследования
    frontier[layer].push_back(origin); // Добавление начальной точки в фронтир

    Point current, nextPoint; // Текущая и следующая точки

    int dx[4] = {-1, 0, 1, 0}; // Смещения по X для соседних точек
    int dy[4] = {0, 1, 0, -1}; // Смещения по Y для соседних точек

    // Основной цикл поиска
    while (!frontier[layer].empty() || !frontier[layer + 1].empty()) {
        if (frontier[layer].empty()) {
            layer += 1; // Переход к следующему слою
        }
        current = frontier[layer].back(); // Получение текущей точки
        frontier[layer].pop_back(); // Удаление текущей точки из фронтира

        if (explored[current.coordX][current.coordY]) {
            continue; // Пропуск уже исследованной точки
        }

        // Проверка на достижение конечной точки
        if (current.coordX == destination.coordX && current.coordY == destination.coordY) {
            return pathCost[current.coordX][current.coordY]; // Возвращение стоимости пути
        }

        explored[current.coordX][current.coordY] = 1; // Отметка точки как исследованной
        int newPathCost = pathCost[current.coordX][current.coordY] + 1; // Вычисление новой стоимости пути

        // Обход соседних точек
        for (int i = 0; i < 4; ++i) {
            nextPoint = current; // Инициализация следующей точки
            nextPoint.coordX += dx[i]; // Смещение по X
            nextPoint.coordY += dy[i]; // Смещение по Y

            // Проверка на нахождение в пределах карты и отсутствие препятствия
            if (nextPoint.coordX >= 1 && nextPoint.coordX <= width && nextPoint.coordY >= 1 && nextPoint.coordY <= height) {
                if (map[nextPoint.coordX][nextPoint.coordY] == 1 && !explored[nextPoint.coordX][nextPoint.coordY] && newPathCost < pathCost[nextPoint.coordX][nextPoint.coordY]) {
                    pathCost[nextPoint.coordX][nextPoint.coordY] = newPathCost; // Обновление стоимости пути

                    // Определение слоя для следующей точки
                    if (distanceEstimate(current, destination)== distanceEstimate(nextPoint, destination) + 1) {
                        frontier[layer].push_back(nextPoint); // Добавление в текущий слой, если следующая точка ближе к цели
                    } else {
                        frontier[layer + 1].push_back(nextPoint); // Иначе добавление в следующий слой
                    }
                }
            }
        }
    }
    return -1; // Возвращение -1, если путь не найден
}

int main() {
    ios::sync_with_stdio(0); // Отключение синхронизации C и C++ потоков ввода-вывода для ускорения
    cin.tie(0); // Отвязка потока cin от cout, позволяет их параллельное использование
    cout.tie(0); // Отвязка потока cout

    int width, height; // Переменные для хранения ширины и высоты карты
    cin >> width >> height; // Ввод ширины и высоты карты

    string lineInput; // Строка для ввода карты
    Point startPoint, endPoint; // Точки начала и конца

    // Инициализация карты и вспомогательных массивов
    vector<vector<int>> map(width + 1, vector<int>(height + 1));
    vector<vector<int>> pathCost(width + 1, vector<int>(height + 1, 1e9));
    vector<vector<int>> explored(width + 1, vector<int>(height + 1, 0));
    vector<vector<Point>> frontier(width * height);

    // Ввод карты
    for (int i = 1; i <= width; ++i) {
        cin >> lineInput;
        for (int j = 1; j <= height; ++j) {
            map[i][j] = (lineInput[j - 1] == '#') ? 0 : 1; // Заполнение карты, где 0 - препятствие, 1 - свободная клетка
        }
    }

    int queries; // Количество запросов
    cin >> queries; // Ввод количества запросов
    for (int q = 0; q < queries; ++q) {

        // Очистка фронтира и переинициализация вспомогательных массивов для каждого запроса
        for (int i = 0; i < width * height; i++) {
            frontier[i].clear();
        }

        for (int i = 1; i <= width; ++i) {
            pathCost[i].assign(height + 1, 1e9);
            explored[i].assign(height + 1, 0);
        }

        // Ввод начальной и конечной точек
        cin >> startPoint.coordX >> startPoint.coordY >> endPoint.coordX >> endPoint.coordY;
        // Вывод результата поиска пути
        cout << pathFinder(startPoint, endPoint, map, width, height, pathCost, explored, frontier) << "\n";
    }

    return 0; // Конец программы
}

