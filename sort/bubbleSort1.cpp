#include <iostream>
#include <vector>
using namespace std;

void bubbleSort(vector<int>&);
void bubbleSort1(vector<int>&);
void printfVec(vector<int>& a);

void swap(int& a, int& b) {
    a ^= b;
    b ^= a;
    a ^= b;
}
int main() {
    vector<int> a = { 2,6,4,8,1,3,7,5,9,0 };
    bubbleSort1(a);
    printfVec(a);
    return 0;
}

void bubbleSort(vector<int>& nums) {
    int len = nums.size();
    int loopCnt{0};
    for (int i = 0; i < len - 1; i++) {
        for (int j = 0; j < len - i - 1; ++j) {
            loopCnt++;
            if (nums[j] > nums[j + 1]) swap(nums[j], nums[j + 1]);
        }
    }
    cout << "loop cnt:" << loopCnt << endl;
}

void bubbleSort1(vector<int>& nums) {
    int len = nums.size();
    for (int i = len - 1; i >= 0; --i) {
        for (int j = 0; j < i; ++j) {
            if (nums[j] > nums[j+1]) swap(nums[j], nums[j+1]);
        }
    }
}

void printfVec(vector<int>& nums) {
    for (int v : nums) { printf("%d ", v); }
    printf("\n");
}