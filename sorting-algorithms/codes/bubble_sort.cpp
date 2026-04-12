#define SIZE 300000
#define SEED 12345
#include <iostream>
#include <random>
#include <time.h>
using namespace std;

int a[SIZE];
void bubble_sort(int arr[], int size);

int main() {
	time_t start, end;

	srand(SEED);
	for (int i = 0; i < SIZE; i++)
		a[i] = rand() % 500000 + 1;

	start = clock();

	bubble_sort(a, SIZE);

	end = clock();

	double time = (double)(end - start) / CLOCKS_PER_SEC;

	cout << "검증용 정렬 후 a[99999] : " << a[99999] << "\n";
	cout << "실행시간 : " << time << "초";
}

void bubble_sort(int arr[], int size) {
	for (int i = size - 1; i > 0; i--) {
		for (int j = 0; j < size; j++) {
			if (arr[j] > arr[j + 1]) {
				int temp = arr[j];
				arr[j] = arr[j + 1];
				arr[j + 1] = temp;
			}
		}
	}
}
