def A(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

m, n = map(int,input().split())
mapp = []

for i in range(m):
    mapp.append(list(input()))

k = int(input())
dx = [-1, 1, 0, 0]
dy = [0, 0, 1, -1]

for i in range(k):
    x1, y1, x2, y2 = map(int,input().split())
    
    x1 -= 1
    y1 -= 1
    x2 -= 1
    y2 -= 1

    lay = 0
    line = [[] for _ in range(m*n)]
    line[0].append((x1, y1))

    points = {}
    explored = {}
    
    points[(x1, y1)] = 0

    while len(line[lay]) > 0 or len(line[lay + 1]) > 0:

        if len(line[lay]) == 0:
            lay += 1

        now_point = line[lay].pop(0)

        if now_point == (x2, y2):
            print(points[(x2, y2)])
            break

        if now_point not in explored: 

            explored[now_point] = 1
            now_distance = A(now_point[0], now_point[1], x2, y2)

            for i in range(4):
                now_now_point = list(now_point)
                now_now_point[0] += dx[i]
                now_now_point[1] += dy[i]

                if now_now_point[0] >= 0 and now_now_point[1] >= 0 and now_now_point[0] < m and now_now_point[1] < n:
                    if mapp[now_now_point[0]][now_now_point[1]] != "#":
                        points[tuple(now_now_point)] = points[now_point] + 1

                        if now_distance > A(now_now_point[0], now_now_point[1], x2, y2):
                            line[lay].append(tuple(now_now_point))
                        else:
                            line[lay + 1].append(tuple(now_now_point))
    else:
        print(-1)