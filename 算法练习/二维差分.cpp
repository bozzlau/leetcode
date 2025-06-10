#include <iostream>
#include <vector>

using namespace std;

// 根据原始矩阵构造差分矩阵
vector<vector<int>> build2DDiffArray(const vector<vector<int>>& matrix) {
    int rows = matrix.size(), cols = matrix[0].size();
    vector<vector<int>> diff(rows, vector<int>(cols, 0));
    // 初始化差分矩阵
    diff[0][0] = matrix[0][0];
    for (int j = 1; j < cols; j++) diff[0][j] = matrix[0][j] - matrix[0][j-1];
    for (int i = 1; i < rows; i++) diff[i][0] = matrix[i][0] - matrix[i-1][0];
    for (int i = 1; i < rows; i++) {
        for (int j = 1; j < cols; j++) {
            diff[i][j] = matrix[i][j] - matrix[i-1][j] - matrix[i][j-1] + matrix[i-1][j-1];
        }
    }
    return diff;
}

// 在差分矩阵上进行区域修改
void update2DRange(vector<vector<int>>& diff, int x1, int y1, int x2, int y2, int value) {
    diff[x1][y1] += value;
    if (y2 + 1 < diff[0].size()) diff[x1][y2 + 1] -= value;
    if (x2 + 1 < diff.size()) diff[x2 + 1][y1] -= value;
    if (x2 + 1 < diff.size() && y2 + 1 < diff[0].size()) diff[x2 + 1][y2 + 1] += value;
}

// 根据差分矩阵还原原始矩阵
vector<vector<int>> recover2DArray(const vector<vector<int>>& diff) {
    int rows = diff.size(), cols = diff[0].size();
    vector<vector<int>> result(rows, vector<int>(cols, 0));
    // 用二维前缀和还原
    result[0][0] = diff[0][0];
    for (int j = 1; j < cols; j++) result[0][j] = result[0][j-1] + diff[0][j];
    for (int i = 1; i < rows; i++) result[i][0] = result[i-1][0] + diff[i][0];
    for (int i = 1; i < rows; i++) {
        for (int j = 1; j < cols; j++) {
            result[i][j] = result[i-1][j] + result[i][j-1] - result[i-1][j-1] + diff[i][j];
        }
    }
    return result;
}

// 打印矩阵
void printMatrix(const vector<vector<int>>& matrix) {
    for (const auto& row : matrix) {
        for (int x : row) cout << x << " ";
        cout << endl;
    }
}

int main() {
    // 初始矩阵
    vector<vector<int>> matrix = {
        {1, 2, 3},
        {4, 5, 6},
        {7, 8, 9}
    };
    cout << "Original Matrix:" << endl;
    printMatrix(matrix);

    // 构造差分矩阵
    vector<vector<int>> diff = build2DDiffArray(matrix);
    cout << "\nDifference Matrix:" << endl;
    printMatrix(diff);

    // 区域修改：给 (0,0) 到 (1,1) 加 4
    update2DRange(diff, 0, 0, 1, 1, 4);
    cout << "\nDifference Matrix after update:" << endl;
    printMatrix(diff);

    // 还原矩阵
    vector<vector<int>> updated = recover2DArray(diff);
    cout << "\nUpdated Matrix:" << endl;
    printMatrix(updated);

    return 0;
}