import random
'''
Худшее время: O(n^2)
Среднее время: O(n^2)
Лучшее время: O(n)

Затраты памяти: O(1)
'''

def bubble_sort(array):
    n = len(array)
    for i in range(n):
        # После каждого прохода самый большой элемент "всплывает" в конец списка
        # Поэтому, на каждом следующем проходе мы уменьшаем диапазон, в котором
        # производится сравнение элементов
        for j in range(0, n-i-1):
            if array[j] > array[j+1]:
                # Обмен элементами
                array[j], array[j+1] = array[j+1], array[j]

# Пример использования
array = [random.randint(0, 100) for i in range(100)]
bubble_sort(array)
print("Отсортированный массив:", array)
