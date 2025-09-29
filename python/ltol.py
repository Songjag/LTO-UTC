n = int(input())

for i in range(1, n + 1):
    if i % 2 == 1:
        print(i)
    else:
        s = "L"
        if i % 4 == 0:
            s += "T"
        if i % 8 == 0:
            s += "O"
        if i % 16 == 0:
            s += "L"
        print(s)
#full test