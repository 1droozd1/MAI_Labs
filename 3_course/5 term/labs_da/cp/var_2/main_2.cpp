#include <iostream>
#include <vector>
#include <cmath>
#include <algorithm>
#include <string>

using namespace std;

struct Vert {
  int x;
  int y;  
};

int heuristic(const Vert &start, const Vert &end) {
  return abs(start.x - end.x) + abs(start.y - end.y);
}

int A (const Vert &start, const Vert &end, vector<vector<int>>& grid, int n, int m, vector<vector<int>> &cost, vector<vector<int>> &vis_ver, vector<vector<Vert>> &vertex) {
  cost[start.x][start.y] = 0;
  int pos = 0;
  vertex[pos].push_back(start);
  
  int prev;
  Vert current, v;

  int dx[4] = {-1, 0, 1, 0};
  int dy[4] = {0, 1, 0, -1};

  while (!vertex[pos].empty() || !vertex[pos + 1].empty()) {
    if (vertex[pos].empty()) {
      pos += 1;
    }
    current = vertex[pos].back();
    vertex[pos].pop_back();
    
    if (vis_ver[current.x][current.y]) {
      continue;
      }

    if (current.x == end.x && current.y == end.y) {
      return cost[current.x][current.y];
      }


      vis_ver[current.x][current.y] = 1;
   

      prev = cost[current.x][current.y] + 1;

      for (int i = 0; i < 4; ++i) {
      v = current;
      v.x += dx[i];
      v.y += dy[i];
      if (v.x >= 1 && v.x <= n && v.y >= 1 && v.y <= m) {
        if (grid[v.x][v.y] == 1 && !vis_ver[v.x][v.y] && prev < cost[v.x][v.y]) {
          cost[v.x][v.y] = prev;
          if (heuristic(current, end) == heuristic(v, end) + 1) {
            vertex[pos].push_back(v);
          } else {
            vertex[pos + 1].push_back(v);
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
  int n, m;
  cin >> n >> m;
  string c;
  Vert start, end;
  vector<vector<int>> grid(n + 1, vector<int>(m + 1));
    vector<vector<int>> cost(n + 1, vector<int>(m + 1, 1e9));
    vector<vector<int>> vis_ver(n + 1, vector<int>(m + 1, 0));
    vector<vector<Vert>> vertex (n * m);

    for (int i = 1; i <= n; ++i) {
        cin >> c;
        for (int j = 1; j <= m; ++j) {
            grid[i][j] = (c[j - 1] == '#') ? 0 : 1;
        }
    }

    int q;
    cin >> q;
    for (int p = 0; p < q; ++p) {
      for (int i = 0; i < n*m; i++) {
        vertex[i].clear();
      }
        for (int i = 1; i <= n; ++i) {
            cost[i].assign(m + 1, 1e9);
            vis_ver[i].assign(m + 1, 0);
        }
        cin >> start.x >> start.y >> end.x >> end.y;
        cout << A(start, end, grid, n, m, cost, vis_ver, vertex) << "\n";
    }

  return 0;
}