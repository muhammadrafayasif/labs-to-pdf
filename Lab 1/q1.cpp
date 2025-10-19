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
        int getRows() { return rows; }
        int getCols() { return cols; }
        ~Array2D() {
            for (int i = 0; i < rows; i++) {
                delete[] arr[i];
            }
            delete[] arr;
        }
};

class Array1D {
    private:
        int *arr;
        int size;
    public:
        Array1D(int s) : size(s) {
            arr = new int[size];
        }
        // Copy constructor that takes Array2D and flattens it (column order)
        Array1D(Array2D &other) {
            size = other.getRows() * other.getCols();
            arr = new int[size];
            int index = 0;
            for (int i = 0; i < other.getRows(); i++) {
                for (int j = 0; j < other.getCols(); j++) {
                    arr[index++] = other[j][i];
                }
            }
        }
        int& operator[](int index) {
            return arr[index];
        }
        ~Array1D() {
            delete[] arr;
        }
};

int main() {
    cout << "Enter number of rows and columns for 2D array: ";
    int r, c;
    cin >> r >> c;
    Array2D arr2d(r, c);
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            cout << "Enter element at arr[" << i << "][" << j << "]: ";
            cin >> arr2d[i][j];
        }
    }
    Array1D arr1d = arr2d;
    cout << "Flattened 1D array elements: \n";
    for (int i = 0; i < r * c; i++) {
        cout << arr1d[i] << " ";
    }
}