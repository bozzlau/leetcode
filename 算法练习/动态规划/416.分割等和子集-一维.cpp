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

        vector<int> dp(target+1, 0);

        for (int i = 0; i < nums.size(); ++i){
            for (int t = target; t > 0; --t){
                if (nums[i] <= t)
                    dp[t] = max(dp[t], dp[t-nums[i]] + nums[i]);
            }
            for (int x :dp)
                cout << x << " ";
            cout << endl;
        }
        return (dp[target] == target ? true : false);
    }
};

int main(){
    vector<int> nums = {1,5,11,5};
    // vector<int> nums = {1,2,3,5};
    Solution sol;
    bool ans = sol.canPartition(nums);
    cout << ans << endl;
}