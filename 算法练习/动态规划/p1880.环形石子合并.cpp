#include <iostream>
#include <vector>
using namespace std;

const int INF = 1e9;

int main(){
    int n;
    cin >> n;
    vector<int> stones(n, 0);
    vector<int> double_stones(2*n, 0);
    for (int i = 0; i < n; ++i){
        cin >> stones[i];
        double_stones[i] = stones[i];
        double_stones[n+i] = stones[i]; //复制一份石子，环形变为线性
    }

    //前缀和
    vector<int> pre_sum(2*n+1, 0);
    for (int i = 0; i < 2*n; ++i)
        pre_sum[i+1] = pre_sum[i] + double_stones[i];

    //dp初始化
    vector<vector<int>> min_dp(2*n, vector<int>(2*n, 99));
    vector<vector<int>> max_dp(2*n, vector<int>(2*n, 0));
    for (int i = 0; i < 2*n; ++i){
        min_dp[i][i] = 0; //单个每堆石子无需合并，代价是0
        max_dp[i][i] = 0; //单个每堆石子无需合并，代价是0
    }
    
    //求i到j堆的石子数量
    auto get_sum = [&](int i, int j){
        return pre_sum[j+1] - pre_sum[i];
    };
    
    //区间动态规划
    int min_cost = INF;
    int max_cost = 0;
    for (int len = 2; len <= n; ++len){ //子区间长度,长度从2开始
        for (int i = 0; i+len <= 2*n; ++i){ //区间起点i
            int j = i + len - 1;  //区间终点j
            for (int k = i; k < j; ++k){
                min_dp[i][j] = min(min_dp[i][j], min_dp[i][k] + min_dp[k+1][j] + get_sum(i, j));
                max_dp[i][j] = max(max_dp[i][j], max_dp[i][k] + max_dp[k+1][j] + get_sum(i, j));
                if (len == n){
                    printf("--[%d:%d] k=%d min:%d max:%d\n", i, j, k, (min_dp[i][k] + min_dp[k+1][j] + get_sum(i, j)), max_dp[i][j]);
                }
            }
            if (len == n)
                printf("[%d, %d]:%d %d\n", i, j, min_dp[i][j], max_dp[i][j]);
        }

        for (int i = 0; i < n; ++i){
            //从长度2n的链中取区间长度为n的子区间的dp值，即分别从环状的每个元素转一圈
            // [4 5 9 4 4 5 9 4]     *4594复制一份长度变2n，环状变线性
            //即 dp[0,3]-4594  dp[1,4]-5944  dp[2,5]-9445  dp[3,6]-4459
            min_cost = min(min_cost, min_dp[i][i+n-1]);
            max_cost = max(max_cost, max_dp[i][i+n-1]);
        }
    }
    printf("%d\n%d\n", min_cost, max_cost);

    for (int i = 0; i < 2*n; ++i){
        for (int j = 0; j < 2*n; ++j)
            cout << min_dp[i][j] << " ";
        cout << endl;
    }
}