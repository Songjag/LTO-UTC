def so_nguyen_to(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True
n=int(input())
list1=[]
for _ in range(n):
    a,b=map(int,input().split())
    list1.append([a,b])
for  list in list1:
    a,b=list[0],list[1]
    list2=[]
    for i in range(a,b+1):
        if so_nguyen_to(i):
            list2.append(i)
    print(*list2)
    