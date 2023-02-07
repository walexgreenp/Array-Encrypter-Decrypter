#include <iostream>
#include <cmath>
using namespace std;

int secret_formula_apply(int x, int y, int m){
    int e = 7;
    int n = x * y;
    int c = (int)pow(m,e) % n;

    // e = 7, n = 33, c = (1) % 33


    return c;
}

int secret_formula_remove(int x, int y, int c){
    int d = 3;
    int n = x*y;
    int z = (int)pow(c,d) % n;

    // d = 3, n = 33, z = 

    return z;
}

int main(){
    int a = 3, b = 11;
    int arr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int c_arr[10], m_arr[10];

    for (int i = 0; i < 10; i++){
        c_arr[i] = secret_formula_apply(a, b, arr[i]);
    }
    for (int i = 0; i < 10; i++) {
        m_arr[i] = secret_formula_remove(a, b, c_arr[i]);
    }


    cout << "Encrypted: ";
    for (int i = 0; i < 10; i++){
        std::cout << c_arr[i];
        if(i != 9){
            cout << ", ";
        }
    }

    cout << endl << "Decrypted: " ;
    for(int i = 0; i < 10; i++){
        std::cout << m_arr[i];
        if(i != 9){
            cout << ", ";
        }
    }
    cout << endl;
}