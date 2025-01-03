string = 'x1x2x3x4x0x'
operations = '+/-*()_'
result = ''


for operation1 in operations:
    for operation2 in operations:
        for operation3 in operations:
            for operation4 in operations:
                for operation5 in operations:
                    for operation6 in operations:
                        string = string.replace('x', operation1, 1)
                        string = string.replace('x', operation2, 1)
                        string = string.replace('x', operation3, 1)
                        string = string.replace('x', operation4, 1)
                        string = string.replace('x', operation5, 1)
                        string = string.replace('x', operation6, 1)
                        string = string.replace('_', '')
                        try:
                            if eval(string) == 100:
                                result = str(string)
                                break
                        except SyntaxError:
                            pass
                        except ZeroDivisionError:
                            pass
                        except TypeError:
                            pass
                        
                        string = 'x1x2x3x4x0x'

print(result)