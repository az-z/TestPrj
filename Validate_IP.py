#!/bin/python
__author__ = 'Andrew Zyman @SailTech LLC'
import subprocess
import argparse
import os.path, sys
from collections import defaultdict
from time import time
import pandas
import AsyncResolver as asynr
from numpy import NaN

# , ntpath
from operator import itemgetter

def bad_domain(domain):
    """ function validates the 'domain' and returns 1 if the arg is incorrect/invalid"""
    # print (domain)
    if domain[0:1] == '-':
        print ("Invalid  domain query - {}".format(domain))
        return 1
    out_bytes = subprocess.check_output(["nslookup", domain], stderr=subprocess.STDOUT)

    if ('Non-existent domain' in out_bytes) or ('Server failed' in out_bytes):
        # print ('Invalid domain - {}'.format(domain))
        return 1
        # print("DOMAIN DOESN\'T EXIST -  {}" .format(domain))

def main():

    # Open a file
    # Read 3 values in loop
    parser = argparse.ArgumentParser(description='Validates the \'Query\' column for each IP in \'SRC \' column ')
    # parser = argparse.ArgumentParser(description='\t the format of the input file should be :')
    # parser = argparse.ArgumentParser(description='SRC - source IP column')
    # parser = argparse.ArgumentParser(description='DST - DNS server')
    # parser = argparse.ArgumentParser(description='QUERY - the query(hostname) issued by SRC IP')
    parser.add_argument('-i','--input',help='Input CSV file with IPs to examine',required=True,dest='input')
    parser.add_argument('-o','--output',help='Output CSV file ',required=True,dest='output')
    args = parser.parse_args()
    # in_file = r'C:\Temp\1.csv'
    in_file = args.input
    out_file = args.output
    path_out_file, _ = os.path.split(out_file)

    if not os.access(in_file, os.R_OK) or  not os.path.isfile(in_file) or not os.access(path_out_file,os.W_OK):
       print("Unable to access/read files - {} {}".format(in_file, path_out_file))
       sys.exit(1)

    colnames = ['QUERY']
    data = pandas.read_csv(in_file, names=colnames,header=0)
    data[colnames] = data[colnames].astype('str')

    query_list = data[colnames[0]].tolist()
    query_uniq_list = list(set(query_list))

    # TODO : count the existing queries so i can preserve the counts
    query_count = defaultdict(int)
    for query in query_list:
        query_count[query] += 1

    query_count,itemgetter(2)
    query_list_count = len(query_list)
    print("Total number of requests is {}".format(query_list_count))
    print("Number of unique requests is {}".format(len(query_count.keys())))

    out_list = []
    for host, host_cnt in query_count.items():
        # print ("host - {}, host_cnt - {}".format(host,host_cnt))
        out_list.extend([[host,host_cnt,round(host_cnt/(1.0*query_list_count),ndigits=5)*100]])

    #Validate QUERY
    # for i in query_uniq_list,

    ar = asynr.AsyncResolver(query_uniq_list, intensity=500)
    start = time()

    # TODO : convert to dict {inner[0]: inner[1:] for inner in outer}


    for host, ip in ar.resolve().items():
        if ip is None:
            [x.append('None') for x in out_list if x[0]==host]
    end = time()
    print "It took %.2f seconds to process unique requests." % (end - start)

    out_df = pandas.DataFrame(out_list,columns=None,)
    out_df.replace(NaN,0,inplace=True)
    out_df.to_csv(out_file,index=None,header=False,)

    # with open(in_file, 'r') as csvfile:
    #     domain_reader = csv.reader(csvfile)
    #     next(domain_reader)
    #     start_time = time.time()
    #     row_count = 0
    #     for row in domain_reader:
    #         row_count += 1
    #         if bad_domain(row[2]):
    #             out_list.append([row[0], row[1], row[2]])
    #             fault_dict[row[2]] += 1
    #             # print ("{}").format(fault_dict[row[2]])
    #     print("The total DNS processing time  - {} sec".format(time.time() - start_time))
    #     print("The time per dns lookup is  - {} sec".format((time.time() - start_time)/row_count))
    #
    # sorted(out_list,key=lambda :out_list[0]) #sort by SRC

    # start_time = time.time()
    # sorted(out_list,key=itemgetter(0)) #sort by SRC
    # print("Faultlist sorting took - {}".format(time.time() - start_time))
    #
    # Write the file
    # with open(out_file, 'wb') as fff:
    #     fault_writer = csv.writer(fff)
    #     for i in out_list:
    #         fault_writer.writerow(i)
    #     fault_writer.writerow("")
    #     fault_writer.writerow(["Summary of an invalid QUERY"])
    #
    #     for name, values in fault_dict.iteritems():
    #         # print values, name
    #         # tmp = [name,values]
    #         print [name,values]
    #         # fault_writer.writerow(tmp)
    #         fault_writer.writerow([name,values])
    #
    # data.close()
    # fff.close()

if __name__ == '__main__':
    main()
