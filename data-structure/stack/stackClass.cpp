#include <iostream>
#include "stackClass.h"
using namespace std;

stackClass::stackClass() { }

stackClass::stackClass(const stackClass& S) {
    L = S.L;
}

stackClass::~stackClass() { }

void stackClass::Push(int Item) {
    if (L.Length() >= MAX) {
        cout << "Stack Full";
    }
    else {
        L.Insert(1, Item);
    }
}

int stackClass::Pop() {
    if (IsEmpty()) {
        cout << "Stack Empty";
        return -1;
    }
    else {
        int item;
        L.Retrieve(1, item);

        L.Delete(1);

        return item;
    }
}

bool stackClass::IsEmpty() {
    return bool(L.IsEmpty());
}

bool stackClass::IsFull() {
    if (L.Length() >= MAX) {
        return true;
    }
    else {
        return false;
    }
}