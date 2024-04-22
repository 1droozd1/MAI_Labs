#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>

using namespace std;

struct Point {
    int coordX;
    int coordY;  
};

int distanceEstimate(const Point &origin, const Point &destination) {
    return abs(origin.coordX - destination.coordX) + abs(origin.coordY - destination.coordY);
}

int pathFinder(const Point &origin, const Point &destination, vector<vector<int>>& map, int width, int height, vector<vector<int>> &pathCost, vector<vector<int>> &explored, vector<vector<Point>> &frontier) {
    pathCost[origin.coordX][origin.coordY] = 0;
    int layer = 0;
    frontier[layer].push_back(origin);

    Point current, nextPoint;

    int dx[4] = {-1, 0, 1, 0};
    int dy[4] = {0, 1, 0, -1};

    while (!frontier[layer].empty() || !frontier[layer + 1].empty()) {
        if (frontier[layer].empty()) {
            layer += 1;
        }
        current = frontier[layer].back();
        frontier[layer].pop_back();

        if (explored[current.coordX][current.coordY]) {
            continue;
        }

        if (current.coordX == destination.coordX && current.coordY == destination.coordY) {
            return pathCost[current.coordX][current.coordY];
        }

        explored[current.coordX][current.coordY] = 1;
        int newPathCost = pathCost[current.coordX][current.coordY] + 1;

        for (int i = 0; i < 4; ++i) {

            nextPoint = current;
            nextPoint.coordX += dx[i];
            nextPoint.coordY += dy[i];

            if (nextPoint.coordX >= 1 && nextPoint.coordX <= width && nextPoint.coordY >= 1 && nextPoint.coordY <= height) {
                if (map[nextPoint.coordX][nextPoint.coordY] == 1 && !explored[nextPoint.coordX][nextPoint.coordY] && newPathCost < pathCost[nextPoint.coordX][nextPoint.coordY]) {
                    pathCost[nextPoint.coordX][nextPoint.coordY] = newPathCost;

                    if (distanceEstimate(current, destination) == distanceEstimate(nextPoint, destination) + 1) {
                        frontier[layer].push_back(nextPoint);
                    } else {
                        frontier[layer + 1].push_back(nextPoint);
                    }
                }
            }
        }
    }
    return -1;
}

int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);

    int width, height;
    cin >> width >> height;

    string lineInput;
    Point startPoint, endPoint;

    vector<vector<int>> map(width + 1, vector<int>(height + 1));
    vector<vector<int>> pathCost(width + 1, vector<int>(height + 1, 1e9));
    vector<vector<int>> explored(width + 1, vector<int>(height + 1, 0));
    vector<vector<Point>> frontier(width * height);

    for (int i = 1; i <= width; ++i) {
        cin >> lineInput;
        for (int j = 1; j <= height; ++j) {
            map[i][j] = (lineInput[j - 1] == '#') ? 0 : 1;
        }
    }

    int queries;
    cin >> queries;
    for (int q = 0; q < queries; ++q) {

        for (int i = 0; i < width * height; i++) {
            frontier[i].clear();
        }

        for (int i = 1; i <= width; ++i) {
            pathCost[i].assign(height + 1, 1e9);
            explored[i].assign(height + 1, 0);
        }

        cin >> startPoint.coordX >> startPoint.coordY >> endPoint.coordX >> endPoint.coordY;
        cout << pathFinder(startPoint, endPoint, map, width, height, pathCost, explored, frontier) << "\n";
    }

    return 0;
}
