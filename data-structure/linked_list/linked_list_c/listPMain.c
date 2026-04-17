#include <stdio.h>
#include "listP.h"

int main() {
    // 연결리스트 선언
    listType L;

    // 연결리스트 초기화
    Init(&L);

    // 연결리스트에 값 삽입
    for (int i = 1; i <= 10; i++) {
        Insert(&L, i, i);
    }

    // 연결리스트 출력
    int tmp;
    printf("삭제 전 연결리스트 [");
    for (int i = 1; i <= Length(&L); i++) {
        Retrieve(&L, i, &tmp);

        printf(" %d ", tmp);
    }
    printf("]\n");

    // 두 번째 원소 삭제
    Delete(&L, 2);

    // 연결리스트 출력
    printf("삭제 후 연결리스트 [");
    for (int i = 1; i <= Length(&L); i++) {
        Retrieve(&L, i, &tmp);

        printf(" %d ", tmp);
    }
    printf("]\n");
}