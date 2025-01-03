def complete_itinerary(n, itinerary):
    all_stations = set(range(1, n + 1))
    given_stations = set(itinerary) - {0}
    missing_stations = sorted(all_stations - given_stations, reverse=True)
    
    if len(missing_stations) != itinerary.count(0):
        return "*"
    
    filled_itinerary = []
    missing_index = 0
    
    for station in itinerary:
        if station == 0:
            filled_itinerary.append(missing_stations[missing_index])
            missing_index += 1
        else:
            filled_itinerary.append(station)
    
    # Проверка корректности маршрута
    max_station = max(filled_itinerary)
    peak_index = filled_itinerary.index(max_station)
    
    # Сценарий 1: Восхождение до максимума, затем спуск
    if (filled_itinerary[:peak_index] == sorted(filled_itinerary[:peak_index]) and
        filled_itinerary[peak_index:] == sorted(filled_itinerary[peak_index:], reverse=True)):
        return " ".join(map(str, filled_itinerary))
    
    # Сценарий 2: Постоянный спуск
    if filled_itinerary == sorted(filled_itinerary, reverse=True):
        return " ".join(map(str, filled_itinerary))
    
    filled_itinerary = []
    missing_index = 0
    missing_stations_ver_2 = missing_stations[::-1]

    for station in itinerary:
        if station == 0:
            filled_itinerary.append(missing_stations_ver_2[missing_index])
            missing_index += 1
        else:
            filled_itinerary.append(station)

    # Сценарий 3: Постоянный подъем
    if filled_itinerary == sorted(filled_itinerary):
        return " ".join(map(str, filled_itinerary))
    
    return "*"

n = int(input())
map_station = list(map(int, input().split()))
print(complete_itinerary(n, map_station))
