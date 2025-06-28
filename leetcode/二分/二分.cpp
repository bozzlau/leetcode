#include <iostream>
using namespace std;

int half_search(int *p, int len, int target){
    int l = 0, r = len-1;

    // while (l < r){
    //     int mid = l + (r - l + 1) / 2;
    //     if (p[mid] <= target)
    //         l = mid;
    //     else
    //         r = mid - 1;
    // }
    // return (p[l] == target) ? l+1 : -1;

    while (l < r){
        int mid = l + (r - l) / 2;
        if (p[mid] < target)
            l = mid + 1;
        else
            r = mid;
    }
    return (p[l] == target) ? l+1 : -1;

}

int arr[100001];
int main(){
    int n, q;

    cin >> n;
    for (int i = 0; i < n; ++i){
        cin >> arr[i];
    }

    cin >> q;
    int query;
    for (int i = 0; i < q; ++i){
        cin >> query;
        cout << half_search(arr, n, query) << " ";
    }
    cout << endl;
    return 0;
}