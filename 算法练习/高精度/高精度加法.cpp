#include <iostream>
#include <cstring>
using namespace std;

int a[501], b[501];
int sum[501];
const int len = 3;

int main(){
    char str_a[501], str_b[501];
    cin >> str_a; cin >> str_b;
    int len_a = strlen(str_a), len_b = strlen(str_b);

    for (int i = 0; i < len_a; ++i){
        a[len_a - 1 - i] = str_a[i] - '0';
    }
    for (int i = 0; i < len_b; ++i){
        b[len_b - 1 - i] = str_b[i] - '0';
    }

    int maxlen = len_a > len_b ? len_a : len_b;
    int jw = 0;

    for (int i = 0; i < maxlen; ++i){
        sum[i] += (a[i] + b[i] + jw) % 10;
        jw = (a[i] + b[i] + jw) / 10;
    }
    if (jw == 1){
        sum[maxlen] = jw;
    }
    int idx = sum[maxlen] == 1 ? maxlen : maxlen-1;
    for (int i = 0; i <= idx; ++i){
        cout << sum[idx-i];
    }
    cout << endl;
}