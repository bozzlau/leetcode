#include <iostream>
#include <vector>
using namespace std;

//选择排序
void selection_sort(vector<int> &nums) {
    for (int i = 0; i < nums.size() - 1; i++) {
        int min_index = i;
        for (int j = i + 1; j < nums.size(); j++) {
            if (nums[j] < nums[min_index]) {
                min_index = j;
            }
        }
        if (min_index != i) {
            swap(nums[i], nums[min_index]);
        }
    }
}

int main() {
    vector<int> nums = {5, 4, 6, 3, 2, 1};
    selection_sort(nums);
    for (int i = 0; i < nums.size(); i++) {
        cout << nums[i] << " ";
    }
    cout << endl;
    return 0;
}