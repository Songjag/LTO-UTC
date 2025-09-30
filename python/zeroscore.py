n=int(input())
list=list(map(int,input().split()))
list=[i for i in list if i!=0]
print(' '.join(map(str,sorted(list,reverse=True))))
