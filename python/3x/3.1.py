a,b,c,n=map(int,input().split())
max_n=max(a,b,c)
total = sum([a, b, c, n])

if total%3==0 and total//3>=max_n:
    print('YES')
else:
    print('NO')