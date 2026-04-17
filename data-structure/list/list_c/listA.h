#pragma once
#define MAX 100
#include <stdbool.h>

typedef struct { 
    int Count;
    int Data[MAX];
} listType;

void Insert(listType *Lptr, int Position, int Item);

void Delete(listType *Lptr, int Position);

void Retrieve(listType *Lptr, int Position, int *ItemPtr);

void Init(listType *Lptr);

bool IsEmpty(listType *Lptr);

int Length(listType *Lptr);