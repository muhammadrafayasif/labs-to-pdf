#include <iostream>
#include <algorithm>
using namespace std;

class MedianFinder {
    private:
        int* arr;
        int size;
        int capacity;
    public:
        MedianFinder() {
            capacity = 100;
            arr = new int[capacity];
            size = 0;
        }
        void addNum(int num) {
            if (size == capacity) {
                capacity *= 2;
                int* newArr = new int[capacity];
                for (int i = 0; i < size; i++) {
                    newArr[i] = arr[i];
                }
                delete[] arr;
                arr = newArr;
            }
            arr[size++] = num;
        }
        double findMedian() {
            sort(arr, arr + size);
            if (size % 2 == 0) {
                return (arr[size / 2 - 1] + arr[size / 2]) / 2.0;
            } else {
                return arr[size / 2];
            }
        }
        ~MedianFinder() {
            delete[] arr;
        }


};

int main() {
    MedianFinder* medianFinder = new MedianFinder();

    int choice;
    while (true) {
        cout << "1) addNum\n2) findMedian\n3) quit\n=> "; cin >> choice;

        switch (choice) {
            case 1:
                int num;
                cout << "Enter number: "; cin >> num;
                medianFinder->addNum(num);
                cout << endl;
                break;
            
            case 2:
                cout << "The median is: " << medianFinder->findMedian() << endl << endl;
                break;
            
            default:
                delete medianFinder;
                return 0;
        }

    }

    delete medianFinder;
    return 0;
}