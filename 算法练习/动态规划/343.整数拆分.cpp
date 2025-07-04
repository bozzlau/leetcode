#include <iostream>
using namespace std;

class Solution {
public:
    int integerBreak(int n) {
        int s = n / 3;
        int y = n % 3;
        int res = 1;

        switch (n)
        {
        case 2: res = 1; break;
        case 3: res = 2; break;
        case 4: res = 4; break;
        case 5: res = 6; break;
        }

        if (n > 5){
            for (int i = 0; i < s; ++i) res *= 3;
            if (y == 1) res = res * 4 / 3;
            if (y == 2) res *= 2;
        }
        return res;
    }
};

int main(){
    Solution sol;
    int n = 16;
    int ans = sol.integerBreak(n);
    cout << ans << endl;
    return 0;
}
