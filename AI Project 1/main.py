"""
main.py is the primary module for this program. It contains the main function as well as some additional functions that
perform sorting and searching rolls based off of the selections in main.
Author: Nicholas Duncan
Version: 2/4/2022
Email: N01451197@unf.edu
"""
# Import package for manipulating csv files
import csv
import State


def statereport(slist):
    """
    Fix formatting
    The statereport function is responsible for printing out a structured list based on an inputted list.
    :param slist: A list containing state objects.
    :return None, prints out a list.
    :raise None, it is assumed that a proper list will be accepted on program start.
    """
    print("StateReport\n")
    print("Name\t\tMHI\t\tVCR\t\tCFR\t\tCase Rate\t\tDeath Rate\t\tFVR")
    print("------------------------------------------------------------------------")

    # Print out all entries within the stateList list
    # From 0 to the range established by the total length of the list
    # CFR rounded to 6 places, Case Rate and Death Rate to 2, FVR to 3
    for i in range(len(slist)):
        print(slist[i].getstatename() + "\t" + str(slist[i].getstatemedhouseincome()) + "\t" +
              str(slist[i].getstatevcrimerate()) + "\t" + str(round(slist[i].getstatecasefatalityrate(), 6)) + "\t" +
              str(round(slist[i].getstatecaserate(), 2)) + "\t" + str(round(slist[i].getstatedeathrate(), 2)) + "\t" +
              str(round(slist[i].getstatevacrates(), 3)))


# Sort by state name via Quick sort
def namesort(slist):
    """
    Completed
    Incorrect sorting with duplicates
    Sorts an inputted list of state objects via quick sort. The leftmost element is selected as the pivot.
    Then the remaining elements are sorted.
    :param slist: A list of state objects
    :return: the same list but sorted, returned implicitly
    """
    # If the list size is one or empty, return
    print(str(len(slist)))
    if len(slist) <= 1:
        return

    # Quicksort functions by selecting a pivot and sorting the rest of the elements around it if they are higher or low
    # The first element will be the pivot for all calls
    fpivot = slist[0]
    # List for holding smaller objects
    llist = []
    # List for holding larger objects
    rlist = []
    # Run throught the list and split the main list between a list of larger elements and smaller or equal
    for i in range(len(slist)):
        # Skip if the object is the same as the pivot
        if slist[i] is fpivot:
            continue
        # Check if an element is larger than pivot
        elif slist[i].getstatename() > fpivot.getstatename():
            print(slist[i].getstatename() + " > " + fpivot.getstatename())
            rlist.append(slist[i])
        # Else place the element into the left list
        else:
            print(slist[i].getstatename() + " < " + fpivot.getstatename())
            llist.append(slist[i])

    # Run quicksort on the two resulting lists if they have anything within them.
    namesort(rlist)
    namesort(llist)
    # Combine the resulting lists
    slist.clear()
    # Place smaller elements
    for i in range(len(llist)):
        slist.append(llist[i])
    # Place pivot or middle element
    slist.append(fpivot)
    # Place larger elements
    for i in range(len(rlist)):
        slist.append(rlist[i])
    print("Combined size: " + str(len(slist)))
    return


# Sort by case fatality rate via Merge sort
def fatalitysort(slist):
    """
    Completed
    Takes in a list of state objects and sorts it via merge sort against the fatality rate. Works by making a
     left and right array, splitting the input array among them until a single element is left, then combining left
     and right arrays by adding the lowest elements first back to the original array.
    :param slist: A list of state objects
    :return: the same list but sorted
    """
    # Print("States sorted by Case Fatality Rate.")
    # Mergesort involves breaking the list in half until there is only lists of size 1 remaining.
    # If the list is greater than 1, split and run recursively again.
    # After it has returned, sort the left and right arrays while combining them.
    if len(slist) > 1:
        # Get the middle value of the list
        # // operater divides rounding to the floor
        middle = len(slist) // 2
        # Split the list into halves and run mergesort on them.
        rightl = slist[middle:]
        leftl = slist[:middle]
        # Run mergesort on each array
        rightl = fatalitysort(rightl)
        leftl = fatalitysort(leftl)
        # Sort the combined array as needed by case fatality right
        # Whichever value has the smallest leftmost value, add it to the combined array first,
        # then increment that array forward
        # i represents the base array, j for the left, k for the right
        i = 0
        j = 0
        k = 0
        # The end goal is to place items into the array from the smallest to the largest elements
        while j < len(leftl) and k < len(rightl):
            # If the right is larger than the left, place left
            if rightl[k].getstatecasefatalityrate() > leftl[j].getstatecasefatalityrate():
                slist[i] = leftl[j]
                j += 1
            # If the left is larger or equal to the right, place right
            else:
                slist[i] = rightl[k]
                k += 1
            # Advance the placeholder list
            i += 1

        # Ensure there were no stragglers from either list
        while j < len(leftl):
            slist[i] = leftl[j]
            j += 1
            i += 1
        while k < len(rightl):
            slist[i] = rightl[k]
            k += 1
            i += 1
        return slist
    # If the array is size 1, it's time to build back up
    else:
        return slist


