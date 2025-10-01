n=int(input())
le=[]
chan=[]
for i in range(n):
    a=int(input())
    if a%2==0:
        chan.append(a)
    else:
        le.append(a)
chan=chan[::-1]
print(*le,*chan)

#url: https://laptrinhonline.club/problem/basic2