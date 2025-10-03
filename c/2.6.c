#include <stdio.h>

int main(){
    int a;
    scanf("%d", &a);
    
    if (a < 0) {
        printf("INVALID\n");
    }
    else if (((a % 4 == 0) && (a % 100 != 0)) || (a % 400 == 0)) {
        printf("YES\n");
    }
    else {
        printf("NO\n");
    }
    
    return 0;
}
//url:https://laptrinhonline.club/problem/0012dayc