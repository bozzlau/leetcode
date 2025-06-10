#include <iostream>
using namespace std;

void insertSort(int*, int);
int main() {
    int num[10] = { 10, 12, 3, 14, 5, 6, 27, 8, 9, 1 };
    insertSort(num, 10);

    // for (auto i : num) {
    //     cout << i << " ";
    // }
    // cout << endl;
}

void insertSort(int* num, int n) {
    cout << "insertSort" << endl;
    for (int i = 1; i < n; ++i) {
        int t = num[i];
        int j = i - 1;
        // while (j >= 0 && t < num[j]) {
        //     num[j + 1] = num[j];
        //     j--;
        // }
        // num[j + 1] = t;

        for (; j >= 0 && t < num[j]; j--) {
            // cout << t << " " << num[j] << endl;
            if (t < num[j]) {
                num[j + 1] = num[j];
            }
        }
        num[j + 1] = t;

        for (int i = 0;i<n;++i) {
            cout << num[i] << " ";
        }
        cout << endl;
    }
}
