#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

using namespace std;

class Solution {
public:
    int minDistance(string word1, string word2) {
        int len1 = word1.size(), len2 = word2.size();
        vector<vector<int>> dp(len1 + 1, vector<int>(len2 + 1, 0));
        for (int i = 1; i <= len1; i++) dp[i][0] = i;
        for (int i = 1; i <= len2; i++) dp[0][i] = i;

        for (int i = 1; i <= len1; i++){
            for (int j = 1; j <= len2; j++){
                if (word1[i-1] == word2[j-1]){
                    dp[i][j] = dp[i-1][j-1];
                }else{
                    dp[i][j] = min({dp[i][j-1], dp[i-1][j], dp[i-1][j-1]}) + 1;
                }
            }
        }
        //打印dp表
        for (auto v : dp){
            for (int x :v){
                cout << x << " ";
            }
            cout << endl;
        }
        return dp[len1][len2];
    }
};

int main(){
    Solution sol;
    string word1 = "horse", word2 = "ros";
    int ans = sol.minDistance(word1, word2);
    cout << ans << endl;
}