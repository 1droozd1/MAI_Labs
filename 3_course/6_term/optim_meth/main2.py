import numpy as np

def f(x, y, z):
    """Целевая функция для минимизации."""
    return x**2 + y**2 + z**2

def g1(x, y, z):
    """Первое ограничение."""
    return x + y + z - 1

def g2(x, y, z):
    """Второе ограничение."""
    return x**2 + y**2 - z

def system(vars):
    """Система уравнений Лагранжа.

    vars[0] = x
    vars[1] = y
    vars[2] = z
    vars[3] = lambda
    vars[4] = mu
    """
    x, y, z, lambd, mu = vars
    eq1 = 2 * x - lambd - 2 * mu * x        # ∂L/∂x = 0
    eq2 = 2 * y - lambd - 2 * mu * y        # ∂L/∂y = 0
    eq3 = 2 * z - lambd + mu                # ∂L/∂z = 0
    eq4 = g1(x, y, z)                       # Ограничение g1 = 0
    eq5 = g2(x, y, z)                       # Ограничение g2 = 0
    return np.array([eq1, eq2, eq3, eq4, eq5])

def jacobian(vars):
    """Якобиан системы уравнений."""
    x, y, z, lambd, mu = vars
    J = np.array([
        [2 - 2 * mu,        0,          0, -1, -2 * x],
        [0,        2 - 2 * mu,          0, -1, -2 * y],
        [0,               0,        2, -1, 1],
        [1,               1,        1, 0, 0],
        [2 * x,          2 * y,       -1, 0, 0]
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
    initial_guess = [0.5, 0.5, 0.5, 1.0, 0.5]

    solution = newton_raphson(system, jacobian, initial_guess)
    x, y, z, lambd, mu = solution

    print(f"Решение:")
    print(f"x = {x}")
    print(f"y = {y}")
    print(f"z = {z}")
    print(f"lambda = {lambd}")
    print(f"mu = {mu}")

    # Проверка решения
    print("\nПроверка:")
    print(f"f(x, y, z) = {f(x, y, z)}")
    print(f"g1(x, y, z) = {g1(x, y, z)} (должно быть 0)")
    print(f"g2(x, y, z) = {g2(x, y, z)} (должно быть 0)")

if __name__ == "__main__":
    main()
