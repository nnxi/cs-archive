#include <iostream>
#include "stackClass.h"
using namespace std;

int main() {
    stackClass s;
    int target = 26;
    int tmp;

    while (target > 0) {
        tmp = target % 2;
        s.Push(tmp);
        target = target / 2;
    }

    cout << "26 (decimal) = ";
    while (!s.IsEmpty()) {
        cout << s.Pop() << " ";
    }
    cout << "(binary)\n";
}