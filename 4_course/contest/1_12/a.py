def max_power_level(n, gates):
    max_power = 0
    min_power = 0

    operations = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y
    }
    
    for op1, val1, op2, val2 in gates:

        val1 = int(val1)
        val2 = int(val2)

        power1_from_max = operations[op1](max_power, val1)
        power1_from_min = operations[op1](min_power, val1)
        power2_from_max = operations[op2](max_power, val2)
        power2_from_min = operations[op2](min_power, val2)

        max_power = max(power1_from_max, power1_from_min, power2_from_max, power2_from_min)
        min_power = min(power1_from_max, power1_from_min, power2_from_max, power2_from_min)

    return max_power

amount_levels = int(input())
gates = [input().split() for _ in range(amount_levels)]
print(max_power_level(amount_levels, gates))