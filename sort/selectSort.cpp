#include <iostream>
using namespace std;

void quickSort(int* num, int n);
int main() {
    int num[10] = { 10, 12, 3, 14, 5, 6, 27, 8, 9, 1 };
    quickSort(num, 10);

    for (auto i : num) {
        cout << i << " ";
    }
    cout << endl;
}

void quickSort(int* num, int n) {
    cout << "quickSort" << endl;
    cout << num[0] << endl;
    int k = 0;
    int cnt = 0;
    for (int i = 0; i < n ; ++i) {
        k = i;
        for (int j = i + 1; j < n; ++j) {
            if (num[j] < num[k]) {
                k = j;
            }
            ++cnt;
        }
        int tmp = num[i];
        num[i] = num[k];
        num[k] = tmp;
    }
    printf("cnt = %d\n", cnt);
}