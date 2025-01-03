import math

class Matrix:
    def __init__(self, data=None, rows=None, cols=None):
        self.cmp_eps = 1e-7
        if data is not None:
            self.rows = len(data)
            self.cols = len(data[0]) if self.rows > 0 else 0
            self.v = [row[:] for row in data]
        elif rows is not None and cols is not None:
            self.rows = rows
            self.cols = cols
            self.v = [[0] * cols for _ in range(rows)]
        else:
            self.rows = 0
            self.cols = 0
            self.v = []

    def __str__(self):
        return "\n".join([" ".join(map(lambda x: f"{x:.2f}", row)) for row in self.v])

    def __getitem__(self, row):
        return self.v[row]

    def __float__(self):
        return self.v[0][0]
    
    def __matmul__(self, other):
        if isinstance(other, Matrix):
            if self.cols != other.rows:
                return Matrix(rows=0, cols=0)
            res = Matrix(rows=self.rows, cols=other.cols)
            for i in range(res.rows):
                for j in range(res.cols):
                    res[i][j] = 0
                    for k in range(self.cols):
                        res[i][j] += self[i][k] * other[k][j]
            return res
        else:
            raise ValueError("unsupported operand type(s) for @: 'Matrix' and '{}'".format(type(other)))

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            res = Matrix(rows=self.rows, cols=self.cols)
            for i in range(self.rows):
                for j in range(self.cols):
                    res[i][j] = self[i][j] * other
            return res
        else:
            raise ValueError("unsupported operand type(s) for *: 'Matrix' and '{}'".format(type(other)))

    def __add__(self, rhs):
        if self.rows != rhs.rows or self.cols != rhs.cols:
            raise ValueError("cannot summ up two matrix with different sizes")
        res = Matrix(rows=self.rows, cols=self.cols)
        for i in range(res.rows):
            for j in range(res.cols):
                res[i][j] = self[i][j] + rhs[i][j]
        return res

    def __sub__(self, rhs):
        if self.rows != rhs.rows or self.cols != rhs.cols:
            raise ValueError("cannot negate two matrix with different sizes")
        res = Matrix(rows=self.rows, cols=self.cols)
        for i in range(res.rows):
            for j in range(res.cols):
                res[i][j] = self[i][j] - rhs[i][j]
        return res
    
    def __pow__(self, n):
        def binary_exponentiation(base, power):
            result = self.eye(base.rows)
            while power > 0:
                if power % 2 == 1:
                    result = result @ base
                base = base @ base
                power //= 2
            return result
        if not self.is_square():
            raise ValueError("Matrix is not square")
        if isinstance(n, int):
            if n < 0:
                self = self.inverse()
            return binary_exponentiation(self, abs(n))
        else:
            raise ValueError("unsupported operand type(s) for **: 'Matrix' and '{}'".format(type(n)))
    
    def norm(self):
        return max([sum(map(abs, row)) for row in self.v])
    
    def swap_rows(self, row1, row2):
        res = Matrix(rows=self.rows, cols=self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                if i == row1:
                    res[row2][j] = self[i][j]
                elif i == row2:
                    res[row1][j] = self[i][j]
                else:
                    res[i][j] = self[i][j]
        return res

    def is_square(self):
        return self.rows == self.cols

    def transpose(self):
        tmp = Matrix(rows=self.cols, cols=self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                tmp[j][i] = self[i][j]
        return tmp

    def eye(self, n):
        res = Matrix(rows=n, cols=n)
        for i in range(n):
            res[i][i] = 1
        return res

    def lu_decomposition(self):
        if not self.is_square():
            raise ValueError("Matrix is not square")
        swp = list()
        L = Matrix(rows=self.rows, cols=self.cols)
        U = Matrix(self.v)
        for k in range(self.rows):
            prev = Matrix(U.v)
            idx = k
            for i in range(k + 1, self.rows):
                if abs(prev[idx][k]) < abs(prev[i][k]):
                    idx = i
            prev = prev.swap_rows(k, idx)
            U = U.swap_rows(k, idx)
            L = L.swap_rows(k, idx)
            swp += [idx]
            for i in range(k + 1, self.rows):
                h = prev[i][k] / prev[k][k]
                L[i][k] = h
                for j in range(k, self.rows):
                    U[i][j] = prev[i][j] - h * prev[k][j]
        for i in range(self.rows):
            L[i][i] = 1
        return L, U, swp
    
    def solve_triag(self, right, upper_triag=False):
        if self.rows != right.rows:
            raise ValueError("Different rows")
        res = Matrix(rows=self.rows, cols=1)
        b = self.rows - 1 if upper_triag else 0
        e = -1 if upper_triag else self.rows
        s = -1 if upper_triag else 1
        for i in range(b, e, s):
            res[i][0] = right[i][0]
            for j in range(self.rows):
                if i == j: continue
                res[i][0] -= self[i][j] * res[j][0]
            res[i][0] = res[i][0] / self[i][i]
        return res

    def solve_gauss(self, right):
        L, U, swp = self.lu_decomposition()
        for i, s in enumerate(swp):
            right = right.swap_rows(i, s)
        z = L.solve_triag(right, False)
        x = U.solve_triag(z, True)
        return x
    
    def inverse(self):
        if not self.is_square() or self.det() == 0:
            raise ValueError("Matrix does not have inverse")
        res = Matrix(rows=self.rows, cols=self.cols)
        for i in range(self.rows):
            right = Matrix(rows=self.rows, cols=1)
            right[i][0] = 1
            colmn = self.solve_gauss(right)
            for j in range(self.rows):
                res[j][i] = colmn[j][0]
        return res

    def det(self):
        _, U, swp = self.lu_decomposition()
        res = 1
        sign = 1 - 2 * (sum([i!=el for i, el in enumerate(swp)]) % 2)
        for i in range(self.rows):
            res *= U[i][i]
        return res * sign
    
    def solve_tridiagonal(self, right):
        p = [-self[0][1] / self[0][0] for _ in range(self.rows)]
        q = [right[0][0] / self[0][0] for _ in range(self.rows)]
        for i in range(1, self.rows):
            if (i != self.rows - 1):
                p[i] = -self[i][i + 1] / (self[i][i] + self[i][i - 1] * p[i - 1])
            else:
                p[i] = 0
            q[i] = (right[i][0] - self[i][i - 1] * q[i - 1]) / (self[i][i] + self[i][i - 1] * p[i - 1])
        res = Matrix(rows=self.rows, cols=1)
        res[res.rows - 1][0] = q[res.rows - 1]
        for i in range(res.rows - 2, -1, -1):
            res[i][0] = p[i] * res[i + 1][0] + q[i]
        return res

    def solve_iteration(self, right, eps=1e-6):
        alpha = Matrix(rows=self.rows, cols=self.rows)
        beta = Matrix(rows=self.rows, cols=1)
        
        for i in range(self.rows):
            for j in range(self.rows):
                if i != j:
                    alpha[i][j] = -self[i][j] / self[i][i]
            beta[i][0] = right[i][0] / self[i][i]
        
        x = beta
        cur = alpha.norm()
        m = cur
        epsk = 2 * eps
        iter_count = 0
        print("m = ", m)
        
        while epsk > eps:
            prev_x = Matrix(x.v)
            x = beta + alpha @ x
            cur_x_diff = x - prev_x
            if m < 1:
                epsk = m / (1 - m) * cur_x_diff.norm()
            else:
                epsk = cur_x_diff.norm()
            iter_count += 1
        
        return x, iter_count

    def solve_seidel(self, right, eps=1e-6):
        n = self.rows
        alpha = Matrix(rows=n, cols=n)
        beta = Matrix(rows=n, cols=1)
        for i in range(n):
            for j in range(n):
                alpha[i][j] = -self[i][j] / self[i][i] if i != j else 0
            beta[i][0] = right[i][0] / self[i][i]

        C = Matrix(rows=n, cols=n)
        B = Matrix(rows=n, cols=n)
        for i in range(n):
            for j in range(n):
                if i <= j:
                    C[i][j] = alpha[i][j]
                else:
                    B[i][j] = alpha[i][j]

        prev = Matrix(beta.v)
        new_b = (self.eye(n) - B)**-1 @ beta
        new_a = (self.eye(n) - B)**-1 @ C
        x = new_a @ prev + new_b

        def calc_eps(prev, x, aplha_norm, c_norm=0):
            if aplha_norm < 1:
                return c_norm / (1 - aplha_norm) * (x - prev).norm()
            else:
                return (x - prev).norm()

        aplha_norm = alpha.norm()
        c_norm = C.norm()
        iter_count = 1
        while calc_eps(prev, x, aplha_norm, c_norm) > eps:
            prev = x
            x = new_a @ prev + new_b
            iter_count += 1
        return x, iter_count
    
    def method_jacobi(self, eps=1e-6):
        A = Matrix(self.v)
        n = self.rows
        epsk = 2 * eps
        vec = self.eye(n)
        iter = 0
        while (epsk > eps):
            cur_i = 1
            cur_j = 0
            for i in range(n):
                for j in range(i + 1, n):
                    if (abs(A[cur_i][cur_j]) < abs(A[i][j])):
                        cur_i = i
                        cur_j = j
            u = Matrix(rows=n, cols=n)
            phi = math.pi / 4
            if (abs(A[cur_i][cur_i] - A[cur_j][cur_j]) > A.cmp_eps):
                phi = 0.5 * math.atan((2 * A[cur_i][cur_j]) / (A[cur_i][cur_i] - A[cur_j][cur_j]))
            for i in range(n):
                u[i][i] = 1
            u[cur_i][cur_j] = -math.sin(phi)
            u[cur_i][cur_i] = math.cos(phi)
            u[cur_j][cur_i] = math.sin(phi)
            u[cur_j][cur_j] = math.cos(phi)
            vec = vec @ u
            A.v = u.transpose() @ A @ u
            epsk = 0
            for i in range(n):
                for j in range(i):
                    epsk += A[i][j] * A[i][j]
            epsk = math.sqrt(epsk)
            iter += 1
        return A, vec, iter
    
    def qr_decomposition(self):
        n = self.rows
        q = self.eye(n)
        r = Matrix(self.v)
        for i in range(n - 1):
            v = Matrix(rows=n, cols=1)
            s = 0
            for j in range(i, n):
                s += r[j][i] * r[j][i]
            v[i][0] = r[i][i] + (1 if r[i][i] > 0 else -1 )* math.sqrt(s)
            for j in range(i + 1, n):
                v[j][0] = r[j][i]
            h = self.eye(n) - (v@v.transpose()) * (2.0 / (v.transpose()@v)[0][0])
            q = q @ h
            r = h @ r

        return q, r

    def qr_eigenvalues(self, eps=1e-6): 
        n = self.rows
        a = Matrix(self.v)
        prev = [0 for _ in range(n)]
        cur  = [2*eps for _ in range(n)]

        def do_step(a):
            for _ in range(100):
                q, r = a.qr_decomposition()
                a = r @ q
            return a

        while (not all([abs(cur[i] - prev[i]) < eps for i in range(n)])):
            a = do_step(a)
            cur = []
            i = 0
            while i < n:
                if (sum([abs(a[j][i]) for j in range(i + 1 , n)]) < 0.01):
                    cur += [a[i][i]]
                else:
                    b = -(a[i][i] + a[i + 1][i + 1])
                    c = a[i][i] * a[i + 1][i + 1] - a[i][i + 1] * a[i + 1][i]
                    d = b * b - 4 * c
                    sgn = complex(1, 0) if (d > 0) else complex(0, 1)
                    d = math.sqrt(abs(d))
                    cur += [(0.5 * (-b - sgn * d)), 0.5 * (-b + sgn * d)]
                    i += 1
                i += 1
            prev = cur
        return prev

class Reader:
    def __init__(self, fn):
        self.filename = fn
    def readSystem(self):
        A, b = [], []
        with open(self.filename, 'r') as f:
            for l in f:
                numbers = [float(num) for num in l.split()]
                A.append(numbers[:-1])
                b.append([numbers[-1]])
        return Matrix(A), Matrix(b)
    def readMatrix(self):
        with open(self.filename, 'r') as f:
            A = [ [float(num) for num in l.split()] for l in f]
        return Matrix(A)


class Lab1:
    def __init__(self):
        self.fn = 'data/t1'
        R = Reader(self.fn + '.txt')
        self.coof, self.right = R.readSystem()
    def Do(self):
        with open(self.fn + '_ans.txt', 'w') as f:
            print(self.coof.solve_gauss(self.right), file=f)

class Lab2:
    def __init__(self):
        self.fn = 'data/t2'
        R = Reader(self.fn + '.txt')
        self.coof, self.right = R.readSystem()
    def Do(self):
        with open(self.fn + '_ans.txt', 'w') as f:
            print(self.coof.solve_tridiagonal(self.right), file=f)

class Lab3:
    def __init__(self):
        self.fn = 'data/t3'
        R = Reader(self.fn + '.txt')
        self.coof, self.right = R.readSystem()
    def Do(self):
        with open(self.fn + '_ans.txt', 'w') as f:
            res, iters = self.coof.solve_iteration(self.right)
            print("[Iterations] Get result:\n", res, sep='', file=f)
            print(f"By {iters} iterations", file=f)
            print("--"*10, file=f)
            res, iters = self.coof.solve_seidel(self.right)
            print("[Seidel] Get result:\n", res, sep='', file=f)
            print(f"By {iters} iterations", file=f)

class Lab4:
    def __init__(self):
        self.fn = 'data/t4'
        R = Reader(self.fn + '.txt')
        self.m = R.readMatrix()
    def Do(self):
        with open(self.fn + '_ans.txt', 'w') as f:
            vals, vecs, iters = self.m.method_jacobi()
            print("[Jakobi] Check:\n", vecs.transpose() @ self.m @ vecs, sep='')
            print("[Jakobi] Get values:\n", vals, sep='', file=f)
            print("[Jakobi] Get vecs:", file=f)
            vecs = vecs.transpose()
            for e in vecs.v:
                tmp = Matrix([e])
                print(tmp.transpose(), file=f)
                print("--"*10, file=f)
            print(f"By {iters} iterations", file=f)
    
class Lab5:
    def __init__(self):
        self.fn = 'data/t5'
        R = Reader(self.fn + '.txt')
        self.m = R.readMatrix()
    def Do(self):
        with open(self.fn + '_ans.txt', 'w') as f:
            q, r = self.m.qr_decomposition()
            print("[QR] A = \n", self.m, sep='')
            print("[QR check] q * r = \n", q @ r, sep='')
            print("[QR dec] Get matrix Q:\n", q, sep='', file=f)
            print("[QR dec] Get matrix R:\n", r, sep='', file=f)
            print("[QR method] Get self-values:", file=f)
            print(self.m.qr_eigenvalues(), file=f)


if __name__ == "__main__":
    l1 = Lab1()
    l1.Do()

    l2 = Lab2()
    l2.Do()

    l3 = Lab3()
    l3.Do()

    l4 = Lab4()
    l4.Do()

    l5 = Lab5()
    l5.Do()
