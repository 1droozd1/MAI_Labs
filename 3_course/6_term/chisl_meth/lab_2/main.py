from matrix import Matrix
import math

class Solver:
    def __init__(self, f, df):
        self.f = f
        self.df = df

    @classmethod
    def arg_max(cls, f, l, r, eps=1e-6):
        iter = 0
        while r - l > eps:
            a, b = (r + 2 * l) / 3, (2 * r + l)/3
            if f(a) < f(b): l = a
            else: r = b
            iter += 1
        return (l + r) / 2, iter

    @classmethod
    def maximize(cls, f, l, r, eps=1e-6):
        return f(cls.arg_max(f, l, r, eps)[0])

    def newton(self, x0, eps=1e-6):
        xk = x0 - self.f(x0) / self.df(x0)
        iter = 0
        while abs(xk - x0) > eps:
            x0 = xk
            xk = x0 - self.f(x0) / self.df(x0)
            iter += 1
        return xk, iter

    def iteration(self, l, r, eps=1e-6):
        x = (l + r) / 2
        xk = self.f(x)
        iter = 0
        mx = self.arg_max(self.df, l, r)[0]
        q = self.df(mx)
        fix = q / (1 - q)
        while fix * abs(xk - x) > eps:
            x = xk
            xk = self.f(x)
            iter +=1
        return xk, iter

    def newton_sys(self, x, eps=1e-6):
        def next(xk):
            A = Matrix(rows=n, cols=n)
            B = Matrix(rows=n, cols=1)
            for i in range(len(self.df)):
                for j in range(len(self.df[i])):
                    A[i][j] = self.df[i][j](xk)
                B[i][0] = -self.f[i](xk)
            dx = A.solve_gauss(B)
            return xk + dx
        n = x.rows
        prev = Matrix(x.v)
        cur = next(prev)
        iter = 1
        while ((cur - prev).norm() > eps):
            prev = cur
            cur = next(prev)
            iter +=1
        return cur, iter

    def iteration_sys(self, ls, rs, eps=1e-6):
        n = len(self.f)
        x0 = Matrix([[(rs[i] + ls[i])/2 for i in range(n)]]).transpose()
        def get_J_inv():
            A = Matrix(rows=n, cols=n)
            for i in range(len(self.df)):
                for j in range(len(self.df[i])):
                    A[i][j] = self.df[i][j](x0)
            return A**(-1)

        def next(xk, T):
            return xk - T @ Matrix([[self.f[0](xk)],[self.f[1](xk)]])

        T = get_J_inv()
        def get_norm_q():
            f00 = lambda x: 2 * 3 * x - 1
            f01 = lambda x: 2 * x
            f10 = lambda x: -1/math.cos(x)
            f11 = lambda x: 1
            Q = T.eye(n) - T @ Matrix([
                [self.maximize(f00, ls[0], rs[0]), self.maximize(f01, ls[1], rs[1])],
                [self.maximize(f10, ls[0], rs[0]), self.maximize(f11, ls[1], rs[1])]
            ])
            return Q.norm()
        
        Q_norm = get_norm_q()
        # if (Q_norm > 1):
        #     return None
        prev = x0
        cur = next(prev, T)
        iter = 1
        while (1 / (1 - Q_norm) * (cur - prev).norm() > eps):
            prev = cur
            cur = next(prev, T)
            iter +=1
        return cur, iter

if __name__ == "__main__":
    def T1():
        s = Solver(lambda x: x**6 - 5*x - 2, lambda x: 6*x**5 - 5)
        ddf = lambda x: -125/(36 * (2 + 5 * x)**(11/6))
        l, r = 1, 2
        if (s.f(l) * ddf(l) > 0):
            x0 = l
        else:
            x0 = r
        print("Solve eq: x = {} by Iteration method with {} iterations".format(*s.newton(x0)))

    def T2():
        s = Solver(lambda x: (5*x + 2)**(1/6), lambda x: 5/(6 * (5 * x + 2)**(5/6)))
        print("Solve eq: x = {} by Iteration method with {} iterations".format(*s.iteration(1, 2)))
    
    def T3(a=3):
        f = [
            lambda x: a * x[0][0]**2 - x[0][0] + x[1][0]**2 - 1,
            lambda x: x[1][0] - math.tan(x[0][0]),
        ]
        df = [
            [lambda x: 2 * a * x[0][0] - 1,  lambda x: 2 * x[1][0] ],
            [lambda x: -1/math.cos(x[0][0]), lambda x: 1],
        ]
        x0 = Matrix([[1], [1]])
        s = Solver(f, df)

        ans, iter = s.newton_sys(x0)
        print("Get answer: x = ({}, {}) by Newton method with {} iterations".format(ans[0][0], ans[1][0], iter))

    def T4(a=3):
        phi = [
            lambda x: a * x[0][0]**2 - x[0][0] + x[1][0]**2 - 1,
            lambda x: x[1][0] - math.tan(x[0][0]),
        ]
        dphi = [
            [lambda x: 2 * a * x[0][0] - 1,  lambda x: 2 * x[1][0] ],
            [lambda x: -1/math.cos(x[0][0]), lambda x: 1],
        ]

        s = Solver(phi, dphi)

        ans, iter = s.iteration_sys([0.4, 0.4], [0.7, 0.8])
        print("Get answer: x = ({}, {}) by Iterations method with {} iterations".format(ans[0][0], ans[1][0], iter))


    T1()
    T2()
    T3()
    T4()





