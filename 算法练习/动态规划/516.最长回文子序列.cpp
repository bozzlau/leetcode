#include <iostream>
using namespace std;

class Solution {
public:
    int longestPalindromeSubseq(string s) {
        int len = s.length();
        vector<vector<int>> dp(len, vector<int>(len, 0));
        for (int i = 0; i < len; ++i)
            dp[i][i] = 1;
        for (auto v:dp){
            for (int x:v){
                cout << x << " ";
            }
            cout << endl;
        }

        for (int i = len - 1; i >= 0; --i){
            for (int j = i+1; j < len; ++j){
                if (s[i] == s[j]){
                    dp[i][j] = dp[i+1][j-1] + 2;
                }else{
                    dp[i][j] = max(dp[i][j-1], dp[i+1][j]);
                }
            }
        }
        cout << endl;
        for (auto v:dp){
            for (int x:v){
                cout << x << " ";
            }
            cout << endl;
        }
        return dp[0][len-1];
    }
};

int main(){
    string s = "bbbab";
    Solution sol;
    int res = sol.longestPalindromeSubseq(s);
    cout << res << endl;

}