#include "BST.h"

int main() {
    Nptr T;

    T = NULL;

    Insert('K', T);
    Insert('C', T);
    Insert('P', T); 
    Insert('D', T);
    Insert('B', T); 
    Insert('E', T); 
    Insert('R', T); 
    Insert('U', T);
    Insert('S', T);
    Insert('M', T);

    Search('D', T);

    cout << "Inorder: ";
    Inorder(T);
    cout << endl;

    cout << "Preorder: ";
    Preorder(T);
    cout << endl;

    cout << "Postorder: ";
    Postorder(T);
    cout << endl;

    Delete('B', T);
    Delete('D', T);
    Delete('K', T);
    Search('D', T);

    cout << "Inorder after deletion: ";
    Inorder(T);
    cout << endl;

    cout << "Preorder after deletion: ";
    Preorder(T);
    cout << endl;

    cout << "Postorder after deletion: ";
    Postorder(T);
    cout << endl;

    return 0;
}