#include <iostream>
using namespace std;

class Table {
    private:
        float **table;
        int rows, cols, curr_row;

    public:
        Table(int r, int c) : rows(r), cols(c), curr_row(0) {
            table = new float*[rows];
            for (int i=0; i<cols; i++){
                table[i] = new float[cols];
            }
        }
        bool insert(float gpas[], int n){
            for (int i=0; i<n; i++){
                table[curr_row][i] = gpas[i];
            }
            curr_row++;
            return true;
        }
        void get_sem_gpas() {
            for (int i=0; i<rows; i++){
                float gpa=0;
                for (int j=0; j<cols; j++){
                    gpa += table[i][j];
                }
                cout << "GPA for student " << i+1 << " is " << gpa/cols << endl;
            }
        }
};

int main(){
    int rows, cols;
    cout << "Enter number of students: "; cin >> rows;
    cout << "Enter number of subjects: "; cin >> cols;
    Table students(rows, cols);

    for (int i = 0; i < rows; i++) {
        float gpas[3];
        cout << "Enter " << cols << " GPAs for student " << (i+1) << ": ";
        for (int j = 0; j < cols; j++) {
            cin >> gpas[j];
        }
        students.insert(gpas, cols);
    }

    students.get_sem_gpas();
    return 0;
}