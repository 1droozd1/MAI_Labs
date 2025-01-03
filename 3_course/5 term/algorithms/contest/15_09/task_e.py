def fun(number):
    new_number = '1'

    while int(new_number) < number:
        new_number += '1'
    result = number - int(new_number)

    if result < 0:
        new_number = new_number[:-1]
        result = number - int(new_number)

    if len(str(number)) == len(new_number) and len(str(result)) == len(new_number):
        return result
    elif len(str(number)) == len(new_number) + 1 and len(str(result)) + 1 == len(str(number)):
        return result
    else:
        return 0

number = int(input())
result = 1
while number > 0:
    number = fun(number)
    if number == 0:
        break
    else:
        result += 1

print(result)