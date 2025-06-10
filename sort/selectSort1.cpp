#include <iostream>
#include <vector>
using namespace std;

void selectSort(vector<int>&);
void printfVec(vector<int>& a);

void swap(int& a, int& b) {
    a ^= b;
    b ^= a;
    a ^= b;
}
int main() {
    vector<int> a = { 5,4,0,3,2,1,12,9,11,8,7,6 };
    selectSort(a);
    printfVec(a);
    return 0;
}

void selectSort(vector<int>& nums) {
    int len = nums.size();
    for (int i = 0; i < len - 1; ++i) {
        for (int j = i + 1; j < len; ++j) {
            if (nums[j] < nums[i]) swap(nums[j], nums[i]);
        }
    }
}

void printfVec(vector<int>& nums) {
    for (int v : nums) { printf("%d ", v); }
    printf("\n");
}
