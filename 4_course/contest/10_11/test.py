from collections import defaultdict

def can_schedule_training(n, m, tM, tK, dependencies):
    # Строим граф зависимостей для преподавателя Медера
    graph_M = defaultdict(list)
    graph_K = defaultdict(list)
    
    for fi, si in dependencies:
        if fi != tK:
            graph_M[fi].append(si)

    for fi, si in dependencies:
        if fi != tM:
            graph_K[fi].append(si)
    
    # Функция для поиска листьев в графе
    def find_leaves(graph):
        leaves = []
        for node in range(1, n+1):
            if len(graph[node]) == 0 and node != tM and node != tK:
                leaves.append(node)
        return leaves

    leaves_M = find_leaves(graph_M)
    leaves_K = find_leaves(graph_K)
    
    # Теперь соединяем все листья двух графов между собой
    for leaf_M in leaves_M:
        for leaf_K in leaves_K:
            graph_M[leaf_M].append(leaf_K)  # Соединяем листья между собой
    
    # Функция для нахождения пути с обходом всех вершин
    def dfs_paths(start, graph):
        visited = set()
        path = []
        def dfs(node):
            visited.add(node)
            path.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor)
        dfs(start)
        return path
    
    # Находим путь для Медера и Кылычбека
    path_M = dfs_paths(tM, graph_M)
    path_K = dfs_paths(tK, graph_K)
    
    # Проверяем, что все вершины покрыты
    all_covered = set(path_M) | set(path_K)
    if len(all_covered) == n:
        result = ["YES"]
        result.append(str(len(path_M)))
        result.append(" ".join(map(str, path_M)))
        result.append(str(len(path_K)))
        result.append(" ".join(map(str, path_K)))
        return "\n".join(result)
    else:
        return "NO"


# Ввод
kol_topic, amount_connect = map(int, input().split())
love_topic1, love_topic2 = map(int, input().split())

edges = [tuple(map(int, input().split())) for _ in range(amount_connect)]

# Вывод
print(can_schedule_training(kol_topic, amount_connect, love_topic1, love_topic2, edges))