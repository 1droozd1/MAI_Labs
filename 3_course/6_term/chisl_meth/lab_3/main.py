from matrix import Matrix
import re
from math import sqrt, atan

class Polynomial:
    def __init__(self, coefficients):
        if isinstance(coefficients, str):
            self.coeffs = self._parse_poly_str(coefficients)
        elif isinstance(coefficients, dict):
            self.coeffs = coefficients
    
    def __call__(self, x):
        res = 0
        for power, coeff in self.coeffs.items():
            res += coeff * x ** power
        return res
    
    def _parse_poly_str(self, poly_str):
        pattern = re.compile(r"([+-]?[\d]*\.?\d+)*(x\^?(\d*))?")
        parts = pattern.findall(poly_str.replace(' ', '').replace('--', '+'))
        coeffs = {}
            
        for part in parts:
            if part[0]:
                monomial = part
                coeff = monomial[0]
                if coeff == '+' or coeff == '':
                    coeff = 1
                elif coeff == '-':
                    coeff = -1
                else:
                    coeff = float(coeff)
                    
                if monomial[1].startswith('x'):
                    if monomial[2] == '':
                        power = 1
                    else:
                        power = int(monomial[2])
                else:
                    power = 0
                    
                if power in coeffs:
                    coeffs[power] += coeff
                else:
                    coeffs[power] = coeff

        return coeffs


    def __mul__(self, other):
        # Перемножение многочленов
        new_coeffs = {}
        for power1, coeff1 in self.coeffs.items():
            for power2, coeff2 in other.coeffs.items():
                new_power = power1 + power2
                new_coeff = coeff1 * coeff2
                if new_power in new_coeffs:
                    new_coeffs[new_power] += new_coeff
                else:
                    new_coeffs[new_power] = new_coeff
        return Polynomial(new_coeffs)

    def __add__(self, other):
        new_coeffs = self.coeffs.copy()
        for power, coeff in other.coeffs.items():
            if power in new_coeffs:
                new_coeffs[power] += coeff
            else:
                new_coeffs[power] = coeff
        return Polynomial(new_coeffs)
    
    def derivative(self):
        new_coeffs = {}
        for power, coeff in self.coeffs.items():
            if power > 0:
                new_coeffs[power - 1] = coeff * power
        return Polynomial(new_coeffs)


    def __str__(self):
        return self._fmt_poly(self.coeffs)
    
    def _fmt_poly(self, coeffs):
        # Форматирование многочлена в строку
        terms = []
        for power in sorted(coeffs.keys(), reverse=True):
            coeff = coeffs[power]
            if coeff:
                if power == 0:
                    term = str(coeff)
                elif power == 1:
                    term = f"{coeff if coeff != 1 else ''}x"
                else:
                    term = f"{coeff if coeff != 1 else ''}x^{power}"
                terms.append(term)
        return ' + '.join(term for term in terms if term).replace('+ -', '- ')

class Spline:
    def __init__(self, x, pols):
        self.x = x
        self.pols = pols

    @classmethod
    def lower_bound(cls, A, key):
        left = -1
        right = len(A)
        while right > left + 1:
            middle = (left + right) // 2
            if A[middle] >= key:
                right = middle
            else:
                left = middle
        return right

    def derivative(self):
        return Spline(self.x, [p.derivative() for p in self.pols])

    def __call__(self, x):
        i = self.lower_bound(self.x, x)
        return self.pols[max(0, i-1)](x)

