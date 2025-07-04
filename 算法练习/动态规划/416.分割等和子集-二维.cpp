#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    bool canPartition(vector<int>& nums) {
        int sum = 0, target = 0;
        for (int x : nums) sum += x;
        if (sum % 2 == 0)
            target = sum / 2;
        else
            return false;

        vector<vector<int>> dp(nums.size()+1, vector<int>(target+1, 0));

        for (int i = 1; i <= nums.size(); ++i){
            for (int t = 1; t <= target; ++t){
                if (nums[i-1] > t)
                    dp[i][t] = dp[i-1][t];
                else
                    dp[i][t] = max(dp[i-1][t], dp[i-1][t-nums[i-1]] + nums[i-1]);
            }
        }

        return (dp[nums.size()][target] == target ? true : false);
    }
};

int main(){
    // vector<int> nums = {1,5,11,5};
    vector<int> nums = {1,2,3,5};
    Solution sol;
    bool ans = sol.canPartition(nums);
    cout << ans << endl;
}