import math
import numpy as np
from matrix import Matrix


class BoundaryCond:
    def __init__(self, y0, yn, alph, betta, gamm, delt, eps=1e-6):
        self.y0 = y0
        self.yn = yn

        self.alph = alph
        self.bett = betta
        self.gamm = gamm
        self.delt = delt
        self.epsilon = eps

    def get_Y(self):
        print(self.yn)
        
    
    def set_yn(self, yn):
        self.yn = yn

class EqSolver:
    def __init__(self, F, Y, a, b):
        self.F = F # система
        self.Y = Y # y([x1,x2]) = [y0, y1]
        self.a = a # левая граница
        self.b = b # праввая граница
    
    @staticmethod
    def sum_list(a: list, b: list) -> list:
        assert len(a) == len(b)
        return list([a[i] + b[i] for i in range(len(a))])

    def ans_format(self, Y):
        x, y, z = zip(*self.shooting(y0=1, yn=26, alph=0, bett=1, delt=1, gamm=-1, h=0.1, n0=10, n1=8, eps=0.00001))
        return x[::2], y[::2], z[::2]
    @staticmethod
    def mul_list(n: float, a: list) -> list:
        return list([n * a[i] for i in range(len(a))])

    def euler_explicit(self, h):
        Y = self.Y
        x = self.a
        res = [(x, Y[0], Y[1])]
        while x <= self.b:
            next = self.F([x] + Y)
            Y = EqSolver.sum_list(Y, EqSolver.mul_list(h, next))
            x += h
            res += [(x,  Y[0], Y[1])]
        return res

    def euler_with_recalc(self, h):
        Y = self.Y
        x = self.a
        res = [(self.a, Y[0], Y[1])]
        while x <= self.b:
            next1 = self.F([x] + Y)
            _Y_ = EqSolver.sum_list(Y, EqSolver.mul_list(h, next1))
            next2 = self.F([x + h] + _Y_)
            Y = EqSolver.sum_list(
                Y,
                EqSolver.mul_list(
                    h/2,
                    EqSolver.sum_list(
                        next1,
                        next2
                    )
                )
            )
            x += h
            res += [(x,  Y[0], Y[1])]
        return res

    def runge_kutta(self, h, max_steps=None):
        x = self.a
        Y = self.Y
        res = [(x, Y[0], Y[1])]
        iter = 1
        while x <= self.b:
            if (not (max_steps is None)) and (max_steps <= iter):
                break
            K1 = EqSolver.mul_list(h, self.F([x] + Y))
            K2 = EqSolver.mul_list(h, self.F([x + h/2] + EqSolver.sum_list(Y, EqSolver.mul_list(1/2, K1))))
            K3 = EqSolver.mul_list(h, self.F([x + h/2] + EqSolver.sum_list(Y, EqSolver.mul_list(1/2, K2))))
            K4 = EqSolver.mul_list(h, self.F([x + h] + EqSolver.sum_list(Y, EqSolver.mul_list(1, K3))))

            Res = EqSolver.sum_list(Y, EqSolver.mul_list(1/6, K1))
            Res = EqSolver.sum_list(Res, EqSolver.mul_list(1/3, K2))
            Res = EqSolver.sum_list(Res, EqSolver.mul_list(1/3, K3))
            Y = EqSolver.sum_list(Res, EqSolver.mul_list(1/6, K4))

            x += h
            iter += 1
            res += [(x,  Y[0], Y[1])]
        return res
    
    def adams(self, h):
        Res = self.runge_kutta(h, max_steps=4)
        x = Res[-1][0]
        Y = Res[-1][1:]
        while x <= self.b:
            F1 = self.F(Res[-4])
            F2 = self.F(Res[-3])
            F3 = self.F(Res[-2])
            F4 = self.F(Res[-1])
            
            Tmp = EqSolver.sum_list(Y, EqSolver.mul_list(h*55/24, F4))
            Tmp = EqSolver.sum_list(Tmp, EqSolver.mul_list(h*(-59)/24, F3))
            Tmp = EqSolver.sum_list(Tmp, EqSolver.mul_list(h*37/24, F2))
            Y = EqSolver.sum_list(Tmp, EqSolver.mul_list(h*(-9)/24, F1))

            x += h
            Res += [(x,  Y[0], Y[1])]
        return Res

    def runge_romberg(self, h, method='euler'):
        acc = {
            'adams': (self.adams, 4),
            'runge_kutta': (self.runge_kutta, 4),
            'euler_cauchy': (self.euler_with_recalc, 2),
            'euler': (self.euler_explicit, 1)
        }
        if not method in acc.keys():
            print("Bad mathod name")
            return []
        f, p = acc[method]
        _, y1, _ = zip(*f(h))
        _, y2, _ = zip(*f(h/2))
        p = 4
        k = 2
        return [(y - yk) / (k**p - 1) for (y, yk) in zip(y1, y2[::k])]
    
    def shooting(self, y0, yn, alph, bett, delt, gamm, h, n0=1, n1=0.8, eps=0.0001):
        def solve(n_):
            return EqSolver(self.F, [n_, (y0 - alph * n_) / bett], self.a, self.b).runge_kutta(h)
        def PHI(n_):
            _, y, z = zip(*solve(n_))
            return delt * y[-1] + gamm * z[-1] - yn

        phi0 = PHI(n0)
        phi1 = PHI(n1)
        while abs(phi1) > eps:
            n = n1 - ((n1 - n0) / (phi1 - phi0)) * phi1
            n0, n1 = n1, n
            phi0, phi1 = phi1, PHI(n1)
        return solve(n1)
    
    def finite_difference_method(self, p, q, f, y0, yn, alph, bett, delt, gamm, h):
        x = np.arange(self.a, self.b + h, h)
        n = len(x)
        rows = [alph * h - bett, bett] + [0 for _ in range(2, n)]
        A = [rows]
        B = [y0 * h]
        for i in range(1, n - 1):
            rows = []
            B += [f(x[i]) * h ** 2]
            for j in range(n):
                if j == i - 1:
                    rows.append(1 - p(x[i]) * h / 2)
                elif j == i:
                    rows.append(q(x[i]) * h ** 2 - 2)
                elif j == i + 1:
                    rows.append(1 + p(x[i]) * h / 2)
                else:
                    rows.append(0)
            A += [rows]
        rows = []
        B.append(yn * h)
        for i in range(n):
            if i == n - 1: rows.append(delt * h + gamm)
            elif i == n - 2: rows.append(-gamm)
            else: rows.append(0)
        A += [rows]
        A = Matrix(A)
        B = Matrix([[i] for i in B])
        y = A.solve_triag(B)
        return self.ans_format(y)
        




