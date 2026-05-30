#include "BST.h"

void Insert(char Key, Nptr& T) {
    if (T == NULL) {
        T = new node;
        T->Key = Key;
        T->LChild = NULL;
        T->RChild = NULL;
    }
    else if (T->Key > Key)
        Insert(Key, T->LChild);
    else 
        Insert(Key, T->RChild);
}

void Delete(char Key, Nptr& T) {
    if (T == NULL)
        cout << "No Record with Such Key: " << Key << "\n";
    else if (T->Key > Key)
        Delete(Key, T->LChild);
    else if (T->Key < Key)
        Delete(Key, T->RChild);
    else if (T->Key == Key) {
        if (T->LChild == NULL && T->RChild == NULL) {
            Nptr Temp = T;
            T = NULL;
            delete Temp;
        }
        else if (T->LChild == NULL) {
            Nptr Temp = T;
            T = T->RChild;
            delete Temp;
        }
        else if (T->RChild == NULL) {
            Nptr Temp = T;
            T = T->LChild;
            delete Temp;
        }
        else 
            SuccessorCopy(T->RChild, T->Key);
    }
}

void Search(char Key, Nptr T) {
    if (T == NULL) 
        cout << "No Such Node: " << Key << "\n"; 
    else if (T->Key == Key)
        cout << "Found: " << T->Key << "\n";
    else if (T->Key > Key)
        Search(Key, T->LChild); 
    else
        Search(Key, T->RChild);
}

void SuccessorCopy(Nptr& T, char& Key) {
    if (T->LChild == NULL) {
        Key = T->Key;
        Nptr Temp = T;
        T = T->RChild;
        delete Temp;
    }
    else {
        SuccessorCopy(T->LChild, Key);
    }
}

void Preorder(Nptr T) {
    if (T == NULL)
        return;
    cout << T->Key;
    Preorder(T->LChild);
    Preorder(T->RChild);
}

void Inorder(Nptr T) {
    if (T == NULL)
        return;
    Inorder(T->LChild);
    cout << T->Key;
    Inorder(T->RChild);
}

void Postorder(Nptr T) {
    if (T == NULL)
        return;
    Postorder(T->LChild);
    Postorder(T->RChild);
    cout << T->Key;
}