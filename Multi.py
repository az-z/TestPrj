# from multiprocessing import Process, Queue
import  multiprocessing as mp
import random
import time

import pandas
import adns

def rand_num(queue):
    num = random.random()
    print(num)
    time.sleep(5.0)
    print("done sleeping")
    queue.put(num)

# TODO: 1 spread file into # of parts
#  open a file
# read wc -l
#       now lets estimate number of records
#       get file size in bytes
#       read first 1K records, calculate aver size of a record in bytes
#       get the approximate size of the file in the records

# num_lines/CPU_COUNT
# create a range for each process
input_file = r'data/input.cvs'

buff = pandas.read_csv(input_file,nrows=2)

print buff

# TODO: 1a Get rid of dups in each chank of the file. Due to bug in the adns module
# TODO: 2  Glue per process return values into one result set
# TODO: 3  write the result set into a file.



if __name__ == "__main__":
    queue = mp.Queue()

    cpu_num = mp.cpu_count()
    print("CPU count - {} ".format(cpu_num))
    # processes = [multiprocessing.Process(target=rand_num, args=cpu_num)]
    processes = [mp.Process(target=rand_num, args=(queue,)) for x in range(cpu_num)]

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    result = 0
    for p in processes:
        result += queue.get()
    print result