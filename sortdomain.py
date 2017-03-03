import operator
import csv
import os.path, sys
from operator import itemgetter
from collections import defaultdict

faultlist_counts = defaultdict(int)

full_file = 'C:\\temp\\domain.csv'
full_file_fault = "C:\\temp\\domain_fault.csv"

with open(full_file,'r') as csvfile:
    domain_reader = csv.reader(csvfile)
    # next(domain_reader)
    # start_time = time.time()
    row_count = 0
    for row in domain_reader:
        row_count += 1
        # if bad_domain(row[2]):
        #     faultlist.append([row[0], row[1], row[2]])
        faultlist_counts[row[0]] += 1
            # print ("{}").format(faultlist_counts[row[2]])
    # print("The total DNS processing time  - {} sec".format(time.time() - start_time))
    # print("The time per dns lookup is  - {} sec".format((time.time() - start_time) / row_count))
# sorted(faultlist,key=lambda :faultlist[0]) #sort by SRC
# start_time = time.time()

# sorted(faultlist, key=itemgetter(0))  # sort by SRC
sorted(faultlist_counts.items(), key=itemgetter(1))  # sort by SRC
# print("Faultlist sorting took - {}".format(time.time() - start_time))

with open(full_file_fault, "wb") as fff:
    fault_writer = csv.writer(fff)
    # for i in faultlist:
    #     fault_writer.writerow(i)
    # fault_writer.writerow("")
    fault_writer.writerow(["Summary of an invalid QUERY"])
    for name, values in faultlist_counts.iteritems():
        # print values, name
        # tmp = [name,values]
        print [name, values]
        # fault_writer.writerow(tmp)
        fault_writer.writerow([name, values])
csvfile.close()
fff.close()
