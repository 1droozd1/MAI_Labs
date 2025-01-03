def generate_dna(n):
    length = 2 ** n
    dna = []

    # Генерируем ДНК, чтобы они были уникальными на каждом шаге
    for i in range(length):
        # Генерируем строку, где в первых половинах повторяются 0 и 1
        if i < length // 2:
            dna.append('0')
        else:
            dna.append('1')

    # Перемешиваем части, чтобы получить разнообразие
    for i in range(1, n):
        for j in range(2 ** (n - i)):
            if j % 2 == 0:
                dna[j * 2**i : (j + 1) * 2**i] = ['0'] * 2**i
            else:
                dna[j * 2**i : (j + 1) * 2**i] = ['1'] * 2**i

    return ''.join(dna)

n = int(input().strip())
print(generate_dna(n))
