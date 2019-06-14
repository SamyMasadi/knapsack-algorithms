File: knapsack_problem.py
Author: Samy Masadi

	The program presents and tests three different potential solutions to the 0-1 knapsack problem.
Given a knapsack weight capacity and a list of items with weights and values, determine
the combination of items that fits in the knapsack.

Three methods are presented:
	Brute Force: The method performs an exhaustive search through every possible combination of items.
	Dynamic Programming: The method determines a best value for a certain capacity to weight by building upon
previously calculated best values for smaller capacities to weights. It saves the values for later best
value determinations
	Greedy Ratio: The method simply finds and pick the item with the best value/weight ratio that fits in
the knapsack. Keep picking until no more items can be added to the knapsack.

	Performance tests range from small 5-item, 6-capacity example to a large 10000, 10000 example.
Test 1 tests the provided example.
Test 2 is a 20,20 test that is created specifically to demonstrate a non-optimal solution from the greedy method.
Test 3 is a 27,27 test that shows the practical limits of the brute force method.
Test 4 checks performance of Greedy and Dynamic on a 5000,5000 example.
Test 5 checks performance of Greedy and Dynamic on a 10000,10000 example.
Tests 3-5 contain randomly generated weights and values

	Keep track of performance times then print the results in a chart to make time comparisons easy.

Required for use: Python 3.0 or later version must be installed.

To run in Windows command line:
Double-click the knapsack_problem.py file or navigate to the file's directory and
enter "knapsack_problem.py".

To run in IDLE Python Shell:
1. Run IDLE.
2. Click "File" then "Open".
3. Navigate to "knapsack_problem.py" then click "Open".
4. To run the program, Press F5 on the keyboard, or click "Run" then "Run Module".