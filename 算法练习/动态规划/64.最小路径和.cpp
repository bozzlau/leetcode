#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int minPathSum(vector<vector<int>>& grid) {
        int m = grid.size(), n = grid[0].size();
        vector<vector<int>> dp(m, vector<int>(n));
        int tmp = 0;
        dp[0][0] = grid[0][0];
        for (int i = 1; i < m; ++i) dp[i][0] += dp[i-1][0] + grid[i][0];
        for (int i = 1; i < n; ++i) dp[0][i] += dp[0][i-1] + grid[0][i];

        for (int i = 1; i < m; ++i){
            for (int j = 1; j < n; ++j){
                dp[i][j] += min({dp[i-1][j], dp[i][j-1]}) + grid[i][j];
            }
        }
        for (auto v:dp){
            for (int x : v){
                cout << x << " ";
            }
            cout << endl;
        }
        return dp[m-1][n-1];
    }
};

int main(){
    // vector<vector<int>> gird = {{1,3,1},{1,5,1},{4,2,1}};
    vector<vector<int>> gird = {{1,2,3},{4,5,6}};
    Solution sol;
    int ans = sol.minPathSum(gird);
    cout << ans << endl;
    return 0;
}
