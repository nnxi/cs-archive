#include <iostream>
using namespace std;

typedef struct nodeRecord {
	int Key;
	nodeRecord* LChild;
	nodeRecord* RChild;
} node;

typedef node* Nptr;

Nptr Insert (Nptr T, int Key) {
	if (T == NULL) {
		T = (node*)malloc(sizeof(node));
		T->Key = Key;
		T->LChild = NULL;
		T->RChild = NULL;
	}
	else if (T->Key > Key) {
		T->LChild = Insert(T->LChild, Key);
	}
	else {
		T->RChild = Insert(T->RChild, Key);
	}
	return T;
}

void SC (Nptr& T, Nptr& DelNodeData) {
	if (T->LChild == NULL) {
		DelNodeData->Key = T->Key;
		Nptr temp = T;
		T = T->RChild;
		delete temp;
	}
	else {
		SC(T->LChild, DelNodeData);
	}
}

void Delete (Nptr& T, int Key) {
	if (T == NULL) {
		cout << "No Record with such Key\n";
	}
	else if (T->Key > Key) {
		Delete(T->LChild, Key);
	}
	else if (T->Key < Key) {
		Delete(T->RChild, Key);
	}
	else if (T->Key == Key) {
		if (T->LChild == NULL && T->RChild == NULL) {
			Nptr temp = T;
			T = NULL;
			delete temp;
		}
		else if (T->LChild == NULL) {
			Nptr temp = T;
			T = T->RChild;
			delete temp;
		}
		else if (T->RChild == NULL) {
			Nptr temp = T;
			T = T->LChild;
			delete temp;
		}
		else {
			SC(T->RChild, T);
		}
	}
}

void PreOrder(Nptr T) {
	if (T != NULL) {
		cout << T->Key << "\n";
		PreOrder(T->LChild);
		PreOrder(T->RChild);
	}
}

void InOrder(Nptr T) {
	if (T != NULL) {
		InOrder(T->LChild);
		cout << T->Key << "\n";
		InOrder(T->RChild);
	}
}

void PostOrder(Nptr T) {
	if (T != NULL) {
		PostOrder(T->LChild);
		PostOrder(T->RChild);
		cout << T->Key << "\n";
	}
}

void main() {
	Nptr R = NULL;
	R = Insert(R, 43);
	R = Insert(R, 53);
	R = Insert(R, 69);
	R = Insert(R, 72);
	R = Insert(R, 14);
	R = Insert(R, 32);
	R = Insert(R, 43);
	R = Insert(R, 17);
	R = Insert(R, 39);
	R = Insert(R, 56);
	R = Insert(R, 41);

	cout << "\nInOrder : \n";
	InOrder(R);

	cout << "\nPreOrder : \n";
	PreOrder(R);

	cout << "\nPostOrder : \n";
	PostOrder(R);

	cout << "\nDelete : 69\n";
	Delete(R, 69);

	cout << "\nDelete : 17\n";
	Delete(R, 17);

	cout << "\nInOrder : \n";
	InOrder(R);

	cout << "\nPreOrder : \n";
	PreOrder(R);

	cout << "\nPostOrder : \n";
	PostOrder(R);
}
