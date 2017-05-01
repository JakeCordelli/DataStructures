//  Code implementation and execution with the help from:
//  http://www.sanfoundry.com/cpp-program-sort-array-10-elements-using-heap-sort-algorithm/
//  Implemented and modified by Jake Cordelli


#include <iostream>
using namespace std;

void min_heapify(int *a, int i, int n)
{
    int j, temp;
    temp = a[i];
    j = 2*i;
    while (j <= n)
    {
        if (j < n && a[j+1] > a[j])
            j = j+1;
        if (temp > a[j])
            break;
        else if (temp <= a[j])
        {
            a[j/2] = a[j];
            j = 2*j;
        }
    }
    a[j/2] = temp;
    return;
}
void heapsort(int *a, int n)
{
    int i, temp;
    for (i = n; i >= 2; i--)
    {
        temp = a[i];
        a[i] = a[1];
        a[1] = temp;
        min_heapify(a, 1, i - 1);
    }
}

//In order to build the heap, an array is passed in as well as the length of that array
void build_minheap(int *a, int n)
{
    int i;
    
    for(i = n/2; i >= 1; i--)
    {
        min_heapify(a, i, n);
    }
}
int main()
{

    //Elements in the array (TURN THIS INTO A VECTOR)
    int a[] = {1, 4, 16, 30, 29, 18, 100, 2, 43, 1};


    int i;
    int n=9;
    
    cout<<"Original input: ";
    //Prints the original array
    for (i=0; i<10; i++){
        cout<<a[i]<<", ";
    }

    
    build_minheap(a,n);
    heapsort(a, n);
    cout<<endl;
    cout<<"Sorted output: ";
    for (i = 0; i <= n; i++)
    {
        cout<<a[i]<<", ";
    }
    cout<<endl;
    

    
    return 0;
}