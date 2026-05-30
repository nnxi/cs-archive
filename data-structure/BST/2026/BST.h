#include <iostream>
using namespace std;

struct node {
    char Key;
    node* LChild;
    node* RChild;
};

typedef node* Nptr;

void Insert(char Key, Nptr& T);
void Delete(char Key, Nptr& T);
void Search(char Key, Nptr T);
void SuccessorCopy(Nptr& T, char& Key);
void Preorder(Nptr T);
void Inorder(Nptr T);
void Postorder(Nptr T);