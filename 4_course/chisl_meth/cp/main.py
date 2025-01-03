import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# 1. Генерация данных
np.random.seed(42)
x = np.linspace(0, 10, 100)
y_true = np.sin(x) + 0.5
noise = np.random.normal(0, 0.2, size=x.shape)
y_noisy = y_true + noise

# 2. Визуализация исходных данных
plt.scatter(x, y_noisy, label="Noisy Data", alpha=0.6)
plt.plot(x, y_true, label="True Function", color="green")
plt.legend()
plt.title("Исходные данные")
plt.show()

# 3. Реализация робастного сглаживающего сплайна
class RobustSpline:
    def __init__(self, x, y, smoothing_factor=1.0):
        self.x = x
        self.y = y
        self.smoothing_factor = smoothing_factor
        self.weights = np.ones_like(y)
        self.spline = None

    def huber_loss(self, residuals, delta=1.0):
        return np.where(np.abs(residuals) <= delta,
                        0.5 * residuals**2,
                        delta * (np.abs(residuals) - 0.5 * delta))

    def update_weights(self):
        residuals = self.y - self.spline(self.x)
        self.weights = np.where(np.abs(residuals) <= 1.0, 1.0, 1.0 / np.abs(residuals))
        residuals = self.y - self.spline(self.x)
        assert residuals.shape == self.y.shape, "Остатки имеют неправильную форму!"
        print(f"Обновленные веса: {self.weights}")

    def fit(self, max_iter=10):
        for i in range(max_iter):
            self.spline = UnivariateSpline(self.x, self.y, w=self.weights, s=self.smoothing_factor)
            residuals = self.y - self.spline(self.x)
            print(f"Итерация {i + 1}: Средний остаток = {np.mean(residuals):.4f}")
            self.update_weights()

    def predict(self, x_new):
        return self.spline(x_new)

# 4. Построение и визуализация робастного сплайна
spline_model = RobustSpline(x, y_noisy, smoothing_factor=5.0)
spline_model.fit()

x_dense = np.linspace(0, 10, 500)
y_smooth = spline_model.predict(x_dense)

plt.scatter(x, y_noisy, label="Noisy Data", alpha=0.6)
plt.plot(x_dense, y_smooth, label="Robust Spline", color="red")
plt.plot(x, y_true, label="True Function", color="green")
plt.legend()
plt.title("Робастный сглаживающий сплайн")
plt.show()

# 5. Оценка модели
residuals = y_noisy - spline_model.predict(x)
huber_loss_values = spline_model.huber_loss(residuals)

print(f"Среднее значение ошибок: {np.mean(residuals):.4f}")
print(f"Суммарное значение Huber Loss: {np.sum(huber_loss_values):.4f}")