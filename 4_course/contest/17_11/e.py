def result(n, map_station):
    all_stations = set(range(1, n + 1))
    given_stations = set(map_station) - {0}
    missing_stations = list(all_stations - given_stations)
    map_station_ver2 = map_station[:]

    if len(missing_stations) != map_station.count(0):
        return "*"
    
    missing_stations.sort(reverse=True)
    missing_stations_ver2 = missing_stations[:]

    idx = 0
    for i in range(n):
        if map_station[i] == 0:
            map_station[i] = missing_stations[idx]
            idx += 1

    # Проверить валидность маршрута
    lower_way = False

    for i in range(1, n):
        if lower_way == False:
            if map_station[i] > map_station[i - 1]:
                continue
            else:
                lower_way = True
        else:
            if map_station[i] < map_station[i - 1]:
                continue
            else:
                break
    else:
        return map_station

    missing_stations_ver2 = missing_stations_ver2[::-1]

    for i in range(n):
       if map_station_ver2[i] == 0:
           map_station_ver2[i] = missing_stations_ver2[0]
           missing_stations_ver2.pop(0)
       else:
           if map_station_ver2[i] == n:
               missing_stations_ver2 = missing_stations_ver2[::-1]
    
    # Проверить валидность маршрута
    lower_way = False

    for i in range(1, n):
        if lower_way == False:
            if map_station_ver2[i] > map_station_ver2[i - 1]:
                continue
            else:
                lower_way = True
        else:
            if map_station_ver2[i] < map_station_ver2[i - 1]:
                continue
            else:
                break
    else:
        return map_station_ver2
    
    return '*'

n = int(input())
map_station = list(map(int, input().split()))
print(*result(n, map_station))
