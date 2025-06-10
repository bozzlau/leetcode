#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

//冒泡排序
void bubble_sort(vector<int>& nums) {
    for (int i = 0; i < nums.size() - 1; i++) {
        for (int j = 0; j < nums.size() - i - 1; j++) {
            if (nums[j] > nums[j + 1]) {
                swap(nums[j], nums[j + 1]);
            }
        }
    }
}

int main() {
    vector<int> nums;

    //乱序初始化包含1万个元素的数据
    for (int i = 0; i < 100000; i++) {
        nums.push_back(i);
    }
    //打乱数组元素顺序
    random_shuffle(nums.begin(), nums.end());

    //打印乱序数组
    // for (int i = 0; i < nums.size(); i++) {
    //     cout << nums[i] << " ";
    // }
    //测试排序性能
    auto start = std::chrono::steady_clock::now();
    bubble_sort(nums);
    auto end = std::chrono::steady_clock::now();
    cout << "排序用时: " << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << "ms" << endl;

}