#include <iostream>
using namespace std;

class Solution {
public:
    int searchInsert(vector<int>& nums, int target) {
        return halfSearch(nums, target);
    }

    int halfSearch(vector<int>& nums, int target){
        int l = 0, r = nums.size();

        while (l < r){
            int mid = l + (r -l) / 2;
            if (nums[mid] < target)
                l = mid + 1;
            else
                r = mid;
        }
        return l;
    }
};

int main() {
    Solution sol;
    vector<int> nums1 = {1, 3, 5, 6};
    cout << sol.searchInsert(nums1, 5) << endl; // Output: 2
    cout << sol.searchInsert(nums1, 2) << endl; // Output: 1
    cout << sol.searchInsert(nums1, 7) << endl; // Output: 4
    cout << sol.searchInsert(nums1, 0) << endl; // Output: 0
    vector<int> nums2 = {};
    cout << sol.searchInsert(nums2, 1) << endl; // Output: 0
    return 0;
}