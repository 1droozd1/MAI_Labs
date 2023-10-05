import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Задаем координаты вершин квадрата (основания пирамиды)
base_vertices = np.array([
    [-1, -1, 0],
    [1, -1, 0],
    [1, 1, 0],
    [-1, 1, 0]
])

# Задаем высоту пирамиды
height = 2

# Задаем вершину пирамиды
apex = np.array([0, 0, height])

# Определяем грани пирамиды
faces = [
    [base_vertices[0], base_vertices[1], apex],
    [base_vertices[1], base_vertices[2], apex],
    [base_vertices[2], base_vertices[3], apex],
    [base_vertices[3], base_vertices[0], apex]
]

# Создаем 3D-график
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Отображаем грани пирамиды
ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))

# Устанавливаем пределы осей
ax.set_xlim([-2, 2])
ax.set_ylim([-2, 2])
ax.set_zlim([0, 3])

# Настройка отображения
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

plt.show()
