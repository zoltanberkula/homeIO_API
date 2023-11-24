import threading
import time
from typing import Any

'''
This function will print 5 lines in a loop and sleeps for 1 second after
printing a line.
'''
def threadFunc():
    for i in range(5):
        print('Hello from new Thread ')
        time.sleep(1)


def clientLoopTHRD():
    counter: int = 0
    while counter < 99:
        counter = counter + 1
        print("Running Client stuff!")
    clientCNTR = 0



def checkMainTHRD(inspectorVAR: Any, threshold: Any, identifier: str):
    while inspectorVAR < threshold:
        inspectorVAR = inspectorVAR + 1
        print(f"inspectorVar: {inspectorVAR} under threshold {threshold} id:{identifier}")
    return True
    

def main():
    tobeInspected: int = 0
    threshold = 672
    tobeInspected2: int = 0
    threshold2 = 1344
    print('**** Create a Thread with a function without any arguments ****')

    # Create a Thread with a function without any arguments
    th = threading.Thread(target=checkMainTHRD, args=(tobeInspected, threshold, "thread1 running"))
    th2 = threading.Thread(target=checkMainTHRD, args=(tobeInspected2, threshold2, "thread2 running"))

    # Start the thread
    th.start()
    th2.start()

    # Print some messages on console
    for i in range(4):
       print('Hi from Main Thread')
       #time.sleep(0.5)
       threshold = threshold + 1

    # Wait for thread to finish
    th.join()

if __name__ == '__main__':
   main()