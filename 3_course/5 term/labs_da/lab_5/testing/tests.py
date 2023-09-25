import random
import time
import logging

def generate_test_data(text_length, pattern_length):
    # Генерируем случайную строку заданной длины
    text = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(text_length))
    
    # Генерируем подстроку, которая будет искаться
    pattern_start = random.randint(0, text_length - pattern_length)
    pattern = text[pattern_start:pattern_start + pattern_length]
    
    return text, pattern

def kmp_search(text, pattern):
    n = len(text)
    m = len(pattern)
    
    # Создаем префикс-функцию для шаблона
    pi = [0] * m
    j = 0
    for i in range(1, m):
        while j > 0 and pattern[i] != pattern[j]:
            j = pi[j - 1]
        if pattern[i] == pattern[j]:
            j += 1
        pi[i] = j

    # Выполняем поиск с использованием префикс-функции
    j = 0
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = pi[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1  # Найдено вхождение
    
    return -1  # Вхождение не найдено

def save_test_data_to_file(text, pattern, filename):
    with open(filename, "w") as file:
        file.write(f"Text: {text}\n")
        file.write(f"Pattern: {pattern}\n")

# Настройка логирования
logging.basicConfig(filename='test_results.log', level=logging.INFO, format='%(asctime)s - %(message)s')

def run_tests():
    for i in range(1, 8):
        text_length = 10**i
        pattern_length = random.randint(1, text_length)
        text, pattern = generate_test_data(text_length, pattern_length)

        # Сохраняем тестовые данные в файл
        filename = f"test_data_{i}.txt"
        save_test_data_to_file(text, pattern, filename)
        
        # Измеряем время выполнения find
        start_time = time.time()
        result_find = text.find(pattern)
        end_time = time.time()
        find_time = end_time - start_time
        
        # Измеряем время выполнения kmp_search
        start_time = time.time()
        result_kmp = kmp_search(text, pattern)
        end_time = time.time()
        kmp_time = end_time - start_time
        
        # Сравниваем результаты
        assert result_find == result_kmp
        
        # Записываем результаты в файл журнала
        log_message = f"Text Length: 10^{i}, Pattern Length: {pattern_length}\n"
        log_message += f"Find Time: {find_time:.6f} seconds\n"
        log_message += f"KMP Time: {kmp_time:.6f} seconds\n"
        log_message += "-" * 30
        logging.info(log_message)

if __name__ == "__main__":
    run_tests()
