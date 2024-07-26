def atoi(s):
    return int(s)

result = '1'.join([str(atoi(str(2*int(x))) + 1) for x in ['4', '3', '7']])
print(result)
