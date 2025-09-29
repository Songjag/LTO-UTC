k2,k3,k5,k6=map(int,input().split())
so256=min(k2,k5,k6)
k2-=so256
so32=min(k3,k2)
print(so256*256+so32*32)