# Find and print a state based on a given name
def printbyname(slist, mode):
    """
    Sequencial search works, binary does not.
    A function that takes in a boolean mode and a list of objects
    If the mode is true, Call another function to perform a binary search
    If the mode is false, search via a sequencial search within this function
    Takes in a state as input from the user after being called.
    :param slist: A list of state objects
    :param mode: a boolean describing whether to binary or sequencial sort
    :return: Nothing, a report of the matched state will be printed
    :raise: If a valid state is not found, an error will be printed and user will be returned to the menu
    """
    dstate = input("Enter the desired state, case sensitive: ")
    # if not sorted by name, search via sequencial
    if mode is False:
        print("Searching via sequencial search")
        for i in range(len(slist)):
            # print(slist[i].getstatename())
            if slist[i].getstatename() == dstate:
                # Matching entry found, print the respective report
                slist[i].__str__()
                return
        print("No matching state was found in the file")
        return
    # else use binary search
    elif mode is True:
        print("Searching via binary search")
        index = binarysearch(slist, dstate, 0, len(slist) - 1)
        # print("Returned index: " + str(index))
        if index == -1:
            print("No matching state was found in the file")
            return
        slist[index].__str__()
    else:
        print("How did you mess up the mode?")


def binarysearch(slist, target, leftbound, rightbound):
    """
    Completed
    Supports the previous function, should the array be sorted by name, a binary search is used on the list. The middle
    of the array is calculated by taking the rightbound which starts at the max array size, then subtract by the left,
    divide that by two. If the desired element is larger than the middle, then the new right will be one plus the current
    middle, the new left will be the same. If the desired element is smaller than the new left is one minus the mid.
    :param slist: A list of state objects
    :param target: A string containing the target state
    :param leftbound: sets the leftmost bound of the current iteration's array
    :param rightbound: sets the rightmost bound of the current iteration's array
    :return: Function returns the index of the desired
    :raise: If a valid state is not found, an error will be printed.
    """
    # The list will be sorted by name in this circumstance. Use first letter to help sort.
    # There are no states with 2 of the same letter in the first two characters
    # Python division rounds down, 1/2 = 0
    # Check if the list is a length of one

    # If no matching result is found and the arraysize is 1, Declair that no result can be found
    # If the rightbound has become less than the leftbound, no result could be found
    if rightbound < leftbound:
        return -1
    # Calculate the middle of the current list section
    # First left is the offset if the leftbound had to change, the rightbound is usually the highest part of the list,
    # that is subtracted by the leftbound and divided by 2 and rounded to the nearest floor.
    middle = leftbound + (rightbound - leftbound) // 2
    print(str(middle))
    # Check if the current iteration's center is the target name
    if slist[middle].getstatename() == target:
        return middle

    # gt method will return true if the current state is greater than the target, false otherwise.
    # If current is higher than the target, split and check the left, else check right
    if slist[middle].__gt__(target) is False:
        print("Target is higher than the middle of this list")
        return binarysearch(slist, target, middle + 1, rightbound)
    else:
        print("Target is lower than the middle of this list")
        return binarysearch(slist, target, leftbound, middle - 1)


