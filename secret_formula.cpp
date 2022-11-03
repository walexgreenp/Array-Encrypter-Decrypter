#include <iostream>
#include <cmath>
using namespace std;

int secret_formula_apply(int x, int y, int m){
    int e = 7;
    int n = x*y;
    int c = (int)pow(m,e)%n; //use power from previous assignments

    //don’t worry about the typecast, just treat everything as an int in MIPS

    return c;
}

int main(){
    int a = 3, b = 11;
    int arr[10] = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};
    int c_arr[10], m_arr[10];
    //your arr (krabby in the template) should be unchanged
    for (int i = 0; i < 10; i++){
        c_arr[i] = secret_formula_apply(a, b, arr[i]);
    }
    for (int i = 0; i < 10; i++){
        std::cout << c_arr[i] << endl;
    }

}