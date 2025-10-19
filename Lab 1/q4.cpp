#include <iostream>
using namespace std;

class Array1D {
    private:
        int *arr;
        int size;
    public:
        Array1D(int s) : size(s) {
            arr = new int[size];
        }
        int& operator[](int index) {
            return arr[index];
        }
        // Binary search
        int find(int key) {
            int l=0, r=size-1;
            while (l <= r) {
                int mid = l + (r - l) / 2;
                if (arr[mid] == key) return mid;
                else if (arr[mid] < key) l = mid + 1;
                else r = mid - 1;
            }
            return -1;
        }
        ~Array1D() {
            delete[] arr;
        }
};

int main() {
    cout << "Enter size of 1D array: ";
    int s;
    cin >> s;
    Array1D arr(s);
    cout << "Enter elements in sorted order: ";
    for (int i = 0; i < s; i++) {
        cin >> arr[i];
    }
    cout << "Enter element to search: ";
    int key;
    cin >> key;
    int index = arr.find(key);
    if (index != -1) {
        cout << "Element found at index " << index << endl;
    } else {
        cout << "Element not found" << endl;
    }
    return 0;
}