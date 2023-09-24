import tkinter as tk
from tkinter import DoubleVar
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

# Глобальная переменная для фактора масштабирования
zoom_factor = 1.0

def on_draw():
    global zoom_factor
    
    # Считываем значение константы a, A и B
    a = a_var.get()
    A = A_var.get()
    B = B_var.get()
    
    # Проверяем, что значения A, B и a корректны
    if A >= a or B <= -a or B <= A:
        print("Некорректные значения A, B или a")
        return
    
    # Создаем массив x в пределах от A до B
    x = np.linspace(A, B, 1000)
    
    # Вычисляем y
    y_squared = x**2 * ((a - x) / (a + x))  # Квадрат y
    y_squared = np.maximum(y_squared, 0)  # Убедимся, что значения неотрицательны
    y = np.sqrt(y_squared)  # Вычислим корень для получения y

    # Обновляем график с учетом масштабирования
    ax.cla()
    
    ax.plot(x, y, 'b')
    ax.plot(x, -y, 'b')
    ax.axhline(0, color='black', linewidth=0.5)
    ax.axvline(0, color='black', linewidth=0.5)
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

    # Устанавливаем новые пределы осей
    ax.set_xlim(A * zoom_factor, B * zoom_factor)
    ax.set_ylim(-a * zoom_factor, a * zoom_factor)
    
    canvas.draw()


def zoom_in():
    global zoom_factor
    zoom_factor *= 1.1  # Увеличиваем фактор масштабирования на 10%
    on_draw()  # Перерисовываем график после зума


def zoom_out():
    global zoom_factor
    zoom_factor /= 1.1  # Уменьшаем фактор масштабирования на 10%
    on_draw()  # Перерисовываем график после зума


root = tk.Tk()
root.title("2D Кривая")

# Создаем tkinter переменные для констант a, A и B
a_var = DoubleVar(value=1.0)
A_var = DoubleVar(value=-0.99)
B_var = DoubleVar(value=0.99)

# Создаем поля для ввода констант a, A и B
a_label = tk.Label(root, text="Введите a (a > 0): ")
a_label.pack()
a_entry = tk.Entry(root, textvariable=a_var)
a_entry.pack()

A_label = tk.Label(root, text="Введите A (A > -a): ")
A_label.pack()
A_entry = tk.Entry(root, textvariable=A_var)
A_entry.pack()

B_label = tk.Label(root, text="Введите B (B < a): ")
B_label.pack()
B_entry = tk.Entry(root, textvariable=B_var)
B_entry.pack()

# Создаем кнопки для отрисовки и управления масштабом
draw_button = tk.Button(root, text="Отрисовать", command=on_draw)
draw_button.pack()

zoom_in_button = tk.Button(root, text="Уменьшить", command=zoom_in)
zoom_in_button.pack()

zoom_out_button = tk.Button(root, text="Увеличить", command=zoom_out)
zoom_out_button.pack()

# Настраиваем фигуру и область рисования
fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

# Запускаем главный цикл tkinter
root.mainloop()