#     def Solve_for_Sonya(a=2):
#         phi = [
#             lambda x: a * x[0][0]**2 - x[1][0] + x[1][0]**2 - a,
#             lambda x: x[0][0] - math.sqrt(x[1][0] + a) + 1,
#         ]

#         dphi = [
#             [lambda x: 2 * a * x, lambda y: -1 + 2 * y],
#             [lambda x: 1, lambda y: 1 - 0.5 / math.sqrt(y + a)]
#         ]

#         #(0.84, 1.406)
#         ls = [0.83, 1.3]
#         rs = [0.85, 1.5]
        
#         eps=1e-3
#         n = 2
#         # x0 = Matrix([[(rs[i] + ls[i])/2 for i in range(n)]]).transpose()
#         x0 = Matrix([[0.90],[1.606]])
#         def get_J_inv():
#             x, y = x0[0][0], x0[1][0]
#             A = Matrix([
#                 [dphi[0][0](x), dphi[0][1](y)],
#                 [dphi[1][0](x), dphi[1][1](y)],
#             ])
#             return A**(-1)

#         def next(xk, T):
#             return xk - T @ Matrix([[phi[0](xk)],[phi[1](xk)]])

#         T = get_J_inv()
#         print(T)


#         # print(T.eye(n) - T @ Matrix([
#         #         [Solver.maximize(dphi[0][0], ls[0], rs[0]), Solver.maximize(dphi[0][1], ls[1], rs[1])],
#         #         [Solver.maximize(dphi[1][0], ls[0], rs[0]), Solver.maximize(dphi[1][1], ls[1], rs[1])]
#         #     ]))
#         # return 0
#         def get_norm_q():
#             Q = T.eye(n) - T @ Matrix([
#                 [Solver.maximize(dphi[0][0], ls[0], rs[0]), Solver.maximize(dphi[0][1], ls[1], rs[1])],
#                 [Solver.maximize(dphi[1][0], ls[0], rs[0]), Solver.maximize(dphi[1][1], ls[1], rs[1])]
#             ])
#             print(Q)
#             return Q.norm()
        
#         Q_norm = get_norm_q()
#         print("Q norm = ", Q_norm)
#         prev = x0
#         cur = next(prev, T)
#         iter = 1
#         print("\n\n")
#         while (1 / (1 - Q_norm) * (cur - prev).norm() > eps) and iter < 5:
#             print(cur)
#             print('-'*30)
#             prev = cur
#             cur = next(prev, T)
#             iter +=1
#         print(cur)
#         print(iter)
#         return cur
#     a = 2
#     phi = [
#             lambda x: a * x[0][0]**2 - x[1][0] + x[1][0]**2 - a,
#             lambda x: x[1][0] - math.sqrt(x[1][0] + a) + 1,
#         ]
#     X = Solve_for_Sonya()
#     # print(phi[0](X))
#     # print(phi[1](X))
    



# """
# phi = [
#             lambda x: 1/6 * (1 + math.sqrt(13 - 12*x[1][0]**2)),
#             lambda x: math.tan(x[0][0]),
#         ]
#         dphi = [
#             [lambda x: 0,  lambda x: -(2*math.sqrt(3)*x)/ ((math.sqrt(math.sqrt(39) - 6*x) * math.sqrt(math.sqrt(39) + 6*x))) ],
#             [lambda x: 1/math.cos(x[0][0]), lambda x: 0],
#         ]
# """