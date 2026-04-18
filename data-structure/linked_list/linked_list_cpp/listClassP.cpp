#include <iostream>
#include "listClassP.h"
using namespace std;

listClass::listClass() {
    Count = 0;
    Head = NULL;
}

listClass::listClass(const listClass &L) {
    Count = L.Count;

    if (L.Head == NULL) {
        Head = NULL;
    }
    else {
        Head = new node;
        Head->Data = L.Head->Data;

        Nptr Temp1 = Head;
        for (Nptr Temp2 = L.Head->Next; Temp2 != NULL; Temp2 = Temp2->Next) {
            Temp1->Next = new node;
            Temp1 = Temp1->Next;
            Temp1->Data = Temp2->Data;
        }

        Temp1->Next = NULL;
    }
}

listClass::~listClass() {
    while (!IsEmpty()) {
        Delete(1);
    }
}

void listClass::Insert(int Position, int Item) {
        if (Position > (Count + 1) || Position < 1) {
        cout << "Invalid Position";
    }
    else {
        Nptr p = (node*)malloc(sizeof(node));
        p->Data = Item;

        if (Position == 1) {
            p->Next = Head;
            Head = p;
        }
        else {
            Nptr Temp = Head;

            for (int i = 1; i < (Position - 1); i++) {
                Temp = Temp->Next;
            }

            p->Next = Temp->Next;
            Temp->Next = p;
        }

        Count++;
    }
}

void listClass::Delete(int Position) {
    if (IsEmpty()) {
        cout << "List Empty";
    }
    else if (Position > Count || Position < 1) {
        cout << "Invalid Position";
    }
    else {
        Nptr p;

        if (Position == 1) {
            p = Head;
            Head = Head->Next;
        }
        else {
            Nptr Temp = Head;

            for (int i = 1; i < (Position - 1); i++) {
                Temp = Temp->Next;
            }

            p = Temp->Next;
            Temp->Next = p->Next;
        }

        Count--;
        delete(p);
    }
}

void listClass::Retrieve(int Position, int &Item) {
    Nptr p = Head;

    for (int i = 1; i < Position; i++) {
        p = p->Next;
    }

    Item = p->Data;
}

bool listClass::IsEmpty() {
    return (Count == 0);
}

int listClass::Length() {
    return Count;
}