class Interpolator:
    @classmethod
    def lagrange_interpolation(cls, points):
        terms = []
        for i, (xi, yi) in enumerate(points):
            Li = Polynomial("1.0")
            K = 1.0
            for j, (xj, _) in enumerate(points):
                if i != j:
                    # (x - xj) / (xi - xj)
                    K *= (xi - xj)
                    Li = Li * Polynomial(f"1.0x - {xj}")
            terms.append(Li * Polynomial(f"{yi/K}"))

        lagrange_poly = Polynomial("0")
        for term in terms:
            lagrange_poly = lagrange_poly + term
        return lagrange_poly

    @classmethod
    def newton_interpolation(cls, points):
        n = len(points)
        x, y = zip(*points)
        res = {
            0: y[0],
        }
        dp = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n - 1):
            dp[0][i] = (y[i] - y[i+1]) / (x[i]-x[i+1])
        for i in range(1, n - 1):
            for j in range(n - i - 1):
                dp[i][j] = (dp[i - 1][j] - dp[i - 1][j + 1]) / (x[j] - x[j + 1 + i])
        
        for v in dp[:-1]:
            print(*v[:-1])
        
        Li = Polynomial("1.0")
        for i in range(n - 1):
            Li = Li * Polynomial(f"1.0x - {x[i]}")
            for power, coeff in Li.coeffs.items():
                res[power] = res.get(power, 0) + dp[i][0] * coeff
        return Polynomial(res)

    @classmethod
    def spline(cls, points):
        n = len(points) - 1
        x, y = zip(*sorted(points))
        h = [x[i+1] - x[i] for i in range(n)]
        A = Matrix(rows=n-1, cols=n-1)
        B = Matrix(rows=n-1, cols=n-1)
        for i in range(n - 1):
            if (i > 0):
                A[i][i - 1] = h[i]
            A[i][i] = 2 * (h[i] + h[i + 1])
            if (i < n - 2):
                A[i][i + 1] = h[i + 1]
            B[i][0] = 3 * ((y[i + 2] - y[i + 1]) / h[i + 1] - (y[i + 1] - y[i]) / h[i])
        
        print(A)
        print()
        print(B)
        
        S = A.solve_tridiagonal(B)
        c = [0] + [S[i - 1][0] for i in range(1, n)]
        a = [y[i] for i in range(n)]
        b = [
            (y[i + 1] - y[i]) / h[i] - 1. / 3. * (c[i + 1] + 2 * c[i]) * h[i + 1]
            for i in range(n - 1)
        ] + [(y[n] - y[n - 1]) / h[n - 1] - 2. / 3. * h[n - 1] * c[n - 1]]
        d = [(c[i + 1] - c[i]) / (3 * h[i]) for i in range(n - 1)]+[-c[n - 1] / (3 * h[n - 1])]

        #print(h)
        # print(a)
        # print(b)
        # print(c)
        # print(d)
        
        res = list()
        for i in range(n):
            tmp = Polynomial(f"1.0x - {x[i]}")
            A = Polynomial({0:a[i]})
            B = Polynomial({0:b[i]}) * tmp
            C = Polynomial({0:c[i]}) * tmp * tmp
            D = Polynomial({0:d[i]}) * tmp * tmp * tmp
            res += [A + B + C + D]
        for ll in res:
            print(ll)
        return Spline(x, res)

    @classmethod
    def squares(cls, points, power=4):
        n = len(points)
        P = Matrix([[points[i][0]**j for j in range(power + 1)] for i in range(n)])
        G = P.transpose() @ P
        Y = Matrix([[points[i][1]] for i in range(n)])
        B = P.transpose() @ Y
        res = G.solve_gauss(B)
        return Polynomial({i: res[i][0] for i in range(power + 1)})

class Derrivative:
    @staticmethod
    def derivative(points, power):
        power += 1
        n = len(points)
        p = sorted(points)

        pols = [
            Interpolator.lagrange_interpolation(p[i : i + power]).derivative()
            for i in range(n - power)
        ]
        return Spline(list(zip(*points))[0], pols)

class Integratetor:
    @staticmethod
    def rectangles(f, a, b, step):
        res = 0
        while (a < b):
            res += f((a + step) / 2) * step
            a += step
        return res, 2

    @staticmethod
    def trapezoids(f, a, b, step):
        res = 0
        while (a < b):
            res += (f(a) + f(a + step)) * step
            a += step
        return res / 2, 2

    @staticmethod
    def simpson(f, a, b, step):
        res = 0
        while (a < b):
            res += (f(a) + 4 * f(a + step) + f(a + 2 * step)) * step
            a += 2 * step
        return res / 3, 4

    @staticmethod
    def runge(f, method, a, b, h, k=0.5):
        I_h, p = method(f, a, b, h)
        I_kh, _ = method(f, a, b, k*h)
        return I_h + (I_h - I_kh) / ((k**p) - 1)

