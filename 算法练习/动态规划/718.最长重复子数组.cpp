#include <iostream>
#include <vector>
using namespace std;

class Solution {
public:
    int findLength(vector<int>& nums1, vector<int>& nums2) {
        int len1 = nums1.size(), len2 = nums2.size();
        vector<vector<int>> dp(len1+1, vector<int>(len2+1));
        int res = 0;

        for (int i = 1; i <= len1; ++i){
            for (int j = 1; j <= len2; ++j){
                if (nums1[i-1] == nums2[j-1]){
                    dp[i][j] = dp[i-1][j-1] + 1;
                }
                if (res < dp[i][j])
                    res = dp[i][j];
            }
        }

        for (auto v:dp){
            for (int x:v){
                cout << x << " ";
            }
            cout << endl;
        }
        return res;
    }
};

int main(){
    Solution sol;
    // vector<int> nums1 = {1,2,3,2,1}, nums2 = {3,2,1,4,7};
    vector<int> nums1 = {0,1,1,1,1}, nums2 = {1,0,1,0,1};
    int res = sol.findLength(nums1, nums2);
    cout << res << endl;
    return 0;
}