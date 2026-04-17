#include <stdio.h>
#include "listA.h"

void Insert(listType *Lptr, int Position, int Item) {
    if (Lptr->Count >= MAX) {
        printf("List Full");
    }
    else if (Position > (Lptr->Count + 1) || Position < 1) {
        printf("Invalid Position");
    }
    else {
        for (int i = (Lptr->Count - 1); i >= (Position - 1); i--) {
            Lptr->Data[i + 1] = Lptr->Data[i];
        }

        Lptr->Data[Position - 1] = Item;
        Lptr->Count++;
    }
}

void Delete(listType *Lptr, int Position) {
    if (IsEmpty(Lptr)) {
        printf("List Empty");
    }
    else if (Position > (Lptr->Count - 1) || Position < 1) {
        printf("Invalid Position");
    }
    else {
        for (int i = (Position - 1); i < Lptr->Count; i++) {
            Lptr->Data[i] = Lptr->Data[i + 1];
        }

        Lptr->Count--;
    }
}

void Retrieve(listType *Lptr, int Position, int *ItemPtr) {
    *ItemPtr = Lptr->Data[Position - 1];
}

void Init(listType *Lptr) {
    Lptr->Count = 0;
}

bool IsEmpty(listType *Lptr) {
    return (Lptr->Count == 0);
}

int Length(listType *Lptr) {
    return Lptr->Count;
}