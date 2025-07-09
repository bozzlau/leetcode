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

        if ((sum + target) % 2 == 1 || sum + target < 0) return 0;
        int nt = (sum + target) / 2; // new target
        int len = nums.size();

        vector<vector<int>> dp(len+1, vector<int>(nt+1, 0));
        for (int i = 0; i < len+1; ++i){
            dp[i][0] = 1;
        }
        for (auto v:dp){
            for(int x:v){
                cout << x << " ";
            }
            cout << endl;
        }
        for (int i = 1; i <=len ; ++i){
            for (int j = 0; j <= nt; ++j){
                if (nums[i-1] > j){
                    dp[i][j] = dp[i-1][j];
                }else{
                    dp[i][j] = dp[i-1][j] + dp[i-1][j-nums[i-1]];
                }
            }
        }
        cout << endl;
        for (auto v:dp){
            for(int x:v){
                cout << x << " ";
            }
            cout << endl;
        }
        return dp[len][nt];
    }

};

int main(){
    // vector<int> nums = {1,1,1,1,1}; int target = 3;
    vector<int> nums = {7,9,3,8,0,2,4,8,3,9}; int target = 0;
    // vector<int> nums = {0}; int target = 0;
    // vector<int> nums = {1}; int target = 1;
    Solution sol;
    int res = sol.findTargetSumWays(nums, target);
    cout << res << endl;
    return 0;
}