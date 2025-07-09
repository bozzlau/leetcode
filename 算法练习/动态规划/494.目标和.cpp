#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = 0;
        for (int x : nums){
            sum += x;
        }

        int nt = (sum + target) / 2; // new target
        int len = nums.size();

        vector<vector<int>> dp(len+1, vector<int>(nt+1, 0));
        for (int i = 0; i < len+1; ++i){
            dp[i][0] = 1;
        }
        for (int i = 1; i <=len ; ++i){
            for (int j = 1; j <= nt; ++j){
                if (nums[i-1] > j){
                    dp[i][j] = dp[i-1][j];
                }else{
                    dp[i][j] = dp[i-1][j] + dp[i-1][j-nums[i-1]];
                }
            }
        }
        return dp[len][nt];
    }

};

int main(){
    vector<int> nums = {1,1,1,1,1}; int target = 3;
    // vector<int> nums = {1}; int target = 1;
    // vector<int> nums = {1}; int target = 1;
    Solution sol;
    int res = sol.findTargetSumWays(nums, target);
    cout << res << endl;
    return 0;
}