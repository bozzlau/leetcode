/*
给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。
如果数组中不存在目标值 target，返回 [-1, -1]。
你必须设计并实现时间复杂度为 O(log n) 的算法解决此问题。
示例 1：
输入：nums = [5,7,7,8,8,10], target = 8
输出：[3,4]
*/

#include <iostream>
using namespace std;
class Solution {
public:
    vector<int> searchRange(vector<int>& nums, int target) {
        vector<int> ans;
        ans.push_back(binarySearchLeft(nums, target));
        ans.push_back(binarySearchRight(nums, target));
        return ans;
    }

    int binarySearchLeft(vector<int>& nums, int target){
        if (nums.size() == 0) return -1;
        int l = 0, r = nums.size()-1;
        int mid = 0;
        while (l < r){
            mid = l + (r - l) / 2;
            if (nums[mid] >= target){
                r = mid;
            }else{
                l = mid + 1;
            }
        }
        return (nums[l] == target)?l:-1;
    }

    int binarySearchRight(vector<int>& nums, int target){
        if (nums.size() == 0) return -1;
        int l = 0, r = nums.size()-1;
        int mid = 0;
        while (l < r){
            mid = l + (r - l + 1) / 2;
            if (nums[mid] > target){
                r = mid - 1;
            }else{
                l = mid;
            }
        }
        return (nums[l] == target)?l:-1;
    }
};

int main(){
    vector<int> nums = {5,7,7,8,8,10};
    int target = 8;
    // vector<int> nums = {};
    // int target = 0;
    Solution sol;

    vector<int> ans = sol.searchRange(nums, target);
    printf("[%d,%d]\n",ans[0], ans[1]);
    return 0;
}