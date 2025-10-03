a=int(input())
if a<0:
    print('INVALID ')
elif a%4==0 and a%100!=0 or a%400==0:
    print('YES')
else: 
    print('NO')
#url :https://laptrinhonline.club/problem/0012dayc