import adns
import pandas
from time import time


class AsyncResolver(object):
    def __init__(self, hosts, intensity=100):
        """
        hosts: a list of hosts to resolve
        intensity: how many hosts to resolve at once

        NOTE:
            the list of the hosts must be unique, otherwise the resolver will hang
        """
        self.hosts = hosts
        self.intensity = intensity
        self.adns = adns.init()

    def resolve(self):
        """ Resolves hosts and returns a dictionary of { 'host': 'ip' }. """
        resolved_hosts = {}
        active_queries = {}
        host_queue = self.hosts[:]

        def collect_results():
            for query in self.adns.completed():
                answer = query.check()
                host = active_queries[query]
                del active_queries[query]
                if answer[0] == 0:
                    ip = answer[3][0]
                    resolved_hosts[host] = ip
                elif answer[0] == 101: # CNAME
                    query = self.adns.submit(answer[1], adns.rr.A)
                    active_queries[query] = host
                else:
                    resolved_hosts[host] = None

        def finished_resolving():
            return len(resolved_hosts) == len(self.hosts)

        while not finished_resolving():
            while host_queue and len(active_queries) < self.intensity:
                host = host_queue.pop()
                query = self.adns.submit(host, adns.rr.A)
                active_queries[query] = host
                # print host
            collect_results()

        return resolved_hosts

if __name__ == "__main__":

#
#
#
#

    host_format = "www.host%d.com"
    number_of_hosts = 20000

    hosts = [host_format % i for i in range(number_of_hosts)]

    print( "hosts - {}".format(type(hosts)))
    # exit(1)
    # hosts = ['sunsport.ux.hra.nycnet','sundocentry1.ux.hra.nycnet']

    input_file = r'Data/2domain.csv'

    colnames = ['hostname']
    data = pandas.read_csv(input_file, names=colnames)
    print type(data)
    # buff = pandas.read_csv(input_file,nrows=2,header=None)
    list_data = data.hostname.tolist()

    print type(list_data)
    print list_data

        # print list_data[498:]

    # ar = AsyncResolver(hosts, intensity=500)
    # ar = AsyncResolver(hosts, intensity=50)
    # ar = AsyncResolver(hosts)

    # ar1 = AsyncResolver(list_data)
    # ar1 = AsyncResolver(["www.google.com", "www.reddit.com", "www.nonexistz.net",""])
    # ar1 = AsyncResolver(["www.google.com", "www.reddit.com", "www.nonexistz.net","sunposrep34.ux.hra.nycnet","sunpos1.ux.hra.nycnet"])
    # ar1 = AsyncResolver(["sunposrep34.ux.hra.nycnet", "sunsport.ux.hra.nycnet", "www.google.com","sunpos1.ux.hra.nycnet"])


    start = time()
    # resolved_hosts = ar.resolve()
    end = time()
    print "It took %.2f seconds to resolve %d hosts." % (end - start, number_of_hosts)

    start = time()
    for host, ip in ar1.resolve().items():
        print("Hosts are {}".format(ip,host))
        # if ip is None:
        #     print(' IP - {} - {}'.format(ip,host))
    end = time()
    print "It took %.2f seconds to resolve %d hosts." % (end-start, number_of_hosts)
