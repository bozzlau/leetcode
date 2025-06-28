#include <iostream>
#include <cstring>
using namespace std;

int a[10086], b[10086], res[10086];

int main(){
    string s1, s2;
    bool is_less_0 = false;
    cin >> s1; cin >> s2;

    int len_s1 = s1.size(), len_s2 = s2.size();
    if (len_s1 < len_s2){
        is_less_0 = true;
        string tmp = s1;
        s1 = s2;
        s2 = tmp;
    }else if(len_s1 == len_s2){
        for (int i = 0; i < len_s1; ++i){
            if (s1[i] < s2[i]){
                is_less_0 = true;
                string tmp = s1;
                s1 = s2;
                s2 = tmp;
            }
        }
    }

    len_s1 = s1.size(), len_s2 = s2.size();

    for (int i = 0; i < len_s1; ++i)
        a[len_s1-1-i] = s1[i] - '0';
    for (int i = 0; i < len_s2; ++i)
        b[len_s2-1-i] = s2[i] - '0';

    int max_len = len_s1 > len_s2 ? len_s1 : len_s2;
    for (int i = 0; i < max_len; i++){
        if (a[i] < b[i]){
            a[i+1]--;
            a[i] += 10;
        }
        res[i] = a[i] - b[i];
    }

    if (is_less_0) cout << "-";
    while (max_len-1 > 0 && res[max_len - 1] == 0){
        max_len--;
    }
    for (int i = 0; i < max_len; ++i){
        cout << res[max_len - 1 - i];
    }
    cout << endl;
    return 0;
}