// finalHeapSort.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"

//  Code implementation and execution with the help from:
//  http://www.sanfoundry.com/cpp-program-sort-array-10-elements-using-heap-sort-algorithm/
//  Implemented and modified by Jake Cordelli


#include <iostream>
using namespace std;


//a[] is the new array for the values
void min_heapify(int *a, int i, int n)
{
	int j, temp;
	temp = a[i];
	j = 2 * i;
	//all used to find the value of the greates element in the array
	while (j <= n)
	{
		if (j < n && a[j + 1] > a[j])
			j = j + 1;
		if (temp > a[j])
			break;
		else if (temp <= a[j])
		{
			a[j / 2] = a[j];
			j = 2 * j;
		}
	}
	a[j / 2] = temp;
	//returns the greatest value in the original array which will
	//be used in the new array (a[])
	return;
}
//Input is an unsorted arra of length m
void heapsort(int *a, int n)
{
	int i, temp;
	//the loop runs in order to build the heap in the new array so that the largest 
	//value is at the root
	for (i = n; i >= 2; i--)
	{
		//a[] is the new vector/array
		temp = a[i];
		//swap the value at a[i] with a[0]
		a[i] = a[1];
		a[1] = temp;
		//reduce the heap size by 1
		min_heapify(a, 1, i - 1);
	}
}

//In order to build the heap, an array is passed in as well as the length of that array
void build_minheap(int *a, int n)
{
	int i;


	for (i = n / 2; i >= 1; i--)
	{
		min_heapify(a, i, n);
	}
}
int main()
{

	//Elements in the array (TURN THIS INTO A VECTOR)
	int a[] = { 1, 4, 16, 30, 29, 18, 100, 2, 43, 1 };


	int i;
	int n = 9;

	cout << "Original input: ";
	//Prints the original array
	for (i = 0; i<10; i++) {
		cout << a[i] << ", ";
	}

	//call the min_heap function
	build_minheap(a, n);

	//call the heap sort function
	heapsort(a, n);
	cout << endl;
	cout << "Sorted output: ";
	for (i = 0; i <= n; i++)
	{
		cout << a[i] << ", ";
	}
	cout << endl;



	return 0;
}
