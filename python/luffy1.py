def uoc(n):
    ds=[]
    for i in range(1,n+1):
        if n%i==0 and i%2==1:
            ds.append(i)
    return sum(ds)
n=int(input())
ds=[]
for _ in range(n):
    a,b=map(int,input().split())
    cache=0
    for i in range(a,b+1):
        cache+=(uoc(i))
    ds.append(cache)
        
print('\n'.join(map(str,ds)))
 

