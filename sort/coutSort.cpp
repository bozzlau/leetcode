#include <iostream>
#include <vector>
using namespace std;

int main() {
    int nums[10] = { 16,2,8,5,3,27,4,9,3,8 };
    int max = 0;
    for (int i : nums) {
        if (i > max) {
            max = i;
        }
    }

    vector<int> counter(max + 1, 0);
    for (int n : nums) {
        counter[n]++;
    }

    int m = 0;
    for (int i = 0; i < max + 1; i++) {
        for (int j = 0; j < counter[i]; j++, m++) {
            nums[m] = i;
        }
    }

    for (int v : nums) {
        cout << v << " ";
    }
    cout << endl;
}