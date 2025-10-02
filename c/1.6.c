#include <stdio.h>
int main(){
    long long a,b;
    long long tong,hieu,tich;
    float thuong;
    scanf("%lld %lld",&a,&b);
    tong=a+b;
    hieu=a-b;
    tich=a*b;
    thuong=(float)a/b;
    printf("%lld %lld %lld %.2f\n",tong,hieu,tich,thuong);
    return 0;
}
//url: https://laptrinhonline.club/problem/0006dayc