#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int maxSubArray(vector<int>& nums) {
        vector<int> dp(nums.size(), 0);
        dp[0] = nums[0];

        int res = dp[0];
        for (int i = 1; i < nums.size(); ++i){
            if (dp[i-1] <= 0)
                dp[i] = nums[i];
            else
                dp[i] = dp[i-1] + nums[i];
            res = max(res, dp[i]);
        }

        for (int x: dp){
            cout << x << " ";
            // if (x > res) res = x;
        }
        cout << endl;
        return res;
    }
};

int main(){
    // vector<int> nums = {-2,1,-3,4,-1,2,1,-5,4};
    // vector<int> nums = {-1,-2};
    vector<int> nums = {5,4,-1,7,8};
    Solution sol;
    int res = sol.maxSubArray(nums);
    cout << res << endl;
}