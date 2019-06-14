# Samy Masadi
# CSCI 423
# 4/12/2019
# Project 4
#
# The program presents and tests three different potential solutions to the 0-1 knapsack problem.
# Given a knapsack weight capacity and a list of items with weights and values, determine
# the combination of items that fits in the knapsack.
#
# Three methods are presented:
# Brute Force: The method performs an exhaustive search through every possible combination of items.
# Dynamic Programming: The method determines a best value for a certain capacity to weight by building upon
#   previously calculated best values for smaller capacities to weights. It saves the values for later best
#   value determinations
# Greedy Ratio: The method simply finds and pick the item with the best value/weight ratio that fits in
#   the knapsack. Keep picking until no more items can be added to the knapsack.
#
# Performance tests range from small 5-item, 6-capacity example to a large 10000, 10000 example.
# Test 1 tests the provided example.
# Test 2 is a 20,20 test that is created specifically to demonstrate a non-optimal solution from the greedy method.
# Test 3 is a 27,27 test that shows the practical limits of the brute force method.
# Test 4 checks performance of Greedy and Dynamic on a 5000,5000 example.
# Test 5 checks performance of Greedy and Dynamic on a 10000,10000 example.
# Tests 3-5 contain randomly generated weights and values
#
# Keep track of performance times then print the results in a chart to make time comparisons easy.
########################################################################################################################

### Import Libraries ###

from itertools import combinations
import time
import random

### Function Definitions ###

# A knapsack solution that determines the best value of items that can fit in a knapsack by performing a
# brute force exhaustive search.
# All possible combinations of items are searched from combinations of size 1 to either the capacity (assume items weigh
#    no less than 1) or the number of items available.
# arr: the list of items to choose from
# cap: the knapsack weight capacity
# returns a list containing indices representing the items chosen.
def bruteForce(arr, cap):
    bestCombo = 0                                       # Will contain the indices of items that make up the best combo
    bestValue = 0                                       # Will keep the current bestValue
    for i in range(1, cap+1):                           # Current combo size
        if (i <= len(arr)):
            for j in combinations(range(0, len(arr)), i): # Iterate through a generated list of combinations, nCr = len(arr)Ci
                weight = 0
                value = 0
                for k in j:                             # k corresponds to an element index in arr
                    weight += arr[k][0]
                    value += arr[k][1]
                if (weight <= cap):                     # The combo must fit in knapsack
                    if (value > bestValue):             # Keep track of best combo and best value found
                        bestValue = value
                        bestCombo = j
    return bestCombo

# A knapsack solution method that dynamically determines the best value of items based on the items available
#   and the capacity available.
# It stores previously calculated best values in a 2D list and uses them in determining the current best value.
# arr: the list of items to choose from
# cap: the knapsack weight capacity
# returns a list containing indices representing the items chosen.
def dynamic(arr, cap):
    valueGraph = []                                     # 2D list to keep save generated best values
    bestCombo = []                                      # Will contain the selected items.
    for i in range(0, len(arr)+1):
        row = [0]
        valueGraph.append(row)                          # Initialize first column with zeros
    for i in range(0, cap):
        valueGraph[0].append(0)                         # Initialize first row with zeros
    for row in range(1, len(arr)+1):
        for col in range(1, cap+1):
            value1 = valueGraph[row-1][col]             
            value2 = arr[row-1][1] + valueGraph[row-1][col-arr[row-1][0]]
            if (col - arr[row-1][0] >= 0):              # if item weight fits
                if (value2 > value1):
                    valueGraph[row].append(value2)      # Take item if it adds value
                else:
                    valueGraph[row].append(value1)      # Do not take item.
            else:
                valueGraph[row].append(value1)          # Do not take item.
    row = len(arr)                                      # Backtrack to determine items selected
    col = cap
    while (row > 0 and col > 0):                        # col (weight) bound check is optional, but may speed backtrack up
        if (col - arr[row-1][0] >= 0):                  # if the item fits
            if (valueGraph[row][col] > valueGraph[row-1][col]):
                bestCombo.append(row-1)                 # item was added
                col -= arr[row-1][0]
                row -= 1
            else:
                row -= 1
        else:
            row -= 1
    return bestCombo

# A knapsack solution method that selects items with the best value/weight ratio
#   that fit in the knapsack. It is a greedy algorithm that is not always optimal.
# arr: the list of items to choose from.
# cap: the weight capacity of the knapsack
# returns a list containing indices representing the items chosen.
def greedyRatio(arr, cap):
    itemsChosen = []
    spaceLeft = cap
    selecting = True
    while (selecting):
        selecting = False                               # If no item is selected, selecting remains False
        bestItem = -1
        bestRatio = 0
        highestValue = 0
        for i in range(0, len(arr)):
            if (i not in itemsChosen):                  # Ignore items already chosen
                if (arr[i][0] <= spaceLeft):            # Weight must fit
                    ratio = arr[i][1] / arr[i][0]       # value / weight
                    if (ratio > bestRatio):             # Always choose better ratio
                        bestRatio = ratio
                        highestValue = arr[i][1]
                        bestItem = i
                    elif (ratio == bestRatio):
                        if (arr[i][1] > highestValue):  # If ratio is equal, choose the greater value
                            bestRatio = ratio
                            highestValue = arr[i][1]
                            bestItem = i
        if (bestItem != -1):
            itemsChosen.append(bestItem)                # Select item for knapsack
            spaceLeft -= arr[bestItem][0]               # Calculate space remaining
            selecting = True
    return itemsChosen

