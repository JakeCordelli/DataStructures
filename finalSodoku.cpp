// ConsoleApplication1.cpp : Defines the entry point for the console application.
//The purpose of this program is to complete a sudoku board given only a few inputs as the initial data set.This is useful for solving an actual sudoku puzzle, 
//since you can simply input the given numbers into the vector in the program and the computer will output the numbers that must fit in the board
//(therefore solving the puzzle).

#include "stdafx.h"
#include <iostream>
#include "stdafx.h"
#include <vector>

//this boolean method iterates through each row of the board to see if there is an opening 
bool checkRow(int r, int val, std::vector <std::vector<int>> & BRD)
{
	for (auto item : BRD.at(r))
		//if an item is present, return false  (no opening)
		if (val == item) return false;
	//else, return true if there is no value there (there is an opening)
	return true;
}

//this boolean method iterates through each collumn of the board to see if there is an opening 

bool checkCol(int c, int val, std::vector <std::vector<int>> & BRD)
{
	for (auto item : BRD)
		//if an item is present, return false (no opening) 
		if (val == item.at(c)) return false;
	//else, return true if there is no value there (there is an opening)
	return true;
}

//This boolean method uses the information from the above methods to compute waether or not there is an opening at
//a specific coordinate on the board (ultimately, see if there is an open block). 
bool checkBlk(int blkr, int blkc, int val, std::vector <std::vector<int>> & BRD)
{
	//for each collumn
	for (int r = 0;r<3;r++)
		//for each row
		for (int c = 0;c<3;c++)
			//if there is an item present, return false (no open block)
			if (val == BRD.at(blkr+r).at(blkc+c)) return false;

	//else, return true (there is an open block). 
	return true;
}

//this boolean method checks to see the location of the open block
bool checkLoc(int r, int c, int val, std::vector <std::vector<int>> & BRD)
{
	//new variables are defined in order to store the location of each block
	//The variables here are divided by three in order to give the position for the open block
	int blk_row = (r / 3) * 3;
	int blk_col = (c / 3) * 3;

	//returns the output of all of the methods from above given the inputs from the main
	return checkRow(r, val, BRD)&checkCol(c, val, BRD)&checkBlk(blk_row, blk_col, val, BRD);
}

//This is where the magic happens...

bool solve(std::vector <std::vector<int>> & BRD)
{
	std::vector<int> possibles{ 1, 2, 3, 4, 5, 6, 7, 8, 9 };
	int r, c;
	r = 0;
	bool empty = false;
	// dump board
	
	//iterate through each row of the board
	for (auto row : BRD)
	{
		c = 0;
		//iterate through ech collumn of the board
		for (auto ch : row)
		{
			if (ch == 0)
			{
				empty = true;
				break;
			}
			c++;
		}
		if (empty)break;
		r++;
	}

	// no empty solved
	if (!empty) return(true);
	// otherwise try something

	//try all of the possibility values in the vector through each block on the board 
	for (auto val : possibles)
	{
		if (checkLoc(r, c, val, BRD))
		{
			BRD.at(r).at(c) = val;
			
			if (solve(BRD)) {
				
				return true;
			}
		}
	}

	// backup
	BRD.at(r).at(c) = 0;
	return false;
}

/*
106400000
050730009
000080500
000500907
008000200
901008000
005020000
300047010
000009602

Evil 1,474,316,561*/

int main(int argc, _TCHAR* argv[])
{
	//a partially filled in sodoku boars is initialized at the beginning of the main method
	std::vector <std::vector<int>>  BRD =
	{
		{ 1,0,6,4,0,0,0,0,0 },
		{ 0,5,0,7,3,0,0,0,9 },
		{ 0,0,0,0,8,0,5,0,0 },
		{ 0,0,0,5,0,0,9,0,7 },
		{ 0,0,8,0,0,0,2,0,0 },
		{ 9,0,1,0,0,8,0,0,0 },
		{ 0,0,5,0,2,0,0,0,0 },
		{ 3,0,0,0,4,7,0,1,0 },
		{ 0,0,0,0,0,9,6,0,2 }
	};

	// dump board
	// prints out the original vector initialized above
	for (auto row : BRD)
	{

		for (auto ch : row)
		{

			std::cout << ch;
		}
		std::cout << std::endl;

	}

	//the program is thinking
	std::cout << "NOT Thinking " << std::endl;

	//the solve method is called and the board is printed accordingly
	solve(BRD);
	// dump board
	for (auto row : BRD)
	{

		for (auto ch : row)
		{
			
			std::cout << ch;
		}
		std::cout << std::endl;
		
	}

	return 0;
}