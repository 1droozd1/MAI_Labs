amount_words = int(input())
words = input().split()
errors = 0
list_glas = 'aeiouy'

for word in words:

    count_error_glass = 0
    count_error_word1 = 0
    count_error_word2 = 0

    if len(word) <= 1:
        for char in word:
            if char not in list_glas:
                count_error_glass += 1
    else:
        for char in word:
            if char not in list_glas:
                count_error_glass += 1

        if word[0] in list_glas:
            type_pred = 0
            type_pred2 = 1
            count_error_word2 += 1

        else:
            type_pred = 1
            type_pred2 = 0
            count_error_word2 += 1

        for i in range(1, len(word)):
            if type_pred == 0:
                if word[i] in list_glas:
                    count_error_word1 += 1
                type_pred = 1
            else:
                if word[i] not in list_glas:
                    count_error_word1 += 1
                type_pred = 0

        for i in range(1, len(word)):
            if type_pred2 == 0:
                if word[i] in list_glas:
                    count_error_word2 += 1
                type_pred2 = 1
            else:
                if word[i] not in list_glas:
                    count_error_word2 += 1
                type_pred2 = 0

    errors += min(count_error_glass, count_error_word1, count_error_word2)
print(errors)
