import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.colors import LightSource

# Функция для генерации сектора параболы
def get_parabola_section(a, theta_range, segments, height):
    # Расчет углов для сектора
    theta = np.linspace(0, theta_range, segments)
    # Расчет радиусов для каждого угла по параболе
    r = a * theta**2
    # Создание вершин параболы в 3D пространстве
    return [[r[i] * np.cos(theta[i]), r[i] * np.sin(theta[i]), height] for i in range(segments)]

# Функция для генерации вершин цилиндра с параболическим основанием
def generate_cylinder_vertices(h, a, theta_range, n_segments):
    vertices = []
    # Генерация слоев цилиндра
    for i in range(n_segments + 1):
        z = h * i / n_segments
        vertices += get_parabola_section(a, theta_range, n_segments, z)
    return np.array(vertices)

# Функция для генерации граней цилиндра
def generate_cylinder_faces(n_segments, base_segments):
    faces = []
    # Генерация граней для боковых сторон цилиндра
    for i in range(n_segments):
        for j in range(base_segments - 1):
            current = i * base_segments + j
            next = current + base_segments
            faces += [
                [current, current + 1, next],
                [current + 1, next + 1, next]
            ]
    return faces

# Функция для отрисовки цилиндра с освещением
def draw_cylinder(vertices, faces, ax, light_azimuth, light_altitude):
    ax.clear()
    ls = LightSource(azdeg=light_azimuth, altdeg=light_altitude)
    shaded = np.zeros((len(faces), 3))
    for i, face in enumerate(faces):
        # Расчет нормалей для каждой грани для правильного освещения
        normals = np.cross(vertices[face[1]] - vertices[face[0]],
                           vertices[face[2]] - vertices[face[0]])
        normals /= np.linalg.norm(normals)
        shaded[i] = ls.shade_normals(normals)
    collection = Poly3DCollection(vertices[faces], facecolors=shaded, linewidths=0.5, edgecolors=(0, 0, 0, 0.3))
    ax.add_collection3d(collection)
    
    # Автоматическое масштабирование осей
    max_radius = np.max(np.linalg.norm(vertices[:, :2], axis=1))
    ax.auto_scale_xyz([-max_radius, max_radius], [-max_radius, max_radius], [0, h])
    plt.draw()

# Функция для обновления визуализации цилиндра на основе слайдеров
def update(val):
    global n_segments, light_azimuth, light_altitude, h, a, theta_range
    # Чтение значений с слайдеров
    n_segments = int(slider_segments.val)
    light_azimuth = slider_light.val
    light_altitude = 90 - abs(slider_light.val - 180)
    # Генерация вершин и граней для новой конфигурации
    vertices = generate_cylinder_vertices(h, a, theta_range, n_segments)
    faces = generate_cylinder_faces(n_segments, n_segments)
    # Отрисовка цилиндра с новыми параметрами
    draw_cylinder(vertices, faces, ax, light_azimuth, light_altitude)

# Параметры цилиндра
h, a, theta_range = 15, 0.1, np.pi  # Высота, параметр a для параболы и угловой диапазон для сектора параболы

# Параметры источника света
light_azimuth = 45
light_altitude = 30

# Настройка отображения
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Начальное количество сегментов
n_segments = 20

# Слайдер для количества сегментов
ax_slider_segments = plt.axes([0.25, 0.01, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_segments = Slider(ax_slider_segments, 'Segments', 4, 40, valinit=n_segments, valstep=1)
slider_segments.on_changed(update)

# Слайдер для угла освещения
ax_slider_light = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_light = Slider(ax_slider_light, 'Light Azimuth & Altitude', 0, 360, valinit=light_azimuth, valstep=1)
slider_light.on_changed(update)

# Первоначальная отрисовка
update(0)

plt.show()
