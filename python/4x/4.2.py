a=str(input())
le=0
chan=0
for i in range(len(a)):
    if int(a[i])%2==0:
        chan+=1
    else:
        le+=1
if chan==le:
    print('YES')
else:
    print('NO')
