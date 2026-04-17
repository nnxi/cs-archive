#include <stdio.h>
#include <stdlib.h>
#include "listP.h"

void Insert(listType *Lptr, int Position, int Item) {
    if (Position > (Lptr->Count + 1) || Position < 1) {
        printf("Invalid Position");
    }
    else {
        Nptr p = (node*)malloc(sizeof(node));
        p->Data = Item;

        if (Position == 1) {
            p->Next = Lptr->Head;
            Lptr->Head = p;
        }
        else {
            Nptr Temp = Lptr->Head;

            for (int i = 1; i < (Position - 1); i++) {
                Temp = Temp->Next;
            }

            p->Next = Temp->Next;
            Temp->Next = p;
        }

        Lptr->Count++;
    }
}

void Delete(listType *Lptr, int Position) {
    if (IsEmpty(Lptr)) {
        printf("List Empty");
    }
    else if (Position > Lptr->Count || Position < 1) {
        printf("Invalid Position");
    }
    else {
        Nptr p;

        if (Position == 1) {
            p = Lptr->Head;
            Lptr->Head = Lptr->Head->Next;
        }
        else {
            Nptr Temp = Lptr->Head;

            for (int i = 1; i < (Position - 1); i++) {
                Temp = Temp->Next;
            }

            p = Temp->Next;
            Temp->Next = p->Next;
        }

        Lptr->Count--;
        free(p);
    }
}

void Retrieve(listType *Lptr, int Position, int *ItemPtr) {
    Nptr p = Lptr->Head;

    for (int i = 1; i < Position; i++) {
        p = p->Next;
    }

    *ItemPtr = p->Data;
}

void Init(listType *Lptr) {
    Lptr->Count = 0;
    Lptr->Head = NULL;
}

bool IsEmpty(listType *Lptr) {
    return (Lptr->Count == 0);
}

int Length(listType *Lptr) {
    return Lptr->Count;
}