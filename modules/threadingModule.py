import threading
import time
from typing import Any

def checkMainTHRD(inspectorVAR: Any, threshold: Any, identifier: str):
    while inspectorVAR < threshold:
        inspectorVAR = inspectorVAR + 1
        print(f"inspectorVar: {inspectorVAR} under threshold {threshold} id:{identifier}")
    return True
    

def main():
    tobeInspected: int = 0
    threshold = 112
    tobeInspected2: int = 0
    threshold2 = 224
    tobeInspected3: int = 0
    threshold3 = 336

    th = threading.Thread(target=checkMainTHRD, args=(tobeInspected, threshold, "thread1 running"))
    th2 = threading.Thread(target=checkMainTHRD, args=(tobeInspected2, threshold2, "thread2 running"))
    th3 = threading.Thread(target=checkMainTHRD, args=(tobeInspected3, threshold3, "thread3 running"))

    # Start the thread
    th.start()
    th2.start()
    th3.start()

    # Print some messages on console
    for i in range(4):
       print('Hi from Main Thread')
       #time.sleep(0.5)
       #threshold = threshold + 1

    # Wait for thread to finish
    th.join()

if __name__ == '__main__':
   main()