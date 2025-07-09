#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        int sum = 0;
        for (int x : nums) sum += x;

        /*  P代表 +号子序列的和；N代表 -号子序列的和，不包含正负符号
            P + N = sum(nums); P - N = target
            2P = sum(nums) + target
        */
        if ((sum + target) % 2 == 1 || sum + target < 0) return 0;
        int P = (sum + target) / 2;

        vector<int> dp(P+1, 0);
        dp[0] = 1;
        for (int i = 0; i < nums.size(); ++i){
            for (int j = P; nums[i] <= j; j--){
                dp[j] = dp[j] + dp[j - nums[i]];
            }
            // for (int x:dp) cout << x << " ";
            // cout << endl;
        }
        return dp[P];
    }

};

int main(){
    // vector<int> nums = {1,1,1,1,1}; int target = 3;
    // vector<int> nums = {7,9,3,8,0,2,4,8,3,9}; int target = 0;
    // vector<int> nums = {0}; int target = 0;
    vector<int> nums = {1}; int target = 1;
    Solution sol;
    int res = sol.findTargetSumWays(nums, target);
    cout << res << endl;
    return 0;
}