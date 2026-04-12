#define SIZE 300000
#define SEED 12345
#include <iostream>
#include <random>
#include <time.h>
using namespace std;

int a[SIZE];
int copy_a[SIZE];
void merge_sort(int arr[], int left, int right);
void merge(int arr[], int left, int mid, int right);

int main() {
	time_t start, end;

	srand(SEED);
	for (int i = 0; i < SIZE; i++)
		a[i] = rand() % 500000 + 1;

	start = clock();

	merge_sort(a, 0, SIZE - 1);

	end = clock();

	double time = (double)(end - start) / CLOCKS_PER_SEC;

	cout << "검증용 정렬 후 a[99999] : " << a[99999] << "\n";
	cout << "실행시간 : " << time << "초";
}

void merge_sort(int arr[], int left, int right) {
	if (left < right) {
		int mid = (left + right) / 2;

		merge_sort(arr, left, mid);
		merge_sort(arr, mid + 1, right);
		merge(arr, left, mid, right);
	}
}

void merge(int arr[], int left, int mid, int right) {
	int f = left;
	int m = mid + 1;

	int pointer = 0;

	while (f <= mid && m <= right) {
		if (arr[f] < arr[m]) {
			copy_a[pointer] = arr[f];
			f++;
		}
		else {
			copy_a[pointer] = arr[m];
			m++;
		}
		pointer++;
	}
	if (f <= mid) {
		while (f <= mid) {
			copy_a[pointer] = arr[f];
			pointer++;
			f++;
		}
	}
	else {
		while (m <= right) {
			copy_a[pointer] = arr[m];
			pointer++;
			m++;
		}
	}
	for (int i = left; i <= right; i++) {
		arr[i] = copy_a[i - left];
	}
}
