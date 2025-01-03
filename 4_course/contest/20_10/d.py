n, k = map(int, input().split())

used = set()
result = []
manual_picks = 0
current_letter = ord('A')
for term in range(n):
    if term % 2 == 0:
        while chr(current_letter) in used:
            current_letter += 1
        result.append(chr(current_letter))
        used.add(chr(current_letter))
    else:
        suggested_letter = input().strip()
        if suggested_letter not in used:
            used.add(suggested_letter)
        else:
            while chr(current_letter) in used:
                current_letter += 1
            used.add(chr(current_letter))
            manual_picks += 1
            
if manual_picks == k:
    print("\n".join(result))
else:
    print("Wrong Answer")