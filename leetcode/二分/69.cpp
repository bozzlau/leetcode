#include <iostream>
using namespace std;

class Solution {
public:
    int mySqrt(int x) {
        if (x == 1 or x ==2) return 1;

        // int l = 0, r = x/2;
        // long long square = 0;
        // int mid = 0;
        // while (l <= r){
        //     mid = (l + r) / 2;
        //     square = (long long)mid * mid;
        //     if (square < x){
        //         l = mid + 1;
        //     }else if (square > x)
        //         r = mid - 1;
        //     else if (square == x)
        //         return mid;
        // }
        // return l-1;

        int l = 0, r = x;
        long long square = 0;
        int mid = 0, ans = 0;
        while (l < r){
            mid = (l + r) / 2;
            square = (long long)mid * mid;
            if (square < x){
                ans = mid;
                l = mid + 1;
            }else{
                if (square == x) return mid;
                r = mid;
            }
        }
        return l-1;
    }
};

int main(){
    Solution sol;
    cout << sol.mySqrt(8) << endl;
    cout << sol.mySqrt(9) << endl;
    cout << sol.mySqrt(4) << endl;
    cout << sol.mySqrt(2) << endl;
    return 0;
}