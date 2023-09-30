'''Генерация данных для БД'''
import random
from faker import Faker
import psycopg2

def generate_russian_phone_number():
    '''Генерирует номер телефона в формате +7(999)999-99-99'''
    region_code = random.randint(1, 999)
    phone_number = random.randint(100_0000, 999_9999)
    formatted_number = f"+7({region_code:03d}){phone_number:07d}"
    return formatted_number


# Инициализируем Faker для генерации данных
fake = Faker()

# Устанавливаем соединение с базой данных
conn = psycopg2.connect(
    database="bd_prodject", user="admin", password="postgres",
    host="127.0.0.1", port="5432"
)

# Создаем курсор для выполнения SQL-запросов
cursor = conn.cursor()

# Генерируем и вставляем данные
for _ in range(100):
    full_name = fake.name()
    address = fake.address()
    phone = generate_russian_phone_number()
    email = fake.email()

    # SQL-запрос для вставки данных в таблицу applicants
    INSERT_QUERY = "INSERT INTO applicants (full_name, address, phone, email) VALUES (%s, %s, %s, %s)"
    cursor.execute(INSERT_QUERY, (full_name, address, phone, email))

# Фиксируем изменения в базе данных
conn.commit()

# Закрываем соединение
conn.close()
