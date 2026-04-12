#define SIZE 300000
#define SEED 12345
#include <iostream>
#include <random>
#include <time.h>
using namespace std;

int a[SIZE];
void quick_sort(int arr[], int left, int right);

int main() {
	time_t start, end;

	srand(SEED);
	for (int i = 0; i < SIZE; i++)
		a[i] = rand() % 500000 + 1;

	start = clock();

	quick_sort(a, 0, SIZE - 1);

	end = clock();

	double time = (double)(end - start) / CLOCKS_PER_SEC;

	cout << "검증용 정렬 후 a[99999] : " << a[99999] << "\n";
	cout << "실행시간 : " << time << "초";
}

void quick_sort(int arr[], int left, int right) {
	if (left < right) {
		int k = right;
		int pivot = arr[k];

		int temp = arr[left];
		arr[left] = arr[k];
		arr[k] = temp;

		int low = left + 1;
		int high = right;

		while (low <= high) {
			while (arr[low] < pivot)
				low++;

			while (arr[high] > pivot)
				high--;

			if (low <= high) {
				temp = arr[low];
				arr[low] = arr[high];
				arr[high] = temp;
				low++;
				high--;
			}
		}

		temp = arr[high];
		arr[high] = arr[left];
		arr[left] = temp;

		quick_sort(arr, left, high - 1);
		quick_sort(arr, high + 1, right);
	}
}
