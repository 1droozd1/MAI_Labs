# Генерация входного файла input.bin с бинарными данными
with open("input.bin", "wb") as f:
    n = 10  # количество чисел
    data = [10, 4, 2, 8, 6, 1, 3, 7, 9, 5]  # массив чисел типа uint
    f.write(n.to_bytes(4, byteorder='little'))  # Записываем n (4 байта)
    for num in data:
        f.write(num.to_bytes(4, byteorder='little'))  # Записываем числа (по 4 байта каждое)