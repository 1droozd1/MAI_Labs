import random

'''
Худшее время: O(nlog(n))
Среднее время: O(nlog(n))
Лучшее время: O(nlog(n))

Затраты памяти: O(n)

Исходный массив: [29, 10, 14, 37, 13]
[29, 10] [14, 37, 13] - Разбиение
[29] [10] [14] [37] [13] - Дальнейшее разбиение
[10, 29] [14] [13, 37] - Слияние
[10, 29] [13, 14, 37] - Дальнейшее слияние
[10, 13, 14, 29, 37] - Финальное слияние
'''

def merge_sort(arr):
    if len(arr) <= 1:
        return arr  # Базовый случай: массив с одним или нулем элементов уже отсортирован
    
    mid = len(arr) // 2  # Находим середину массива
    left_half = arr[:mid]  # Делим массив на две половины
    right_half = arr[mid:]
    
    left_half = merge_sort(left_half)  # Рекурсивно сортируем каждую половину
    right_half = merge_sort(right_half)
    
    return merge(left_half, right_half)  # Сливаем отсортированные половины


def merge(left, right):
    result = []  # Результирующий массив
    i = j = 0  # Индексы для итерации по left и right
    
    while i < len(left) and j < len(right):  # Сливаем пока есть элементы в обоих массивах
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    while i < len(left):  # Если остались элементы в left, добавляем их все в результат
        result.append(left[i])
        i += 1
    
    while j < len(right):  # Если остались элементы в right, добавляем их все в результат
        result.append(right[j])
        j += 1
    
    return result  # Возвращаем отсортированный и слитый массив


# Пример использования
array = [random.randint(0, 100) for i in range(10)]
sorted_array = merge_sort(array)
print("Отсортированный массив:", sorted_array)