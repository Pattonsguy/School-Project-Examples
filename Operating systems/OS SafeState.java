import java.io.*;
import java.util.LinkedList;
import java.util.Queue;

class Main {
  public static void main(String[] args) {
    //Example will be used is from the homework assignment
    int resourceTypes = 4;
    int processes = 5;
    //Allocation values
    int[][] Allocations = {{0, 0, 1, 2},
                               {1, 0, 0, 0},
                               {1, 3, 5, 4},
                               {0, 6, 3, 2},
                               {0, 0, 1, 4}};
    
    //Max Values
    int[][] Maximums = {{0, 7, 8, 2},
                            {1, 2, 2, 0},
                            {2, 7, 7, 6},
                            {0, 7, 7, 2},
                            {0, 1, 7, 6}};
    //Available resources
    int[] Available = {1, 5, 2, 0};

    //initialize safe sequence array
    Queue<Integer> safeSeq = new LinkedList<>();

    int[] totalAllocation = {0, 0, 0, 0};

    int[][] Need = {{0, 0, 0, 0},
                        {0, 0, 0, 0},
                        {0, 0, 0, 0},
                        {0, 0, 0, 0},
                        {0, 0, 0, 0}};
    
    //Get the total column values, will most likely only work on square matricies
    for(int i = 0; i < (resourceTypes); i++){
      for(int j = 0; j < (processes); j++){
        //Get the total of each resource column to get the total allocation value
        //System.out.println("Column: " + i);
        //System.out.println("Row: " + j);
        totalAllocation[i] += Allocations[j][i];
      }//end for
    }//end for

    //TESTING print totalAllocations
    System.out.print("Total Allocations: ");
    for(int i = 0; i < resourceTypes; i++){
       System.out.print(totalAllocation[i] + " ");
      
    }//end for
    System.out.print("\n");

    //print out allocation matrix and maximums
    System.out.println("Allocation Matrix: ");
    printMatrix(Allocations, resourceTypes, processes);
    System.out.println("Maximum Matrix: ");
    printMatrix(Maximums, resourceTypes, processes);
    //Generate NEED Matrix
    //Need = max - allocation
    System.out.println("Need Matrix: ");
    for(int i = 0; i < processes; i++){
      for(int j = 0; j < resourceTypes; j++){
          Need[i][j] = Maximums[i][j] - Allocations[i][j];
          //System.out.print(Need[i][j] + ", "); 
        }//end for
      //System.out.print("\n");
      }//end for

    //TESTING print Need matrix
    // length, height
    printMatrix(Need, resourceTypes, processes);
    
    //work = available
    int[] work = Available.clone();
    //Set up finish array, will correspond with the height or processes
    boolean[] finish = {false, false, false, false, false};
    //Loop that will cycle through Need until Need is empty
    //For each iteration,
    //Check if Need <= Work
    //If true, set finish[i] to true, add values of allocation[i] onto work
    //If false, leave at false and continue
    int finishcount = 0;
    int prevfinish = 0;
    while(true){
      for(int i = 0; i < processes; i++){
        System.out.println("Current process: " + i);
        //check if the index is already clear, if so skip
        if(finish[i] == true){
          System.out.println("Process: " + i + " Is already true, skipping");
          continue;
        }//end if

        //Should the process's need fit inside work
        if(needworkcmp(resourceTypes, work, Need[i]) == 0){
          finish[i] = true;
          finishcount += 1;
          safeSeq.add(i);
          //Add available[i] to work
          System.out.print("Work update: ");
          for(int a = 0; a < resourceTypes; a++){
            work[a] += Allocations[i][a];
            System.out.print(work[a] + ", ");
          }//end for
          System.out.print("\n");
          continue;
        }//end if
        else{
          System.out.println("Work is not greater than Need in row " + i);
          finish[i] = false;
          continue;
        }//end else
      }//end for
      
        
       //Check if all finish indecies are true, if the check stays the same after another attempt deny. Else accept.
      //System.out.println("Previous finish true count: " + prevfinish);
      //System.out.println("Current finish count: " + finishcount);
      if(finishcount == processes){
        System.out.println("FINISHED: SYSTEM WILL REMAIN IN A SAFE STATE!");
        System.out.println("Safe Sequence: " + safeSeq);
        return;
      }//end if
      //catch if the total finished has been the same the past two attempts.
      else if(finishcount == prevfinish){
        System.out.println("FINISHED: REQUEST DENIED, WOULD LEAVE SYSTEM IN AN UNSAFE STATE!");
        return;
      }//end else if
      //Neither is true, loop again
      else{
        prevfinish = finishcount;
        continue;
      }//end else
    }//end while
  }//end Main Method

  
  //0 if work >= need, 1 if work < need or incomparable
  static int needworkcmp(int resources, int[] work, int[] needed){
    //check each index
    for(int i = 0; i < resources; i++){
      //System.out.println("Work: " + work[i] + " need: " + needed[i]);
      if (work[i] >= needed[i]){
        continue;
      }//end if
      else{
        //A value of need is greater than a value of work, exit 1
        return 1;
      }//end else
    }//end while
    //If all indecies are equal or work is completely better, exit 0
    return 0;
  }//end method

  //Length is the amount of resource types, height is the amount of processes
  static void printMatrix(int[][] matrix, int length, int height){

    for(int i = 0; i < height; i++){
      for(int j = 0; j < length; j++){
        System.out.print(matrix[i][j] + ", ");
      }//end for
      System.out.print("\n");
    }//end for
  }//end method
}//end Class