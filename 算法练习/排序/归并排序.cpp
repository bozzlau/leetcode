#include <iostream>
#include <cstring>
using namespace std;

const int N = 11;
void sort(int *, int , int );
int main(){
    int a[N] = {11,6,4,2,7,1,9,5,8,3,10};
    int len = sizeof(a) / sizeof(int);
    sort(a, 0, len-1);
    for (int i = 0; i < N; i++) printf("%d ", a[i]);
}

void sort(int *p, int l, int r){
    if (l == r) return;

    int mid = l + (r - l) / 2;
    sort(p, l, mid);
    sort(p, mid+1, r);

    int i = l, j = mid+1, k = 0;
    int tmp[N] = {};
    while (i <= mid && j <= r){
        if (p[i] < p[j]) tmp[k++] = p[i++];
        else tmp[k++] = p[j++];
    }

    while (i <= mid) tmp[k++] = p[i++];
    while (j <= r) tmp[k++] = p[j++];
    for (i = l, k = 0; i <= r; i++, k++){
        p[i] = tmp[k];
    }
}