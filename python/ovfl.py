a,b=map(int,input().split())
if -2**63<int(a+b)<2**63-1:
    print(a+b)
else:
    print("OVERFLOW")