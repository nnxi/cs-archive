typedef struct nodeRecord {
    int Data;
    struct nodeRecord *Next;
} node;
typedef node *Nptr;

class listClass {
    private:
        int Count;
        Nptr Head;

    public:
        listClass();

        listClass(const listClass &L);

        ~listClass();

        void Insert(int Position, int Item);

        void Delete(int Position);

        void Retrieve(int Position, int &Item);

        bool IsEmpty();

        int Length();
};