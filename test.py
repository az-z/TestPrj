__author__ = 'Andrew Zyman(AZ)'
import argparse
import csv
import argparse
import pandas
import AsyncResolver as asynr
from time import time



# TODO: 1 spread file into # of parts
#  open a file
# read wc -l
# num_lines/CPU_COUNT
# create a range for each process
input_file = r'Data/2domain.csv'
# input_file = r'Data/2domain.csv'

colnames = ['hostname']
data = pandas.read_csv(input_file, names=colnames,header=0)
buff = pandas.read_csv(input_file,nrows=2,header=None)
list_data = data.hostname.tolist()
# list_data = data[colnames].get_values()
# list_data = data['hostname'].tolist()

list_data = data[colnames[0]].get_values()


# list_data = data[0]
print list_data
#
# exit(1)

# print len(list_data)
# sorted(list_data)
list_data = list(set(list_data))
print len(list_data)

# exit(1)

# buff = pandas.read_csv(input_file,header=None)
# buff = pandas.read_csv(input_file,index_col=False)

# print buff
# print list_data

ar = asynr.AsyncResolver(list_data,intensity=500)

start = time()

for host, ip in ar.resolve().items():
    if ip is None:
        print(' IP - {} - {}'.format(ip, host))

end = time()
print "It took %.2f seconds ." % (end - start)


#
# buff = pandas.read_csv(input_file,skiprows=2,header=None)
# print buff





#
# full_file_fault = r'C:\Temp\test.csv'
# faultlist = (['SRC', 'DST','QUERY'])
#
# with open(full_file_fault, 'wb') as fff:
#     fault_writer = csv.writer(fff)
#     for i in xrange(1,5):
#         fault_writer.writerow(['1','2', '3'])
# #
# #
# # parser = argparse.ArgumentParser(description='Validates the \'Query\' column for each IP in \'SRC \' column')
# # parser.add_argument('-i','--input',help='Input CSV file with IPs to examine',required=True,dest='input')
# # parser.add_argument('-o','--output',help='Output CSV file ',required=True,dest='output')
# # args = parser.parse_args()
# #
# # print ("input -  {}".format(args.input))
# # print ("output -  {}".format(args.output))
#
# from collections import defaultdict
#
# faultlist_counts = defaultdict(int)
# faultlist_counts['A'] = 0
# faultlist_counts['B'] = 1
# faultlist_counts['B'] += 1
#
# print ("{}").format(str(faultlist_counts))
# print ("{}").format(faultlist_counts)
#
# with open(full_file_fault, 'wb') as fff:
#     fault_writer = csv.writer(fff)
#     for i in xrange(1,5):
#         fault_writer.writerow(['1', '2', '3'])
#
#     for name, values in faultlist_counts.iteritems():
#         print values, name
#         tmp = [name,values]
#         print tmp
#         fault_writer.writerow(tmp)