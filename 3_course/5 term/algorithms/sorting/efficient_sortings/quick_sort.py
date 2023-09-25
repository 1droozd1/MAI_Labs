import random

'''
Худшее время: O(n^2)
Среднее время: O(nlog(n))
Лучшее время: O(n)

Затраты памяти: O(n)
'''

def quick_sort(arr):
    if len(arr) <= 1:
        return arr  # Базовый случай: если массив пустой или содержит один элемент, он уже отсортирован
    pivot = arr.pop()  # Выбираем опорный элемент
    less_than_pivot = []  # Массив для элементов меньше опорного
    greater_than_pivot = []  # Массив для элементов больше опорного
    for element in arr:  # Разбиваем оставшийся массив на два подмассива
        if element <= pivot:
            less_than_pivot.append(element)
        else:
            greater_than_pivot.append(element)
    return quick_sort(less_than_pivot) + [pivot] + quick_sort(greater_than_pivot)  # Рекурсивно сортируем подмассивы и объединяем результаты


# Пример использования
array = [random.randint(0, 100) for i in range(10)]
sorted_array = quick_sort(array)
print("Отсортированный массив:", sorted_array)
