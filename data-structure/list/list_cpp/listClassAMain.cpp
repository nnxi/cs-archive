#include <iostream>
#include "listClassA.h"
using namespace std;

void printList(listClass L);

int main() {
    // L1 선언
    listClass L1;

    // L1에 값 삽입
    for (int i = 1; i <= 10; i++) {
        L1.Insert(i, i);
    }

    // L1 출력
    int tmp;
    cout << "\nL1 : ";
    printList(L1);

    // L1 두 번째 원소 삭제
    L1.Delete(2);
    cout << "\nL1.Delete(2)\n";

    // L1 출력
    cout << "\nL1 : ";
    printList(L1);

    // L2 생성 (복사생성자 호출)
    listClass L2 = L1;
    cout << "\nL2 생성\n";

    // L1, L2 출력
    cout << "\nL1 : ";
    printList(L1);
    cout << "L2 : ";
    printList(L2);

    // L2 첫 번째 원소 삭제
    L2.Delete(1);
    cout << "\nL2.Delete(1)\n";

    // L1, L2 출력
    cout << "\nL1 : ";
    printList(L1);
    cout << "L2 : ";
    printList(L2);
}

// 출력 전용 함수
void printList(listClass L) {
    int tmp;

    cout << "[";
    for (int i = 1; i <= L.Length(); i++) {
        // Retrieve() 사용
        L.Retrieve(i, tmp);

        cout << " " << tmp << " ";
    }
    cout << "]\n";
}