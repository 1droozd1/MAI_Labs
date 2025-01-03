file = open('/Users/dr0ozd/coding/MAI_Labs/4_course/contest/24_11/file.txt', 'r')
per = 0
for line in file:
    line = list(map(int, line.strip().split()))
    line.sort()
    if line[3]**2 > line[1] * line[2] * line[0] or abs(line[0] - line[1]) == abs(line[1] - line[2]) == abs(line[2] - line[3]):
        per += 1
print(per)