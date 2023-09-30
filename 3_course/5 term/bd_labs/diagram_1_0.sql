-- Создание таблицы для хранения информации об абитурентах
CREATE TABLE applicants (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    address TEXT,
    phone VARCHAR(20),
    email VARCHAR(255),
    photo BYTEA -- Для хранения фото в виде бинарных данных
);

-- Создание таблицы для хранения информации о документах абитурентов
CREATE TABLE applicant_documents (
    id SERIAL PRIMARY KEY,
    applicant_id INT REFERENCES applicants(id),
    document_name VARCHAR(255) NOT NULL,
    document_file BYTEA, -- Для хранения документов в формате PDF в виде бинарных данных
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы для расписания и групп
CREATE TABLE schedule (
    id SERIAL PRIMARY KEY,
    group_name VARCHAR(50) NOT NULL,
    course_name VARCHAR(255),
    schedule_data JSONB -- Может содержать расписание в формате JSON
);

-- Создание таблицы для информации о преподавателях (если необходимо)
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    phone VARCHAR(20)
);

-- Создание таблицы для доступа преподавателей к расписанию
CREATE TABLE teacher_access (
    id SERIAL PRIMARY KEY,
    teacher_id INT REFERENCES teachers(id),
    schedule_id INT REFERENCES schedule(id)
);
