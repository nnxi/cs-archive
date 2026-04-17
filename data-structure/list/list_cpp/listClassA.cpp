#include <iostream>
#include "listClassA.h"
using namespace std;

listClass::listClass( ) {
    Count = 0;
}

listClass::listClass(const listClass& L) {
    Count = L.Count;

    for (int i = 1; i <= L.Count; i++) {
        Data[i - 1] = L.Data[i - 1];
    }
}

listClass::~listClass( ) {}

void listClass::Insert(int Position, int Item) {
    if (Count >= MAX) {
        cout << "List Full";
    }
    else if (Position > (Count + 1) || Position < 1) {
        cout << "Invalid Position";
    }
    else {
        for (int i = (Count - 1); i >= (Position - 1); i--) {
            Data[i + 1] = Data[i];
        }

        Data[Position - 1] = Item;
        Count++;
    }
}

void listClass::Delete(int Position) {
    if (IsEmpty()) {
        printf("List Empty");
    }
    else if (Position > (Count - 1) || Position < 1) {
        printf("Invalid Position");
    }
    else {
        for (int i = (Position - 1); i < Count; i++) {
            Data[i] = Data[i + 1];
        }

        Count--;
    }
}

void listClass::Retrieve(int Position, int & Item) {
    Item = Data[Position - 1];
}

bool listClass::IsEmpty() {
    return (Count == 0);
}
int listClass::Length() {
    return Count;
}