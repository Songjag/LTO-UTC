s = input()    
if s != "" and all('a' <= c <= 'z' for c in s):
    print("YES")
else:
    print("NO")
