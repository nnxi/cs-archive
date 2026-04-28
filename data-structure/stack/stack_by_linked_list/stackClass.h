#include "listClass.h" 

class stackClass {
private: 
    listClass L;
    static const int MAX = 100;

public:
    stackClass();

    stackClass(const stackClass& S);

    ~stackClass();

    void Push(int Item);

    int Pop();

    bool IsEmpty();

    bool IsFull();
};  