def can_find_two_good_markers(t, test_cases):
    results = []
    
    for case in test_cases:
        n = case[0]
        a = case[1]
        b = case[2]

        total_good = sum(b)
        total_bad = sum(a)

        possible = False
        
        for x in range(n):
            good_except_x = total_good - b[x]
            if good_except_x > total_bad:
                continue
            
            valid = True
            for y in range(n):
                if y != x and b[y] > total_bad - a[y]:
                    valid = False
                    break
            
            if valid:
                possible = True
                break
        
        if possible:
            results.append("YES")
        else:
            results.append("NO")
    
    return results

t = int(input())
test_cases = []

for _ in range(t):
    n = int(input())
    a = list(map(int, input().split()))
    b = list(map(int, input().split()))
    test_cases.append((n, a, b))

results = can_find_two_good_markers(t, test_cases)
print("\n".join(results))
