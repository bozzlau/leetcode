#include <iostream>
#include <vector>
using namespace std;

void countingSort(vector<int>& numsA) {
    int max = 0;
    for (int i = 0;i < numsA.size();++i) {
        if (numsA[i] > max) max = numsA[i];
    }
    printf("max:%d\n", max);
    //填写计数数组
    vector<int> counter(max + 1, 0);
    for (int i = 0; i < numsA.size(); ++i) {
        counter[numsA[i]]++;
    }
    //输出排序结果
    for (int i = 0, k = 0; i <= counter.size(); ++i) {
        for (int j = counter[i]; j > 0;j--, k++) {
            numsA[k] = i;
            // printf("%d ", i);
        }
    }
    // printf("\n");
}
int main() {
    vector<int> nums{ 6,2,7,5,3,2,1,3,9,0,2,7 };
    for (auto n : nums) { printf("%d ", n); }
    printf("\n");
    //排序
    countingSort(nums);
    for (auto n : nums) { printf("%d ", n); }
    printf("\n");

}