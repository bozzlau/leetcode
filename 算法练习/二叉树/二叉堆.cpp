#include <iostream>
#include <vector>
using namespace std;

int h[101];
int n;//堆中元素个数

void swap(int x, int y){
    int t;
    t = h[x]; h[x] = h[y]; h[y] = t;
}

//向下调整
void shftdown(int i){
    int t, flag = 0;
    //节点i有左儿子
    while(2*i <= n && flag == 0){
        if (h[i] > h[2*i])
            t = 2*i;//大于左儿子
        else
            t = i;
        //有右儿子
        if (2*i+1 <= n){
            if (h[t] > h[2*i+1]) t = 2*i+1;
        }
        
        if (t != i){
            swap(t, i);
            i = t;
        }else{
            flag = 1;
        }
    }
}

void shftup(int i){
    int flag = 0;
    if (i == 1) return;

    while (i > 1 && flag == 0){
        if (h[i] < h[i/2]){
            swap(i, i/2);
            i = i/2;
        }else{
            flag = 1;
        }
    }
}
//建堆方法1
/*
14
99 5 36 7 22 17 46 12 2 19 25 28 1 92
*/
void create(){
    int i;
    for (i = 1; i <= n; i++) scanf("%d", &h[i]);
    for (i = n/2; i >= 1; i--){
        shftdown(i);
    }
}
//建堆方法2
void create1(){
    for (int i = 1; i <= n; i++){
        scanf("%d", &h[i]);
        shftup(i);
    }
}

void printHeap(){
    for (int i = 1; i <= n; i++){
        printf("%d ",h[i]);
        if (i == n) printf("\n");
    }
}

int main(){
    scanf("%d", &n);
    create();
    printHeap();
}