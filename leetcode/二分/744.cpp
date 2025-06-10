/*
给你一个字符数组 letters，该数组按非递减顺序排序，以及一个字符 target。letters 里至少有两个不同的字符。
返回 letters 中大于 target 的最小的字符。如果不存在这样的字符，则返回 letters 的第一个字符。
示例 1：
输入: letters = ["c", "f", "j"]，target = "a"
输出: "c"
解释：letters 中字典上比 'a' 大的最小字符是 'c'。
*/

#include <iostream>
using namespace std;

class Solution {
public:
    char nextGreatestLetter(vector<char>& letters, char target) {
        int l = 0, r = letters.size() - 1;
        int mid = 0;
        while (l < r){
            mid = l + (r - l + 1) / 2;
            if (letters[mid] <= target){
                l = mid;
            }else{
                r = mid - 1;
            }
        }
        
        char ans = ' ';
        if (l == letters.size()-1){
            ans = letters[0];
        }else if (l == 0 && letters[l] > target){
            ans = letters[0];
        }else{
            ans = letters[l+1];
        }
        return ans;
    }
};

int main(){
    Solution sol;
    vector<char> letters = {'c', 'f', 'j'};
    char target = 'j';
    printf("%c\n", sol.nextGreatestLetter(letters, target));
    letters = {'x', 'x', 'y', 'y'},target = 'z';
    printf("%c\n", sol.nextGreatestLetter(letters, target));
    return 0;
}