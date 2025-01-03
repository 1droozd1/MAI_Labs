def result(n: int, map_station: list):
    all_stations = set(range(1, n + 1))
    given_stations = set(map_station) - {0}
    missing_stations = list(all_stations - given_stations)

    if len(missing_stations) != map_station.count(0):
        return "*"
    
    if n in missing_stations:
        # n - в начало - убывающая
        missing_stations = sorted(missing_stations, reverse=True)
        map_station_ver_1 = map_station[::]

        idx = 0
        for i in range(n):
            if map_station_ver_1[i] == 0:
                map_station_ver_1[i] = missing_stations[idx]
                idx += 1

        # Проверить валидность маршрута
        lower_way = False

        for i in range(1, n):
            if lower_way == False:
                if map_station_ver_1[i] > map_station_ver_1[i - 1]:
                    continue
                else:
                    lower_way = True
            else:
                if map_station_ver_1[i] < map_station_ver_1[i - 1]:
                    continue
                else:
                    break
        else:
            return map_station_ver_1
        
        # n - в конец - возрастающая
        missing_stations = missing_stations[::-1]
        map_station_ver_2 = map_station[::]

        idx = 0
        for i in range(n):
            if map_station_ver_2[i] == 0:
                map_station_ver_2[i] = missing_stations[idx]
                idx += 1
        # Проверить валидность маршрута
        lower_way = False

        for i in range(1, n):
            if lower_way == False:
                if map_station_ver_2[i] > map_station_ver_2[i - 1]:
                    continue
                else:
                    lower_way = True
            else:
                if map_station_ver_2[i] < map_station_ver_2[i - 1]:
                    continue
                else:
                    break
        else:
            return map_station_ver_2
        
        return '*'
    
    else:
        index_max = map_station.index(n)
        left, right = 0, len(map_station) - 1

        missing_stations = sorted(missing_stations)

        while left < index_max:
            if map_station[left] == 0:
                map_station[left] = missing_stations[0]
                missing_stations.pop(0)
            left += 1
        
        while right > index_max:
            if map_station[right] == 0:
                map_station[right] = missing_stations[-1]
                missing_stations.pop(-1)
            right -= 1

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
        
        return '*'

n = int(input())
map_station = list(map(int, input().split()))
print(*result(n, map_station))
