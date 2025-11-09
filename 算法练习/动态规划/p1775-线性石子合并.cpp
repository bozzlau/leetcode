#include <iostream>
#include <vector>
using namespace std;

const int Max = 205;
const int INF = 1e9;

int main(){
    int n;
    cin >> n;
    vector<int> stones(n, 0);
    for (int i = 0; i < n; ++i)
        cin >> stones[i];

    //前缀和
    vector<int> pre_sum(n+1, 0);
    for (int i = 0; i < n; ++i)
        pre_sum[i+1] = pre_sum[i] + stones[i];

    //dp初始化
    vector<vector<int>> dp(n, vector<int>(n, INF));
    for (int i = 0; i < n; ++i)
        dp[i][i] = 0; //单个每堆石子无需合并，代价是0
    
    //求i到j堆的石子数量
    auto get_sum = [&](int i, int j){
        return pre_sum[j+1] - pre_sum[i];
    };
    
    //区间动态规划
    for (int len = 2; len <= n; ++len){ //子区间长度,长度从2开始
        for (int i = 0; i+len <= n; ++i){ //区间起点i
            int j = i + len - 1;  //区间终点j
            for (int k = i; k < j; ++k){
                dp[i][j] = min(dp[i][j], dp[i][k] + dp[k+1][j] + get_sum(i, j));
            }

            printf("[%d, %d]:%d  get_sum:%d\n", i, j, dp[i][j], get_sum(i, j));
        }
    }
    cout << dp[0][n-1] << endl;

    for (int i = 0; i < n; ++i){
        for (int j = 0; j < n; ++j)
            cout << dp[i][j] << " ";
        cout << endl;
    }
}