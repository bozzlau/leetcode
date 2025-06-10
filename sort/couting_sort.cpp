#include <iostream>
#include <vector>
using namespace std;

void countingSort(vector<int>& nums) {
    int max = 0;
    int n = nums.size();
    vector<int> res(n, 0);
    for (int i = 0;i < n;++i) {
        if (nums[i] > max) max = nums[i];
    }
    printf("max:%d\n", max);
    //填写计数数组
    vector<int> cnter(max + 1, 0);
    for (int i = 0; i < n; ++i) { cnter[nums[i]]++; }
    //统计前缀和
    for (int i = 0; i < n - 1; ++i) { cnter[i + 1] += cnter[i]; }
    //排序结果
    for (int i = n - 1; i >= 0; --i) { res[--cnter[nums[i]]] = nums[i]; }
    nums = res;
}
int main() {
    vector<int> a{ 6,2,7,5,3,2,1,3,9,2,7 };
    for (auto n : a) { printf("%d ", n); }
    printf("\n");
    //排序
    countingSort(a);
    for (auto n : a) { printf("%d ", n); }
    printf("\n");

}