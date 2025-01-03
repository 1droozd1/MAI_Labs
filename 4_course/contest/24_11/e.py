def check(list_of_highs, m, k):
    amount_highs = 0

    for i in range(len(list_of_highs) - 1):
        if abs(list_of_highs[i] - list_of_highs[i + 1]) <= k:
            continue
        else:
            amount_highs += 1
    
    return amount_highs + 1

def res(list_of_highs, m):
    left = 0
    right = max(list_of_highs) - min(list_of_highs)
    res = -1

    while left <= right:
        k = (left + right) // 2
        amount_highs = check(list_of_highs, m, k)
        if amount_highs == m:
            res = k
            right = k - 1
        else:
            if amount_highs < m:
                right = k - 1
            else:
                left = k + 1
    return res

n, m = map(int, input().split())
list_of_highs = list(map(int, input().split()))
print(res(list_of_highs, m))