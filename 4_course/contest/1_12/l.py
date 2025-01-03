from collections import deque

def survivors_in_rock_paper_scissors(n, m, moves):
    team_a = list(moves[:n][::-1])
    team_b = list(moves[n:])

    def determine_winner(move1, move2):
        if move1 == move2:
            return 0
        elif (move1 == 'R' and move2 == 'S') or \
             (move1 == 'S' and move2 == 'P') or \
             (move1 == 'P' and move2 == 'R'):
            return 1
        else:
            return -1

    def simulate(team_a, team_b):
        team_a = deque(team_a)
        team_b = deque(team_b)
        while team_a and team_b:
            move_a = team_a[0]
            move_b = team_b[0]
            result = determine_winner(move_a, move_b)

            if result == 1:
                team_b.popleft()
            elif result == -1:
                team_a.popleft()
            else:
                team_a_copy, team_b_copy = deque(team_a), deque(team_b)
                team_b_copy.popleft()
                team_a_copy.popleft()
                return simulate(team_a, team_b_copy) + simulate(team_a_copy, team_b)
            
        return len(team_a) + len(team_b)

    return simulate(team_a, team_b)

n, m = map(int, input().split())
moves = list(input())
print(survivors_in_rock_paper_scissors(n, m, moves))