def arrays_as_table(*arrays):
    arrays = [list(arr) for arr in arrays]

    max_length = max(len(arr) for arr in arrays)
    arrays = [arr + [None]*(max_length - len(arr)) for arr in arrays]
    res = ""
    for i in range(max_length):
        row = []
        for arr in arrays:
            element = arr[i]
            if element is None:
                row.append("-")
            else:
                row.append(f"{element:5f}")
        res += '\t'.join(row) + '\n'
    return res




if __name__ == "__main__":
    def T1():
        """
        x^2 y'' + (x + 1)y' - y = 0

        z = y'
        z' = y''

        
        y' = z
        z' = (y - (x + 1)z) / (x**2)
        F(Х) = {z, (y - (x + 1)z) / (x**2)}, где X = (x, y, z)

        """
        E = EqSolver(
            F=lambda X : [X[2], (X[1] - (X[0] + 1)*X[2]) / (X[0]**2)],
            Y=[2 + math.e, 1],
            a=1,
            b=2,
        )

        h = 0.1

        _, y1, _ = zip(*E.euler_explicit(h=h))

        _, y2, _ = zip(*E.euler_with_recalc(h=h))

        x, y3, _ = zip(*E.runge_kutta(h=h))

        x, y4, _ = zip(*E.adams(h=h))

        def f(x):
            return x + 1 + x * math.exp(1/x)
        orig = [f(i) for i in x]

        print("euler_explicit\t\teuler_with_recalc\trunge_kutta\t\tadams\t\t\toriginal\t\teps")
        print('-'*140)
        print(arrays_as_table(y1, y2, y3, y4, orig, E.runge_romberg(h=h, method='runge_kutta')))

        import matplotlib.pyplot as plt
        plt.plot(x, orig, label='original')
        plt.plot(x, y1, label='euler_explicit')
        plt.plot(x, y2, label='euler_with_recalc')
        plt.plot(x, y3, label='runge_kutta')
        plt.plot(x, y4, label='adams')
        plt.legend()
        plt.show()

    def T2():
        E1 = EqSolver(
            F=lambda X : [X[2], (X[1] - (X[0] + 1)*X[2]) / (X[0]**2)],
            Y=[2 + math.e, 1],
            a=1,
            b=2,
        )
        '''
        x(x**2 + 6)y'' - 4(x**2+3)y' + 6x*y
        y' = z
        z' = (4*y*(x**2+3) - 6x*y) / (x**3 + 6*x)

        
        '''
        E = EqSolver(
            F=lambda x : [x[2], (4*x[2]*(x[0]**2+3) - 6*x[0]*x[1]) / (x[0]**3 + 6*x[0])],
            Y=[],
            a=1,
            b=4,
        )
        x, y, z = zip(*E.shooting(y0=1, yn=26, alph=0, bett=1, delt=1, gamm=-1, h=0.2, n0=1, n1=0.8, eps=0.01))
        def f(x):
            return 21*x**3 -31 * x**2 - 62 - (x - 4)**2/100
        E = EqSolver(
            F=lambda x : [x[2], (4*x[2]*(x[0]**2+3) - 6*x[0]*x[1]) / (x[0]**3 + 6*x[0])],
            Y=[],
            a=1,
            b=4,
        )
        x, y1, z = E.finite_difference_method(
            p=lambda x: -4*(x**2+3)/(x**3 + 6*x),
            q=lambda x: 6*x/(x**3 + 6*x),
            f=lambda x: 0,
            y0=1, yn=26, alph=0, bett=1, delt=1, gamm=-1, h=0.2)
        runge_romb = E1.runge_romberg(h=0.05)
        print("x\t\tshooting\tdifference\tf(x)\t\trunge_romberg")
        print(arrays_as_table(x, y1, y, [f(i) for i in x], runge_romb[:len(x)]))

    T1()  
    T2()
