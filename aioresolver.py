#!/usr/bin/python3
# aioresolver
#
# https://github.com/tauh33dkhan/aioresolver.git
# Contact me on twitter @tauh33dkhan

import adns
import sys
import argparse
import json
import cProfile
from collections import deque

def print_banner(silent):
    if not silent:
        print("""\033[32m
       _                           _
      (_)                         | |
  __ _ _  ___  _ __ ___  ___  ___ | |_   _____ _ __
 / _` | |/ _ \| '__/ _ \/ __|/ _ \| \ \ / / _ \ '__|
| (_| | | (_) | | |  __/\__ \ (_) | |\ V /  __/ |
 \__,_|_|\___/|_|  \___||___/\___/|_| \_/ \___|_|

     github.com/tauh33dkhan/aioresolver | \033[31mv2.0

\033[0m""")

version = "v2.0"

def parser_error(errmsg):
    print("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    print("Error: " + errmsg)
    sys.exit()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", dest="file", help="File with list of hosts to resolve", metavar="<input_file>")
    parser.add_argument("-d", dest="domain", help="Domain to bruteforce", default=False, metavar="<domain>")
    parser.add_argument("-w", dest="wordlist", help="Wordlist to use for subdomain bruteforcing", metavar="<wordlist>")
    parser.add_argument("-c", dest="cname", help="Resolve CNAME (dedicated arg)", action="store_true", default=False)
    parser.add_argument("-query", dest="query", help="Query record [A, CNAME, TXT, MX, SOA, NS and PTR]", default="A")
    parser.add_argument("-t", dest="track", help="Filter hosts that resolves to same IP address", action="store_true")
    parser.add_argument("-o", "--outfile", help="File to save output", default=False, metavar="<file_name>")    
    parser.add_argument("-resp", dest="resp", help="Use this option to show response",  default=False, action="store_true")    
    parser.add_argument("-r", dest="resolvers", help="Text file containing DNS resolvers", default=False)
    parser.add_argument("-i", "--intensity", help="Number of domains to resolves at once, (Default=100)", default=100, metavar="<intensity>", type=int)
    parser.add_argument("-s", "--silent", help="Use this option to turn off banner", action="store_true")
    parser.add_argument("--version", help="Show version", action="store_true")
    parser.error = parser_error
    if len(sys.argv) < 2:
       silent = False
       print_banner(silent)
       parser.print_usage()
       sys.exit()
    return parser.parse_args()

class AioResolver(object):
    def __init__(self, file_name=None, wordlist=None, query_record="A", resolve_cname=None, intensity=100, out_file=None, domain=None, track=None, resp=None, resolverlist=None, silent=None):                    
        self.file_name = file_name
        self.silent = silent
        self.wordlist = wordlist
        self.resolve_cname = resolve_cname
        self.intensity = intensity
        self.out_file = out_file
        self.domain = domain
        self.track = track
        self.query_record = query_record
        self.resp = resp
        self.intensity = intensity
        self.query_record = query_record
        self.resolved_hosts = 0
        self.resolverlist = resolverlist
        if self.resolverlist:
            resolver = ""
            with open(self.resolverlist, "r") as wl:
               for line in wl:
                    resolver += "nameserver "+line
               self.adns = adns.init(configtext=resolver)
        else:
            self.adns = adns.init()
        if self.track:
            self.trackingdict = {} 
        
    def resolve(self):
        try:
            with open(self.file_name, 'r') as f:
                if self.query_record == "PTR":
                    self.hosts = self.convert_cidr([line.strip() for line in f])
                    self.lenhosts = len(self.hosts)
                else:
                    self.hosts = [line.strip() for line in f]
                    self.lenhosts = len(self.hosts)
        except Exception as e:    
            print(str(e))
            exit()
        self.resolverEngine()

    def bruteforce(self):
        try:
            with open(self.wordlist, 'r') as wl:
                self.hosts = [line.strip() + "." + self.domain for line in wl]
                self.lenhosts = len(self.hosts)
        except Exception as e:    
            print(str(e))
            exit()
        self.resolverEngine()          

    def removeDupe(self, dlist):
        return list(dict.fromkeys(dlist))
    
    def convert_cidr(self, cidrlist):
        import ipaddress
        print("> Only supports IPv4 cidr")
        iplist = []
        for cidr in cidrlist:
            for ip in ipaddress.IPv4Network(cidr, strict=False):
                iplist.append(str(ip))
        return(iplist)

    def resolverEngine(self):        
        active_queries = {}
        host_queue = deque(self.hosts[:])
        query_record = getattr(adns.rr, self.query_record)
        if self.resp:
            result = {}
            txtrecords = []
            

        def collect_results():
            for query in self.adns.completed():
                answer = query.check()
                host = active_queries[query]
                del active_queries[query]
                if answer[0] == 0:
                    if query_record == 1 or query_record == 5: 
                        self.resolved_hosts += 1
                        if query_record == 1:
                            ips = answer[3]
                            if ips[0] is None:
                                not_alive_host = host # Returns Not Alive hosts do whatever you want to do with it.
                            else:
                                if self.track:
                                    ips = answer[3]
                                    for ip in ips:
                                        if ip in self.trackingdict:
                                            self.trackingdict[ip].append(host)
                                        else:
                                            self.trackingdict[ip] = [host]
                                elif self.resp:
                                    print("{},{}".format(host, ",".join(ips)))
                                    if self.out_file:
                                        out_file.write("{},{}\n".format(host, ip)) 
                                else:
                                    print(host)
                                    if self.out_file:
                                        out_file.write("{}\n".format(host))
                        
                        if query_record == 5:
                            cname = answer[3][0].decode('UTF-8')                                                              
                            if cname is None:
                                not_alive_host = host # Returns Not Alive hosts do whatever you want to do with it.
                            else:
                                if self.resp:
                                    print("{},{}".format(host, cname))
                                    if self.out_file:                                    
                                        out_file.write("{},{}\n".format(host, cname))                                
                                else:
                                    print("{}".format(host))
                                    if self.out_file:                                    
                                        out_file.write("{}\n".format(host))                                      
                    else:
                        record = answer[3]
                        self.resolved_hosts +=1                                    

                        if query_record == 16: # TXT record
                            answer = record
                            if answer[0] != None and type(answer[0]) is tuple:
                                if not self.resp:
                                    print(host)
                                    if self.out_file:
                                        out_file.write(host+"\n")
                                else:                                    
                                    for i in answer:                    
                                        txtrecords.append(i[0].decode('UTF-8'))
                                    result[host] = txtrecords
                        
                        if query_record == 16842767: # MX Record
                            answer = record
                            if answer[0] != None and type(answer[0]) is tuple:
                                if not self.resp:
                                    print(host)
                                    if self.out_file:
                                        out_file.write(host+"\n")
                                else:
                                    mxrecords = []
                                    for i in answer:
                                        mxrecords.append("{} {}".format(i[0], i[1][0]))
                                    result[host] = mxrecords
                        
                        if query_record == 16842754: # NS Record
                                answer = record
                                if answer[0] != None and type(answer[0]) is tuple:
                                    if not self.resp:
                                        print(host)
                                        if self.out_file:
                                            out_file.write(host+"\n")
                                    else:
                                        nsrecords = []
                                        for i in answer:
                                            nsrecords.append(i[0])
                                        result[host] = nsrecords

                        if query_record == 131078: # SOA record
                            answer = record
                            if answer[0] != None and type(answer[0]) is tuple:
                                if not self.resp:
                                    print(host)
                                    if self.out_file:
                                        out_file.write(host+"\n")
                                else:
                                    soarecords = {}
                                    for i in answer:
                                        soarecords['MNAME'] = i[0]
                                        soarecords['RNAME'] = i[1]
                                    result[host] = soarecords

                        if query_record == 16842764: # PTR record
                                answer = record[0]
                                if answer != None:
                                    answer = answer.decode('UTF-8')
                                    if not self.resp:
                                        print(host)
                                        if self.out_file:
                                            out_file.write("{}".format(host)) 
                                    else:
                                        print("{},{}".format(host,answer))
                                        if self.out_file:
                                            out_file.write("{},{}\n".format(host,answer))                                            

                        
                elif answer[0] == 101 and answer[1] != None: # CNAME                    
                    query = self.adns.submit(answer[1], query_record)
                    active_queries[query] = host
                else:
                    self.resolved_hosts += 1

        while not self.resolved_hosts == self.lenhosts:
            while host_queue and len(active_queries) < self.intensity:
                host = host_queue.pop()
                if self.query_record == "PTR":
                    query = self.adns.submit_reverse(host, query_record)
                else:
                    query = self.adns.submit(host, query_record)
                active_queries[query] = host
            collect_results()

        if self.resp and query_record != 16842764 and query_record > 5:
            print(json.dumps(result, indent=2))
            if self.out_file:
                out_file.write(json.dumps(result, indent=2))
                print("\n[+] Saved response in \"{}\" file".format(args.outfile))
        
        if self.track:
            print(self.trackingdict)
            print(json.dumps(self.trackingdict, indent=4))
            if self.out_file:
                print("[+] Output will be saved in \"{}\" file".format(args.outfile))
                out_file.write(json.dumps(self.trackingdict, indent=4))

if __name__ == "__main__":
    args = parse_arguments()
    file_name = args.file
    silent = args.silent
    wordlist = args.wordlist
    resolve_cname = args.cname
    intensity = args.intensity
    out_file = args.outfile
    domain = args.domain
    track = args.track
    query_record = args.query
    resp = args.resp
    resolverlist = args.resolvers

    if not silent:
        print_banner(silent)

    if out_file:
        out_file = open(out_file,'a')
    
    if resolve_cname:
        query_record = "CNAME"

    aior = AioResolver(file_name, wordlist, query_record, resolve_cname, intensity, out_file, domain, track, resp, resolverlist)

    if file_name:
        aior.resolve()

    if domain:
         aior.bruteforce()
         exit()

    if args.version:
        print("Version: %s" % version)