# Prints the items selected for the knapsack
# Uses knapsack elements to access actual item details from items list,
#   ie. items[knapsack[i]][0] == item weight, items[knapsack[i]][1] == item value
# knapsack: the list of selected items; represented as indices applicable to items list
# items: the list of all items
def printKnapsack(knapsack, items):
    totalWeight = 0
    totalValue = 0
    print("Items selected:")
    print("{:^6}{:^8}{:^7}".format("Item", "Weight", "Value"))    
    for i in knapsack:
        totalWeight += items[i][0]
        totalValue += items[i][1]
        if (len(knapsack) <= 6):
            print("{:^6d}{:^8d}{:^7d}".format(i+1, items[i][0], items[i][1]))
    if (len(knapsack) > 6):
        for i in range(0, 5):
            print("{:^6d}{:^8d}{:^7d}".format(knapsack[i]+1, items[knapsack[i]][0], items[knapsack[i]][1]))
        print("* plus",len(knapsack)-5,"more items *")            
    print("Total weight: {:d}".format(totalWeight))
    print("Total value: {:d}".format(totalValue))

# Generates items of random weights and values
# arr: the list to contain the items
# amount: the number of items to generate
def genItems(arr, amount):
    for i in range(0, amount):
        item = []
        item.append(random.randint(1, amount))      # item[0] == weight
        item.append(random.randint(1, amount*10))   # item[1] == value
        arr.append(item)

# Tests Greedy, Dynamic, and Brute Force methods on the input item list and knapsack capacity
# arr: the list of items to choose from
# cap: the knapsack capacity
# returns a list containing the times for each method
def perfTest(arr, cap):
    times = []
    print("Number of items:",len(arr))
    print("Knapsack capacity:",cap,"\n")

    print("Greedy Ratio Method:")
    start = time.perf_counter()
    test = greedyRatio(arr, cap)
    end = time.perf_counter()
    times.append(end-start)
    printKnapsack(test, arr)
    print("Time taken: {:7.6f} seconds\n".format(times[0]))

    print("Dynamic Programming Method:")
    start = time.perf_counter()
    test2 = dynamic(arr, cap)
    end = time.perf_counter()
    times.append(end-start)
    printKnapsack(test2, arr)
    print("Time taken: {:8.6f} seconds\n".format(times[1]))

    print("Brute Force Method:")
    if (len(arr) <= 27):
        if (len(arr) > 25):
            print("This will take about 5 minutes...")
        start = time.perf_counter()
        test3 = bruteForce(arr, cap)
        end = time.perf_counter()
        times.append(end-start)
        printKnapsack(test3, arr)
        print("Time taken: {:9.6f} seconds\n".format(times[2]))
    else:
        print("Too many items for brute force method!\n")
    return times

### Main Program ###

# The given example
example1 = [[3,25],[2,20],[1,15],[4,40],[5,50]]

# Set up example2 items so that the greedy method will not take optimal combo.
example2 = []
example2.append([20,200])
example2.append([1,11])
for i in range(0, 18):
    example2.append([2,18])

# Examples 3-5 will have lists of random weights/values
example3 = []
example4 = []
example5 = []
genItems(example3, 27)
genItems(example4, 5000)
genItems(example5, 10000)

# Performance tests and outputs
print("********************")
print("*{:^18}*".format("Test 1"))
print("********************")
times1 = perfTest(example1, 6)
print("********************")
print("*{:^18}*".format("Test 2"))
print("********************")
times2 = perfTest(example2, 20)
print("********************")
print("*{:^18}*".format("Test 3"))
print("********************")
times3 = perfTest(example3, 27)
print("********************")
print("*{:^18}*".format("Test 4"))
print("********************")
times4 = perfTest(example4, 5000)
print("********************")
print("*{:^18}*".format("Test 5"))
print("********************")
times5 = perfTest(example5, 10000)

print("********************")
print("*Performance Report*")
print("********************")
print("{:^11}{:^9}{:^10}{}".format("Items,Cap", "Greedy", "Dynamic", "Brute Force"))
print("{:^11}{:>9.6f}{:>10.6f}{:>11.6f}".format("5,6", times1[0], times1[1], times1[2]))
print("{:^11}{:>9.6f}{:>10.6f}{:>11.6f}".format("20,20", times2[0], times2[1], times2[2]))
print("{:^11}{:>9.6f}{:>10.6f}{:>11.6f}".format("27,27", times3[0], times3[1], times3[2]))
print("{:^11}{:>9.6f}{:>10.6f}{:^11}".format("5000,5000", times4[0], times4[1], "N/A"))
print("{:^11}{:>9.6f}{:>10.6f}{:^11}".format("10000,10000", times5[0], times5[1], "N/A"))
