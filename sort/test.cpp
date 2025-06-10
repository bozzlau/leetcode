#include <iostream>
#include <deque>
#include <vector>

using namespace std;

// 滑动窗口最大值
vector<int> maxSlidingWindow(vector<int>& nums, int k) {
    vector<int> result;
    deque<int> dq; // 存储下标

    for (int i = 0; i < nums.size(); i++) {
        cout << "Deque elements (using range-based for loop): ";
        for (int element : dq) {
            cout << element << " ";
        }
        cout << endl;        
        // 移除超出窗口范围的元素
        while (!dq.empty() && dq.front() <= i - k) {
            dq.pop_front();
        }

        // 移除队列中比当前元素小的元素，保持单调递减
        while (!dq.empty() && nums[dq.back()] < nums[i]) {
            dq.pop_back();
        }

        // 将当前元素下标加入队列
        dq.push_back(i);

        // 当窗口大小达到k时，记录最大值（队首）
        if (i >= k - 1) {
            result.push_back(nums[dq.front()]);
        }
    }
    return result;
}

int main() {
    vector<int> nums = {1, 3, -1, -3, 5, 3, 6, 7};
    int k = 3; // 窗口大小
    vector<int> result = maxSlidingWindow(nums, k);

    for (int val : result) {
        cout << val << " ";
    }
    cout << endl; // 输出: 3 3 5 5 6 7
    return 0;
}