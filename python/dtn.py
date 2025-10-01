a=str(input())
b=str(input())
count=0
total=len(a)
for i in range(len(a)):
    if a[i]==b[i]:
        count+=1
print(count,"/",total)
print(f"{float(count)/float(total)*10:.1f}")
