const int MAX = 100;

class listClass {
    private:
        int Count;
        int Data[MAX];

    public:
        listClass();

        listClass(const listClass& L);

        ~listClass();

        void Insert(int Position, int Item);

        void Delete(int Position);

        void Retrieve(int Position, int & Item);

        bool IsEmpty();

        int Length();
};