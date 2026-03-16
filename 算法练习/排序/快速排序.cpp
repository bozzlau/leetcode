#include <iostream>
#include <vector>
#include <algorithm> // for std::swap

using namespace std;

/**
 * 分区函数 (Partition)
 * 该函数选取最后一个元素作为基准值 (pivot)
 * 将小于基准值的元素移到左边，大于基准值的元素移到右边
 */
int partition(vector<int>& arr, int low, int high) {
    int pivot = arr[high]; // 选择最后一个元素作为基准
    int i = (low - 1); // i 是较小元素的索引

    for (int j = low; j <= high - 1; j++) {
        // 如果当前元素小于或等于基准
        if (arr[j] <= pivot) {
            i++; // 增加较小元素的索引
            swap(arr[i], arr[j]);
        }
    }
    swap(arr[i + 1], arr[high]);
    return (i + 1);
}

/**
 * 快速排序主函数
 * arr: 待排序数组
 * low: 起始索引
 * high: 结束索引
 */
void quickSort(vector<int>& arr, int low, int high) {
    if (low < high) {
        // pi 是分区索引 (partitioning index)，arr[pi] 已经排好序
        int pi = partition(arr, low, high);

        // 递归排序基准元素左边和右边的子数组
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

// 打印数组的辅助函数
void printArray(const vector<int>& arr) {
    for (int i : arr) {
        cout << i << " ";
    }
    cout << endl;
}

int main() {
    vector<int> arr = {10, 7, 8, 9, 1, 5};
    
    cout << "原始数组: ";
    printArray(arr);

    quickSort(arr, 0, arr.size() - 1);

    cout << "排序后数组: ";
    printArray(arr);

    return 0;
}
