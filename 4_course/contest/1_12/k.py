def max_singing_time(T, A, B, C):
    golden_song_duration = 768
    max_time = 0

    dp = [0] * (T + 1)

    songs = [A, B, C]

    for song in songs:
        for t in range(song, T + 1):
            dp[t] = max(dp[t], dp[t - song] + song)

    for i in range(T + 1):
        if dp[i] > 0:
            max_time = max(max_time, dp[i])

    return max_time + golden_song_duration

t, a, b, c = map(int, input().split())
print(max_singing_time(t, a, b, c))