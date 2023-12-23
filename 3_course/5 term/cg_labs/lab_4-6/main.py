import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import time

# Параметры цилиндра
h, a, theta_range = 15, 0.1, np.pi  # Высота, параметр a для параболы и угловой диапазон для сектора параболы

# Параметры источника света
light_azimuth = 45
light_altitude = 30

# Начальное количество сегментов
n_segments = 20

# Угол поворота
rotation_angle = 0.0

# Масштаб сцены
scale = 1.0

# Угол поворота камеры
camera_rotation = 0.0

# Расстояние между камерой и фигурой
camera_distance = 30.0

# Функция для настройки камеры
def set_camera():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    camera_x = camera_distance * np.cos(np.radians(camera_rotation))
    camera_y = camera_distance * np.sin(np.radians(camera_rotation))
    gluLookAt(camera_x, camera_y, 10, 0, 0, 0, 0, 0, 1)

# Функция для генерации сектора параболы
def get_parabola_section(a, theta_range, segments, height):
    vertices = []
    for i in range(segments):
        theta = (i / segments) * theta_range
        r = a * theta**2
        x = r * np.cos(theta)
        y = r * np.sin(theta)
        vertices.append((x, y, height))
    return vertices

# Функция для генерации вершин цилиндра с параболическим основанием
def generate_cylinder_vertices(h, a, theta_range, n_segments, scale):
    vertices = []
    for i in range(n_segments + 1):
        z = (i / n_segments) * h
        vertices.extend(get_parabola_section(a * scale, theta_range, n_segments, z))
    return vertices

# Функция для генерации граней цилиндра
def generate_cylinder_faces(n_segments, base_segments):
    faces = []
    for i in range(n_segments):
        for j in range(base_segments - 1):
            current = i * base_segments + j
            next = current + base_segments
            faces.append((current, current + 1, next))
            faces.append((current + 1, next + 1, next))
    return faces

# Функция для настройки освещения
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, (1.0, -1.0, 1.0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))

# Функция для отрисовки цилиндра с освещением
def draw_cylinder(vertices, faces):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()
    glRotatef(light_azimuth, 0, 0, 1)
    glRotatef(light_altitude, 1, 0, 0)
    
    # Применяем поворот вокруг оси Z
    glRotatef(rotation_angle, 0, 0, 1)

    glBegin(GL_TRIANGLES)
    for face in faces:
        for vertex_index in face:
            x, y, z = vertices[vertex_index]
            glNormal3f(2 * x / (a * scale)**2, 2 * y / (a * scale)**2, -1)
            glVertex3f(x, y, z)
    glEnd()

    glPopMatrix()
    pygame.display.flip()

# Инициализация Pygame
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -30)

# Включение тестирования глубины для 3D-отображения
glEnable(GL_DEPTH_TEST)

# Настройка освещения
setup_lighting()

# Генерация вершин и граней цилиндра
vertices = generate_cylinder_vertices(h, a, theta_range, n_segments, scale)
faces = generate_cylinder_faces(n_segments, n_segments)

# Переменные для управления анимацией
animation_speed = 0.1  # Скорость анимации
animation_time = 0.0  # Время анимации
animation_running = True  # Флаг, указывающий, выполняется ли анимация

# Основной цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            quit()

        # Обработка событий клавиатуры
        if event.type == KEYDOWN:
            if event.key == K_LEFT:  # Стрелка влево
                rotation_angle += 5.0  # Увеличиваем угол поворота
            elif event.key == K_RIGHT:  # Стрелка вправо
                rotation_angle -= 5.0  # Уменьшаем угол поворота
            elif event.key == K_UP:  # Клавиша "+" (увеличить масштаб)
                scale += 0.1  # Увеличиваем масштаб
                vertices = generate_cylinder_vertices(h, a, theta_range, n_segments, scale)
            elif event.key == K_DOWN:  # Клавиша "-" (уменьшить масштаб)
                scale -= 0.1  # Уменьшаем масштаб
                if scale < 0.1:
                    scale = 0.1  # Минимальный масштаб
                vertices = generate_cylinder_vertices(h, a, theta_range, n_segments, scale)
            elif event.key == K_s:  # Клавиша "S" (запуск/остановка анимации)
                animation_running = not animation_running

    # Если анимация выполняется, обновляем параметры анимации
    if animation_running:
        animation_time += animation_speed
        a = 0.1 + 0.05 * np.sin(animation_time)  # Изменяем параметр 'a' синусоидально
        vertices = generate_cylinder_vertices(h, a, theta_range, n_segments, scale)

    # Отрисовка цилиндра с освещением
    draw_cylinder(vertices, faces)

    # Ожидание небольшой задержки для управления скоростью анимации
    time.sleep(0.03)