def printspearman(slist):
    """
    Complete
    Prints out a spearman's rho matrix based on a given list of state objects. Array are made for each sorting method
    used in the X and Y. These are then individually compared and calculated in a function call. Finally the results
    are printed here.
    :param slist: A list of state objects
    :return: Nothing, prints out the spearman's rho matrix before returning
    """
    popsize = len(slist)
    # Initialize, populate, and sort each list type
    # row lists
    crlist = slist.copy()
    crlist.sort(key=lambda state: state.caserate)
    drlist = slist.copy()
    drlist.sort(key=lambda state: state.deathrate)
    # column lists
    mhilist = slist.copy()
    mhilist.sort(key=lambda state: state.medhouseincome)
    vcrlist = slist.copy()
    vcrlist.sort(key=lambda state: state.vcrimerate)
    fvrlist = slist.copy()
    fvrlist.sort(key=lambda state: state.fullvacrates)

    # X1:CR vs. MHI, X2: CR vs. VCR, X3: CR vs. FVR
    x1 = spearcomp(crlist, mhilist, popsize)
    x2 = spearcomp(crlist, vcrlist, popsize)
    x3 = spearcomp(crlist, fvrlist, popsize)
    # X4:DR vs. MHI, X5: DR vs. VCR, X6: DR vs. FVR
    x4 = spearcomp(drlist, mhilist, popsize)
    x5 = spearcomp(drlist, vcrlist, popsize)
    x6 = spearcomp(drlist, fvrlist, popsize)

    # Formula is 1 - (6 * (sum of d^2) / n * (n^2 - 1))
    # D is the change in position of a specified state from one graph to another
    # n is the total number of elements, in this case n = 50
    print("--------------------------------------------------------------------------")
    print("|\t\t\t|\tMedian Household Income\t|\tViolent Crime Rate\t|\tFall Vaccination Rate\t|")
    print("|\tCase Rate\t|\t" + str(round(x1, 4)) + "\t|\t" + str(round(x2, 4)) + "\t|\t" + str(round(x3, 4)) + "\t|")
    print("|\tDeath Rate\t|\t" + str(round(x4, 4)) + "\t|\t" + str(round(x5, 4)) + "\t|\t" + str(round(x6, 4)) + "\t|")


def spearcomp(list1, list2, listsize):
    """
    Complete
    Takes in two lists, one representing a list sorted by an X axis parameter and the other sorted by a Y paremeter.
    Involves calculating the index different for a state between two arrays adding that to a sum for all state
    combinations. Finaly a final calculation is returned as per the given formula for the Spearman's Rho
    :param list1: A list of state objects sorted by one of the X specified parameters
    :param list2: A list of state objects sorted by one of the Y specified parametewr
    :param listsize: takes in the size of the main list that the two input lists are based off of
    :return: The total calculation for a specific combination of lists
    """
    # iterate through the first list while searching for a match in the second
    # take the absolute difference in rank, square it, and add it to the sum.
    dsqsum = 0
    for i in range(len(list1)):
        for j in range(len(list2)):
            if list2[j].getstatename() is list1[i].getstatename():
                # print("i: " + list1[i].getstatename() + str(i) + " j: " + list2[j].getstatename() + str(j))
                dsqsum += pow((abs((j + 1) - (i + 1))), 2)
                # print(str(dsqsum))
            else:
                continue

    return 1 - ((6 * dsqsum) / (listsize * (listsize * (listsize - 1))))


# Load in the assigned CSV file, throw an error if it is not in the directory
print("Loading CSV File")
try:
    file = open("States.csv", "r")
except IOError:
    print("File could not be opened, please check that it is in the project directory")
    exit()
lines = csv.reader(file)
print("File read successfully!\n")

# Skip the first line on the reader as it only contains line info
next(lines)
# Initialize a list to store states
stateList = []
# Tokenize the entire CSV into a 2D array
# curList = 0
for line in lines:
    stateList.append(State.State(line[0], line[1], line[2], line[3], line[4],
                                 line[5], line[6], line[7], line[8], line[9]))
    # print(stateList[curList].__str__())
    # curList += 1

print("There were " + str(State.State.stateCount) + " state records from file")

# Variables used to help with decision-making
namesorted = False
while True:
    print("1. Print a state report")
    print("2. Sort by name")
    print("3. Sort by case fatality rate")
    print("4. Find and print a state for a given name")
    print("5. Print a Spearman's rho matrix")
    print("6. Quit")
    choice = input("Enter a number between ")
    # If the choice is 1 print a state report
    if choice == "1":
        statereport(stateList)
    # If the choice is 2, sort by state name
    elif choice == "2":
        namesorted = True
        namesort(stateList)
    # If the choice is 3, sort by fatality rate
    elif choice == "3":
        namesorted = False
        stateList = fatalitysort(stateList)
    # If the choice is 4, print a state based on a given name
    elif choice == "4":
        printbyname(stateList, namesorted)
    # If the choice is 5
    elif choice == "5":
        printspearman(stateList)
    # If the choice is 6
    elif choice == "6":
        print("Have a good day!\n")
        break
    # If the choice is somehow invalid
    else:
        continue
    # End of while loop

# Close the file and end the program
file.close()
