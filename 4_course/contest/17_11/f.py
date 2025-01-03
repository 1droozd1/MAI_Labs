k, n = map(int, input().split())
k_2 = 2 * k
k_3 = 3 * k

# Можем ли мы посадить всех типов + можем ли мы перекрыть типами все поле
if n < k_2 - 1 or k_3 < n:
    print('*')
elif n == k_2 - 1:
    print('X-' * (k - 1), 'X', sep='')
else:
    print('-X-' * (n - k_2), 'X-' * (k_3 - n), sep='')