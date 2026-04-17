#include <stdio.h>
#include "listA.h"

int main() {
    // 리스트 선언
    listType L;

    // 리스트 초기화
    Init(&L);

    // 리스트에 값 삽입
    for (int i = 1; i <= 10; i++) {
        Insert(&L, i, i);
    }

    // 리스트 출력
    int tmp;
    printf("삭제 전 리스트 [");
    for (int i = 1; i <= Length(&L); i++) {
        Retrieve(&L, i, &tmp);

        printf(" %d ", tmp);
    }
    printf("]\n");

    // 두 번째 원소 삭제
    Delete(&L, 2);

    // 리스트 출력
    printf("삭제 후 리스트 [");
    for (int i = 1; i <= Length(&L); i++) {
        Retrieve(&L, i, &tmp);

        printf(" %d ", tmp);
    }
    printf("]\n");
}