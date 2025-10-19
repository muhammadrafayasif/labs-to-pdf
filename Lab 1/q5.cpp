#include <iostream>
using namespace std;
 
class Array2D {
    private:
        int **arr;
        int rows, cols;
    public:
        Array2D(int r, int c) : rows(r), cols(c) {
            arr = new int*[rows];
            for (int i = 0; i < rows; i++) {
                arr[i] = new int[cols];
            }
        }
        int* operator[](int index) {
            return arr[index];
        }
        int find(int key) {
            int l = 0, r = rows * cols - 1;
            while (l <= r) {
                int mid = l + (r - l) / 2;
                int mid_val = arr[mid / cols][mid % cols];
                if (mid_val == key) return true;
                else if (mid_val < key) l = mid + 1;
                else r = mid - 1;
            }
            return false;
        }
        ~Array2D() {
            for (int i = 0; i < rows; i++) {
                delete[] arr[i];
            }
            delete[] arr;
        }
};

int main() {
    cout << "Enter number of rows and columns for 2D array: ";
    int r, c;
    cin >> r >> c;
    Array2D arr2d(r, c);
    cout << "Enter elements in sorted order:\n";
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            cin >> arr2d[i][j];
        }
    }
    cout << "Enter element to search: ";
    int key;
    cin >> key;
    int index = arr2d.find(key);
    if (index) {
        cout << "Element found" << endl;
    } else {
        cout << "Element not found" << endl;
    }
    return 0;
}