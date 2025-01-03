def knapsack_strong(n, W, items):
    max_weight = (3/2) * W
    
    dp = {0: 0}
    item_selection = {0: []}
    
    for i in range(n):
        weight, cost = items[i]
        current_items = list(dp.items())
        
        for current_cost, current_weight in current_items:
            new_cost = current_cost + cost
            new_weight = current_weight + weight
            
            if new_weight <= max_weight:
                if new_cost not in dp or new_weight < dp[new_cost]:
                    dp[new_cost] = new_weight
                    item_selection[new_cost] = item_selection[current_cost] + [i + 1]

    best_cost = -1
    for cost in dp.keys():
        if dp[cost] <= max_weight:
            best_cost = max(best_cost, cost)

    if best_cost == -1:
        return 0, []

    selected_items = item_selection[best_cost]
    return best_cost, selected_items


def solve_knapsack_problem(test_cases):
    results = []
    
    for n, W, items in test_cases:
        _, selected_items = knapsack_strong(n, W, items)
        results.append((len(selected_items), selected_items))
    
    return results


kol_tests = int(input())
test_cases = []

for _ in range(kol_tests):
    n, W = map(int, input().split())
    items = [tuple(map(int, input().split())) for _ in range(n)]
    test_cases.append((n, W, items))

results = solve_knapsack_problem(test_cases)

for count, selected in results:
    print(count)
    print(' '.join(map(str, selected)))
