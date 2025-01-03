from collections import Counter

def read_text_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def calculate_letter_match_percentage(text1, text2):
    count1 = Counter(text1.replace(" ", "").lower())
    count2 = Counter(text2.replace(" ", "").lower())
    total_letters = sum(count1.values())
    matches = sum((count1 & count2).values())
    percentage = matches / total_letters if total_letters > 0 else 0
    return percentage

# Пути к файлам
files = {
    'long_text1': './lab_3/longrange/long_text1.txt',
    'long_text2': './lab_3/longrange/long_text2.txt',
    'long_word1': './lab_3/longrange/long_word1.txt',
    'long_word2': './lab_3/longrange/long_word2.txt',
    'long_symbols1': './lab_3/longrange/long_symbols1.txt',
    'long_symbols2': './lab_3/longrange/long_symbols2.txt',

    'mid_text1': './lab_3/midrange/mid_text1.txt',
    'mid_text2': './lab_3/midrange/mid_text2.txt',
    'mid_word1': './lab_3/midrange/mid_word1.txt',
    'mid_word2': './lab_3/midrange/mid_word2.txt',
    'mid_symbols1': './lab_3/midrange/mid_symbols1.txt',
    'mid_symbols2': './lab_3/midrange/mid_symbols2.txt',

    'low_text1': './lab_3/lowrange/low_text1.txt',
    'low_text2': './lab_3/lowrange/low_text2.txt',
    'low_word1': './lab_3/lowrange/low_word1.txt',
    'low_word2': './lab_3/lowrange/low_word2.txt',
    'low_symbols1': './lab_3/lowrange/low_symbols1.txt',
    'low_symbols2': './lab_3/lowrange/low_symbols2.txt'
}

# Чтение содержимого файлов
texts = {name: read_text_from_file(path) for name, path in files.items()}

# Сравнения
comparisons = [
    ('long_text1', 'long_text2'),
    ('long_text1', 'long_symbols1'),
    ('long_text1', 'long_word1'),
    ('long_symbols1', 'long_symbols2'),
    ('long_word1', 'long_word2'),

    ('mid_text1', 'mid_text2'),
    ('mid_text1', 'mid_symbols1'),
    ('mid_text1', 'mid_word1'),
    ('mid_symbols1', 'mid_symbols2'),
    ('mid_word1', 'mid_word2'),

    ('low_text1', 'low_text2'),
    ('low_text1', 'low_symbols1'),
    ('low_text1', 'low_word1'),
    ('low_symbols1', 'low_symbols2'),
    ('low_word1', 'low_word2')
]

# Расчет и вывод процентов совпадения букв
for text1_name, text2_name in comparisons:
    percentage = calculate_letter_match_percentage(texts[text1_name], texts[text2_name])
    print(f"Совпадения между {text1_name} и {text2_name}: {percentage:.4f}")
