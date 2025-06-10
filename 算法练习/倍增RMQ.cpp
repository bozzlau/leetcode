#include <vector>
#include <iostream>
using namespace std;

const int N = 100005;
const int LOG = 20;

vector<vector<int>> st(N, vector<int>(LOG));
vector<int> arr(N);

void preprocess(int n) {
    for (int i = 0; i < n; i++) {
        st[i][0] = arr[i];
    }
    for (int j = 1; j < LOG; j++) {
        for (int i = 0; i + (1 << j) - 1 < n; i++) {
            st[i][j] = min(st[i][j-1], st[i + (1 << (j-1))][j-1]);
        }
    }
    cout << "ok" << endl;
}

int query(int L, int R) {
    int len = R - L + 1;
    int k = 0;
    while ((1 << (k + 1)) <= len) k++;
    if (L + (1 << k) - 1 == R) return st[L][k];
    return min(st[L][k], st[R - (1 << k) + 1][k]);
}

int main() {
    int n = 8; // 8棵果树
    // 果子数量
    arr = {3, 1, 4, 1, 5, 9, 2, 6};
    
    preprocess(n); // 预处理

    // 查询示例
    cout << "从第2棵到第5棵的最小值: " << query(1, 4) << endl; // 输出1
    cout << "从第4棵到第8棵的最小值: " << query(3, 7) << endl; // 输出1

    return 0;
}