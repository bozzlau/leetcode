#include <iostream>
#include <algorithm>
#include <vector>
using namespace std;

class Solution {
public:
    int maximalSquare(vector<vector<char>>& matrix) {
        int r = matrix.size(), c = matrix[0].size();
        vector<vector<int>> dp(r, vector<int>(c, 0));

        for (int i = 0; i < r; ++i) dp[i][0] = matrix[i][0] - '0';
        for (int i = 0; i < c; ++i) dp[0][i] = matrix[0][i] - '0';

        int maxval = 0;
        for (int i = 0; i < r; ++i){
            for (int j = 0; j < c; ++j){
                if (matrix[i][j] == '1' && i > 0 && j > 0)
                    dp[i][j] = min({dp[i][j-1], dp[i-1][j], dp[i-1][j-1]}) + 1;
                maxval = max({maxval, dp[i][j]});
            }
        }

        return maxval*maxval;
    }
};

int main(){
    Solution sol;
    // vector<vector<char>> matrix =   {{'1','0','1','0','0'}
    //                                 ,{'1','0','1','1','1'}
    //                                 ,{'1','1','1','1','1'}
    //                                 ,{'1','0','1','1','1'}};
    vector<vector<char>> matrix =   {{'0','1'}
                                    ,{'1','0'}};
    // vector<vector<char>> matrix =   {{'1','1'}
    //                                 };
    int ans = sol.maximalSquare(matrix);
    cout << ans << endl;
    return 0;
}