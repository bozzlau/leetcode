#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int lengthOfLIS(vector<int>& nums) {
        if (nums.size() <= 1) return nums.size();
        // vector<int> dp(nums.size(), 1);
        // int result = 0;
        // for (int i = 1; i < nums.size(); i++) {
        //     for (int j = 0; j < i; j++) {
        //         if (nums[i] > nums[j]) dp[i] = max(dp[i], dp[j] + 1);
        //     }
        //     if (dp[i] > result) result = dp[i]; // 取长的子序列
        // }
        // return result;        

        vector<int> tails;
        for (int i = 0; i < nums.size(); ++i){
            int idx = binary_search(tails, nums[i]);

            if (idx == tails.size())
                tails.push_back(nums[i]);
            else
                tails[idx] = nums[i];
        }

        for (auto x:tails) cout << x << " ";
        cout << endl;
        return tails.size();
    }

    int binary_search(vector<int>& nums, int num){
        int l = 0, r = nums.size()-1;

        while (l <= r){
            int mid = l + (r - l) / 2;
            if (nums[mid] < num)
                l = mid + 1;
            else
                r = mid - 1;
        }
        return l;
    }
};

int main(){
    vector<int> num = {10,9,2,5,3,7,101,18};
    Solution sol;
    int res = sol.lengthOfLIS(num);
    cout << res << endl;
}