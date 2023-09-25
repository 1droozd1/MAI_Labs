import random

'''
Худшее время: O(n^2)
Среднее время: O(n^2)
Лучшее время: O(n)

Затраты памяти: O(1)

Шейкерная сортировка отличается от пузырьковой тем, что она двунаправленная: 
алгоритм перемещается не строго слева направо, а сначала слева направо, затем справа налево.
'''

def shaker_sort(array):
    left = 0
    right = len(array) - 1
    while left <= right:
        for i in range(left, right):
            if array[i] > array[i + 1]:
                array[i], array[i + 1] = array[i + 1], array[i]
        right -= 1
        
        for i in range(right, left, -1):
            if array[i] < array[i - 1]:
                array[i], array[i - 1] = array[i - 1], array[i]
        left += 1
    return array


# Пример использования
array = [random.randint(0, 100) for i in range(100)]
shaker_sort(array)
print("Отсортированный массив:", array)
