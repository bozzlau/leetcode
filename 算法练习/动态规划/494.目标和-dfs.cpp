#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int findTargetSumWays(vector<int>& nums, int target) {
        // int times = 0;
        // dfs(nums, target, 0, 0, times);
        // return times;

        return dfs(nums, target, 0, 0);
    }

    int dfs(vector<int>& nums, int target, int sum, int idx){
        if (nums.size() == idx){
            // if (target == sum)
            //     return 1;
            // return 0;
            return (target == sum) ? 1 : 0;
        }

        int ans = dfs(nums, target, sum + nums[idx], idx+1) + dfs(nums, target, sum - nums[idx], idx+1);
        return ans;
    }

    // void dfs(vector<int>& nums, int target, int sum, int idx, int &times){
    //     if (idx == nums.size() and target == sum){
    //         ++times;
    //         // cout << times << endl;
    //         return;
    //     }
    //     if (idx >= nums.size())
    //         return;

    //     for (int n : {nums[idx], -nums[idx]}){
    //         sum += n;
    //         dfs(nums, target, sum, idx+1, times);
    //         sum -= n;
    //     }
    // }
};

int main(){
    vector<int> nums = {1,1,1,1,1}; int target = 3;
    // vector<int> nums = {1}; int target = 1;
    Solution sol;
    int res = sol.findTargetSumWays(nums, target);
    cout << res << endl;
    return 0;
}