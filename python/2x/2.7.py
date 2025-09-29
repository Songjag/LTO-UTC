try:
    a = input()
    if len(a) == 1 and a.isalnum():
        print("YES")
    else:
        print("NO")
except UnicodeDecodeError:
    print("NO")