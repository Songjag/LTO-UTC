a,b,c=map(float,input().split())
print(a+b+c)
def check(a,b,c):
    if a+b>c and a+c>b and b+c>a:
        return True
    return False
def s(a,b,c):
    return ((a+b)*c)/2
def p(a,b,c):
    return a+b+c
if check(a,b,c):
    print("Chu vi = ",p(a,b,c))
else:
    print("Dien tich = ",s(a,b,c))