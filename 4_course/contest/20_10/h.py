import math

def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

def connect(parent, rank, x, y):
    rootX = find(parent, x)
    rootY = find(parent, y)
    
    if rootX != rootY:
        if rank[rootX] > rank[rootY]:
            parent[rootY] = rootX
        elif rank[rootX] < rank[rootY]:
            parent[rootX] = rootY
        else:
            parent[rootY] = rootX
            rank[rootX] += 1

n, k = map(int, input().split())

parent = list(range(n))
rank = [0] * n

for _ in range(k):
    a, b = map(int, input().split())
    a -= 1
    b -= 1
    connect(parent, rank, a, b)

component_size = {}
for i in range(n):
    root = find(parent, i)
    if root not in component_size:
        component_size[root] = 0
    component_size[root] += 1

p = 0
for size in component_size.values():
    p += size * (size - 1) // 2

q = n * (n - 1) // 2

if p == 0:
    print("0 1")
else:
    gcd = math.gcd(p, q)
    print(f"{p // gcd} {q // gcd}")
