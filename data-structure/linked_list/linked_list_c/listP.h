#pragma once
#define MAX 100
#include <stdbool.h>

typedef struct nodeRecord {
    int Data;
    struct nodeRecord *Next;
} node;
typedef node *Nptr;

typedef struct {
    int Count;
    Nptr Head;
} listType;
typedef listType *Lptr;

void Insert(listType *Lptr, int Position, int Item);

void Delete(listType *Lptr, int Position);

void Retrieve(listType *Lptr, int Position, int *ItemPtr);

void Init(listType *Lptr);

bool IsEmpty(listType *Lptr);

int Length(listType *Lptr);