if __name__ == "__main__":
    def T1():
        print("\n"+"-"*10+"Task 1" + "-"*10)

        def cmp(f, points):
            print(f"actual | predicted")
            for (x, y) in points:
                print(f"{y} | {f(x)}")

        f = lambda x: x ** 0.5
        points = [
            (0.1, f(0.1)),
            (1.7, f(1.7)),
            (3.4, f(3.4)),
            (5.1, f(5.1)),
        ]

        LI = Interpolator.lagrange_interpolation(points)
        print(f"f(x) = {LI}")
        # cmp(LI, points)
        X = 3.0
        print(f"Diff at X*={X} is {f(X) - LI(X)}\n\n")

        NI = Interpolator.newton_interpolation(points)
        print(f"f(x) = {NI}")
        # cmp(NI, points)
        X = 3.0
        print(f"Diff at X*={X} is {f(X) - NI(X)}")
        if True:
            import numpy as np
            import matplotlib.pyplot as plt
            x, y = zip(*points)
            x_detailed = np.linspace(min(x), max(x), 400)
            plt.figure(figsize=(10, 6))
            plt.scatter(x, y, color='red', label='Data Points')
            dots = [LI(x_i) for x_i in x_detailed]
            plt.plot(x_detailed, dots, label=f'pol', color='blue')

            plt.legend()
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Approximation')
            plt.grid(True)

            plt.show()

        print("-"*10+'-'*len("Task 1") + "-"*10+"\n\n")

    def T2():
        print("-"*10+"Task 2" + "-"*10)
        points = [
            (0.0, 0.0),
            (1.7, 1.3038),
            (3.4, 1.8439),
            (5.1, 2.2583),
            (6.8, 2.6077),
        ]
        X = 3.0
        SP = Interpolator.spline(points)

        print(f"spline(x) at X*={X} is {SP(X)}")
        if True:
            import numpy as np
            import matplotlib.pyplot as plt
            x, y = zip(*points)
            x_detailed = np.linspace(min(x), max(x), 400)
            plt.figure(figsize=(10, 6))
            plt.scatter(x, y, color='red', label='Data Points')
            dots = [SP(x_i) for x_i in x_detailed]
            plt.plot(x_detailed, dots, label=f'spline', color='blue')

            plt.legend()
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Spline Approximation')
            plt.grid(True)

            plt.show()

        print("-"*10+'-'*len("Task 2") + "-"*10+"\n\n")

    def T3():
        print("-"*10+"Task 3" + "-"*10)
        def loss(f):
            res = 0
            for (x, y) in points:
                res += (y - f(x))**2
            return res
        points = [
            (0.0, 1.0),
            (0.2, 1.0032),
            (0.4, 1.0512),
            (0.6, 1.2592),
            (0.8, 1.8192),
            (1.0, 3.0),
        ]
        LS_1 = Interpolator.squares(points, power=1)
        print(f"f1(x) = {LS_1}\n\t with loss = {loss(LS_1)}")
        LS_2 = Interpolator.squares(points, power=2)
        print(f"f2(x) = {LS_2}\n\t with loss = {loss(LS_2)}")
        if True:
            import numpy as np
            import matplotlib.pyplot as plt

            LS_3 = Interpolator.squares(points, power=3)
            # print(f"f3(x) = {LS_3}\n\t with loss = {loss(LS_3)}")
            LS_4 = Interpolator.squares(points, power=4)
            # print(f"f4(x) = {LS_4}\n\t with loss = {loss(LS_4)}")
            LS_5 = Interpolator.squares(points, power=5)
            # print(f"f4(x) = {LS_5}\n\t with loss = {loss(LS_5)}")

            x, y = zip(*points)
            x_detailed = np.linspace(min(x), max(x), 400)
            plt.figure(figsize=(10, 6))
            plt.scatter(x, y, color='red', label='Data Points')
            #plt.plot(x_detailed, LS_1(x_detailed), label=f'Linear Model, Loss = {loss(LS_1):.4f}', color='blue')
            #plt.plot(x_detailed, LS_2(x_detailed), label=f'Quadratic Model, Loss = {loss(LS_2):.4f}', color='green')
            #plt.plot(x_detailed, LS_3(x_detailed), label=f'Cubic Model, Loss = {loss(LS_3):.4f}', color='pink')
            #plt.plot(x_detailed, LS_4(x_detailed), label=f'Quadrangular Model, Loss = {loss(LS_4):.4f}', color='purple')
            plt.plot(x_detailed, LS_5(x_detailed), label=f'Quadrangular Model, Loss = {loss(LS_5):.4f}', color='gray')

            plt.legend()
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.title('Least Squares Polynomial Approximation')
            plt.grid(True)

            plt.show()
        print("-"*10+'-'*len("Task 3") + "-"*10+"\n\n")

    def T4():
        print("-"*10+"Task 4" + "-"*10)
        points = [
            (-0.2, 1.7722),
            (0.0, 1.5708),
            (0.2, 1.3694),
            (0.4, 1.1593),
            (0.6, 0.9273),
        ]

        DF1 = Derrivative.derivative(points, 1)
        DF2 = Derrivative.derivative(points, 2)
        DDF1 = DF1.derivative()
        DDF2 = DF2.derivative()
        X = 0.2
        print(f"1)f'({X}) ≈ {DF1(X)}")
        print(f"1)f''({X}) ≈ {DDF1(X)}")
        print()
        print(f"2)f'({X}) ≈ {DF2(X)}")
        print(f"2)f''({X}) ≈ {DDF2(X)}")
        print("-"*10+'-'*len("Task 4") + "-"*10+"\n\n")

    def T5():
        print("-"*10+"Task 5" + "-"*10)
        def f(x):
            return 1 / (3 * (x ** 2) + 4 * x + 2)
        def F(x):
            return atan((3 * x + 2) / sqrt(2)) / sqrt(2)
        a, b = -2, 2
        h0 = 1.0
        h1 = 0.5
        print(f"[rectangles, h = {h0}] integral from {a} to {b} is {Integratetor.rectangles(f, a, b, h0)[0]}")
        print(f"[rectangles, h = {h1}] integral from {a} to {b} is {Integratetor.rectangles(f, a, b, h1)[0]}")
        print()
        print(f"[trapezoids, h = {h0}] integral from {a} to {b} is {Integratetor.trapezoids(f, a, b, h0)[0]}")
        print(f"[trapezoids, h = {h1}] integral from {a} to {b} is {Integratetor.trapezoids(f, a, b, h1)[0]}")
        print()
        print(f"[simpson, h = {h0}]    integral from {a} to {b} is {Integratetor.simpson(f, a, b, h0)[0]}")
        print(f"[simpson, h = {h1}]    integral from {a} to {b} is {Integratetor.simpson(f, a, b, h1)[0]}")
        print()
        print(f"[runge+rectangles]    integral from {a} to {b} is {Integratetor.runge(f, Integratetor.rectangles, a, b, h0)}")
        print(f"[runge+trapezoids]    integral from {a} to {b} is {Integratetor.runge(f, Integratetor.trapezoids, a, b, h0)}")
        print(f"[runge+simpson]       integral from {a} to {b} is {Integratetor.runge(f, Integratetor.simpson, a, b, h0)}")
        print()
        p1 = abs(((F(b) - F(a)) - Integratetor.runge(f, Integratetor.simpson, a, b, h0)) / (F(b) - F(a)))
        print(f"Exact value is {F(b) - F(a)} and p = {p1}")
        print("-"*10+'-'*len("Task 5") + "-"*10+"\n\n")
    T1()
    T2()
    T3()
    T4()
    T5()
