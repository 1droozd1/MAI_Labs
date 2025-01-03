from collections import defaultdict

def can_schedule_training(n, m, tM, tK, dependencies):
    graph = defaultdict(list)
    
    for fi, si in dependencies:
        graph[fi].append(si)

    def dfs_paths(start_topic):
        stack = [(start_topic, [])]
        paths = []

        while stack:
            node, path = stack.pop()

            path = path + [node]
            if not graph[node]:
                paths.append(path)
            else:
                for neighbor in graph[node]:
                    stack.append((neighbor, path))
        return paths

    schedule_M = dfs_paths(tM)
    schedule_K = dfs_paths(tK)
    
    all_topics = set(range(1, n + 1))
    for path_M in schedule_M:
        for path_K in schedule_K:
            covered_topics = set(path_M) | set(path_K)
            if covered_topics == all_topics:
                result = ["YES"]
                result.append(str(len(path_M)))
                result.append(" ".join(map(str, path_M)))
                result.append(str(len(path_K)))
                result.append(" ".join(map(str, path_K)))
                return "\n".join(result)
    
    return "NO"

kol_topic, amount_connect = map(int, input().split())
love_topic1, love_topic2 = map(int, input().split())

edges = [tuple(map(int, input().split())) for _ in range(amount_connect)]

print(can_schedule_training(kol_topic, amount_connect, love_topic1, love_topic2, edges))
