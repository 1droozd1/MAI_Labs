import numpy as np

def f(x, y):
    """Целевая функция для минимизации."""
    return x**2 + y**2

def g(x, y):
    """Ограничение."""
    return x + y - 2

def system(vars):
    """Система уравнений Лагранжа.

    vars[0] = x
    vars[1] = y
    vars[2] = lambda (множитель Лагранжа)
    """
    x, y, lambd = vars
    eq1 = 2 * x + lambd       # ∂L/∂x = 0
    eq2 = 2 * y + lambd       # ∂L/∂y = 0
    eq3 = g(x, y)             # Ограничение g(x, y) = 0
    return np.array([eq1, eq2, eq3])

def jacobian(vars):
    """Якобиан системы уравнений."""
    x, y, lambd = vars
    J = np.array([
        [2, 0, 1],   # ∂(2x + λ)/∂x, ∂(2x + λ)/∂y, ∂(2x + λ)/∂λ
        [0, 2, 1],   # ∂(2y + λ)/∂x, ∂(2y + λ)/∂y, ∂(2y + λ)/∂λ
        [1, 1, 0]    # ∂g/∂x, ∂g/∂y, ∂g/∂λ
    ])
    return J

def newton_raphson(system, jacobian, initial_guess, tol=1e-10, max_iter=100):
    """Метод Ньютона-Рафсона для систем нелинейных уравнений."""
    vars = np.array(initial_guess, dtype=float)
    for i in range(max_iter):
        F = system(vars)
        J = jacobian(vars)
        try:
            delta = np.linalg.solve(J, -F)
        except np.linalg.LinAlgError:
            raise Exception("Якобиан вырожден, метод не сходится.")
        vars = vars + delta
        if np.linalg.norm(delta, ord=2) < tol:
            print(f"Сошлось за {i+1} итераций.")
            return vars
    raise Exception("Метод Ньютона-Рафсона не сошёлся за заданное количество итераций.")

def main():
    # Начальное приближение
    initial_guess = [0.5, 0.5, 1.0]  # x, y, lambda

    solution = newton_raphson(system, jacobian, initial_guess)
    x, y, lambd = solution

    print(f"Решение:")
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"lambda = {lambd}")

    # Проверка решения
    print("\nПроверка:")
    print(f"f(x, y) = {f(x, y)}")
    print(f"g(x, y) = {g(x, y)} (должно быть 0)")

if __name__ == "__main__":
    main()