def count_straights(n, m, s, cards_on_table):
    unique_cards = sorted(set(cards_on_table))
    count = 0
    num_cards = len(unique_cards)

    for i in range(num_cards):
        min_card = unique_cards[i]

        if i + m - s - 1 >= num_cards:
            continue
        
        max_card_from_table = unique_cards[i + m - s - 1]

        lower_bound = max(1, max_card_from_table - m + 1)
        upper_bound = min(n - m + 1, min_card)

        if i > 0:
            lower_bound = max(lower_bound, unique_cards[i - 1] + 1)

        if lower_bound <= upper_bound:
            count += upper_bound - lower_bound + 1

    return count

n, m, s = map(int, input().split())
cards_on_table = list(map(int, input().split()))
result = count_straights(n, m, s, cards_on_table)
print(result)
