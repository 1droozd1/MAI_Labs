import tkinter as tk
from tkinter import DoubleVar
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Глобальная переменная для фактора масштабирования
zoom_factor = 1.0

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def on_draw():

    global zoom_factor
    
    # Считываем значение константы a
    a = a_var.get()
    
    # Вычисляем координаты вершин пирамиды
    X = np.array([0, 0, 0])  # Вершина
    A = np.array([-a, -a, 0])  # Основание
    B = np.array([a, -a, 0])
    C = np.array([a, a, 0])
    D = np.array([-a, a, 0])
    E = np.array([0, 0, a])  # Пересечение вершины и основания
    
    # Создаем вершины пирамиды
    vertices = [X, A, B, C, D, E]
    
    # Создаем грани пирамиды
    faces = [[vertices[0], vertices[1], vertices[2], vertices[3]],
             [vertices[0], vertices[1], vertices[4]],
             [vertices[0], vertices[2], vertices[4]],
             [vertices[0], vertices[3], vertices[4]],
             [vertices[1], vertices[2], vertices[5]],
             [vertices[2], vertices[3], vertices[5]],
             [vertices[3], vertices[4], vertices[5]],
             [vertices[4], vertices[1], vertices[5]]]
    
    print("Рисуем")
    
    # Рисуем грани пирамиды
    ax.cla()
    ax.add_collection3d(Poly3DCollection(faces, facecolors='cyan', linewidths=1, edgecolors='r', alpha=.25))
    
    # Создаем векторы для стрелок на осях
    arrow_length = a * zoom_factor  # Длина стрелок
    arrow_color = 'black'
    ax.quiver(0, 0, 0, arrow_length, 0, 0, color=arrow_color, label='X')
    ax.quiver(0, 0, 0, 0, arrow_length, 0, color=arrow_color, label='Y')
    ax.quiver(0, 0, 0, 0, 0, arrow_length, color=arrow_color, label='Z')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    ax.set_xlim([-a * zoom_factor * 1.5, a * zoom_factor * 1.5])
    ax.set_ylim([-a * zoom_factor * 1.5, a * zoom_factor * 1.5])
    ax.set_zlim([0, a * zoom_factor * 1.5])
    
    canvas.draw()

def zoom_in():
    global zoom_factor
    zoom_factor *= 1.1  # Увеличиваем фактор масштабирования на 10%
    print("Увеличиваем")
    on_draw()  # Перерисовываем график после зума

def zoom_out():
    global zoom_factor
    zoom_factor /= 1.1  # Уменьшаем фактор масштабирования на 10%
    print('Уменьшаем')
    on_draw()  # Перерисовываем график после зума

root = tk.Tk()
root.title("3D Пирамида")

# Создаем tkinter переменную для константы a
a_var = DoubleVar(value=1.0)

# Создаем поле для ввода константы a
a_label = tk.Label(root, text="Введите a (a > 0): ")
a_label.pack()
a_entry = tk.Entry(root, textvariable=a_var)
a_entry.pack()

# Создаем кнопки для отрисовки и управления масштабом
draw_button = tk.Button(root, text="Отрисовать", command=on_draw)
draw_button.pack()

zoom_in_button = tk.Button(root, text="Увеличить", command=zoom_in)
zoom_in_button.pack()

zoom_out_button = tk.Button(root, text="Уменьшить", command=zoom_out)
zoom_out_button.pack()

# Настраиваем 3D фигуру и область рисования
fig = plt.figure()
fig.set_size_inches(9, 7)

# Задайте ширину и высоту окна
window_width = 600
window_height = 500

# Вызов функции для выравнивания окна по центру экрана
center_window(root, window_width, window_height)

ax = fig.add_subplot(111, projection='3d')
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Запускаем главный цикл tkinter
root.mainloop()