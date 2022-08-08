import java.util.LinkedList;
import java.util.Queue;

class Main {
  public static void main(String[] args) {
    
    //Initialize a queue to act as a buffer for threads to interract with
    Queue<Integer> intQ = new LinkedList<>();
    //initialize a producer and consumer thread with references to the queue object
    Thread producer = new Thread(new Producer(intQ));
    Thread consumer = new Thread(new Consumer(intQ));

    //start both the producer and consumer
    producer.start();
    consumer.start();

    //use SYNC keyword to syncronize threads
    try{
      producer.join();
      consumer.join();
    }//end try
    catch(Exception e){
          System.out.println("Sync was interrupted");
    }//end catch
    //Example 1: Buffer is full and producer is waiting
    //Example 2: Buffer is empty and Consumer is waiting
    //Buffer is partially full
    System.out.println("Goodbye");
  }//end main
}//end class

//Producer class: Sets elements to 1 (FULL)
class Producer implements Runnable{
  //Constructors
  //holds reference to a given queue
  private Queue<Integer> intQ;
  private int sleeptime = 100;
  public Producer(Queue<Integer> intQ){
    this.intQ = intQ;
  }//end constructor
  
  //run method
  public void run(){
    //Use Sync keyword to ensure individual threads sync with one another.
    synchronized(intQ){
      while(true){
        //check if the queue is full, limit is 10
        if(intQ.size() >= 10){
          System.out.println("Producer: Queue is full, producer is waiting");
          //Set the producer to wait for an amount of time.
          //Must have a try block in the event of an exception.
          try{
            intQ.wait(sleeptime);
            //intQ.notify();
          }//end try
          catch(InterruptedException e){
            //print out the error message if something happens to the thread.
            e.printStackTrace();
          }//end catch
        
        }//end if
        //place an item into the queue
        intQ.add(1);
        System.out.println("Producer: Adding element to queue");
        //wake up any threads in waiting, notably the consumer
        //notify();
      }//end while
    }//end sync
  }//end run
}//end class

//Consumer class: sets elements to 0 (EMPTY)
class Consumer implements Runnable{
  //Constructors
  //holds reference to a given queue
  private Queue<Integer> intQ;
  public Consumer(Queue<Integer> intQ){
    this.intQ = intQ;
  }//end constructor
  
  //run method
  public void run(){
    //Use Sync keyword to ensure individual threads sync with one another.
    synchronized(intQ){
      while(true){
      //check if there are any items in the queue
      if(intQ.isEmpty() == true){
        System.out.println("Consumer: The Queue is empty, consumer waiting");
        //Consumer will wait for an amount of time.
        //try catch block is necessary for wait functions.
        try{
          intQ.wait(1000);
          intQ.notify();
        }//end try
        catch(InterruptedException e){
          //print out the error message if something happens to the thread.
          e.printStackTrace();
        }//end catch
        
      }//end if
      //remove item from the queue
      intQ.remove();
      System.out.println("Consumer: Removing element from queue");
      //notify to allow any thread in waiting to continue, in this case the producer.
        //notify();
      }//end while
    }//end sync
  }//end run
}//end class