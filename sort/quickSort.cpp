#include <iostream>
using namespace std;

void swapint(int* x, int* y) {
    int tmp = *x;
    *x = *y;
    *y = tmp;
}
int partition(int* nums, int left, int right) {
    // int pivot = nums[left + (right - left) / 2];
    int pivot = nums[right];
    int i = left, j = right;
    while (i <= j) {
        while (nums[i] < pivot)
            ++i;
        while (nums[j] > pivot)
            --j;
        if (i <= j) {
            swapint(&nums[i], &nums[j]);
            ++i;--j;
        }
    }
    return i;
}

void quickSort(int* nums, int left, int right) {
    if (left == right) return;
    int i = partition(nums, left, right);

    if (left < i-1) quickSort(nums, left, i - 1);
    if (right > i) quickSort(nums, i, right);
}
int main() {
    // int num[11] = { 10, 12, 3, 14, 5, 6, 27, 8, 9, 12 ,4 };
    int num[] = { 10, 3, 14, 5, 6 };
    // int num[] = { 3,2,5,2 };

    // int num[6] = { 2, 4, 1, 0, 3, 5 };
    int len = sizeof(num) / sizeof(num[0]);
    quickSort(num, 0, len - 1);

    for (int v : num) cout << v << " ";
    cout << endl;
    return 0;
}