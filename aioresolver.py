#!/usr/bin/python3
#
# aioresolver
#
# https://github.com/tauh33dkhan/asyn-resolver.git
#
# Contact me on twitter @tau33dkhan
#

import adns
import sys
import argparse
import json


version = "v1.2"

def Banner():
    if banner:
        print("""\033[32m
       _                           _
      (_)                         | |
  __ _ _  ___  _ __ ___  ___  ___ | |_   _____ _ __
 / _` | |/ _ \| '__/ _ \/ __|/ _ \| \ \ / / _ \ '__|
| (_| | | (_) | | |  __/\__ \ (_) | |\ V /  __/ |
 \__,_|_|\___/|_|  \___||___/\___/|_| \_/ \___|_|\033[0m
						 \033[31mv1.2

\033[0m""")


def resolve():
    try:
        with open(file_name, 'r') as f:
            myNames = [line.strip() for line in f]
    except IOError:
        Banner()
        print("[!] File \"{}\" does not exist".format(file_name))
        exit()
    Banner()
    ar = AsyncResolver(myNames, intensity)
    resolved = ar.resolve()
    output(resolved)


def bruteforce():
    try:
        with open(wordlist, 'r') as wl:
            w = ["%s.%s" % (line.strip(),domain) for line in wl]
    except IOError:
        exit("[!] Unable to read wordlist file: \"{}\"".format(w))
    ar = AsyncResolver(w, intensity)
    resolved = ar.resolve()
    output(resolved)


def output(resolved):
    if print_raw:
        json_file = open("raw.json", 'w')
        r = json.dumps(resolved)
        json_file.write(str(r))  # Saving resolved/not resolved hosts in json format to raw.txt file
        print("[+] Saved resolved/not resolved hosts in json format to raw.txt file\n")

    if do_out:
        print("[+] Saving resolved hosts in \"{}\" file".format(args.output))
        wofile = out_file.write

    if cname_output:
        print("[+] Saving resolved CNAMES in \"{}\" file".format(args.output_cname))
        wcnamefile = cname_ofile.write

    for i in resolved.items():
        host = i[0]
        ip, cname = i[1]
        if ip is None:
            not_alive_host = host  # Returns Not Alive hosts do whatever you want to do with it
        else:
            if do_out:
                wofile(host+"\n")
            elif resolve_cname or cname_output:
                if cname_output:
                    wcnamefile("%s,%s\n" % (host, cname))
                else:
                    print("%s,%s" % (host, cname))
            else:
                print(host)


#####################################################################
#  Following Class is taken from async_dns.py coded by Peter Krumins
#
#  I modified Some part of it to also get CNAME
######################################################################
# Created by Peter Krumins (peter@catonmat.net, @pkrumins on twitter)
# www.catonmat.net -- good coders code, great coders reuse
#
# Asynchronous DNS Resolution in Python.
#
# Read more about how this code works in my post:
# www.catonmat.net/blog/asynchronous-dns-resolution


class AsyncResolver(object):
    def __init__(self, hosts, intensity=100):
        """intensity: how many hosts to resolve at once"""
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
                    cname = answer[1]
                    resolved_hosts[host] = [ip, cname]
                elif answer[0] == 101:  # CNAME
                    query = self.adns.submit(answer[1], adns.rr.A)
                    active_queries[query] = host
                else:
                    resolved_hosts[host] = [None, None]

        def finished_resolving():
            return len(resolved_hosts) == len(self.hosts)

        while not finished_resolving():
            while host_queue and len(active_queries) < self.intensity:
                host = host_queue.pop()
                query = self.adns.submit(host, adns.rr.A)
                active_queries[query] = host
            collect_results()

        return resolved_hosts

# AsyncResolver class ends here


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="file with domain names to resolve")
    parser.add_argument("-o", "--output")
    parser.add_argument(
        "-c", "--cname", help="Resolve CNAME", action="store_true")
    parser.add_argument("-cO", "--output-cname")
    parser.add_argument(
        "-r", "--raw", help="Save resolved/not-resolved domains in a raw.json file", action="store_true")
    parser.add_argument(
        "-i", "--intensity", help="Number of domains to resolves at once, Default=100")
    parser.add_argument(
        "-s", "--silent", help="Use this option to turn off banner", action="store_true")
    parser.add_argument("-d", "--domain")
    parser.add_argument("-w", "--wordlist",
                        help="Wordlist to use for bruteforcing")
    parser.add_argument("-v", "--version", help="Show version", action="store_true")
    args = parser.parse_args()

    file_name = args.file
    silent = args.silent
    wordlist = args.wordlist

    if args.cname:
        resolve_cname = True
    else:
        resolve_cname = False

    if args.output_cname:
        cname_output = True
        cname_ofile = open(args.output_cname, "w")
    else:
        cname_output = False

    if args.intensity:
        intensity = int(args.intensity)
    else:
        intensity = 100

    if args.silent:
        banner = False
    else:
        banner = True

    if args.output:
        out_file = open(args.output, 'a')
        do_out = True
    else:
        do_out = False

    if args.raw:
        print_raw = True
    else:
        print_raw = False

    if args.domain:
        wordlist = args.wordlist
        domain = args.domain
        Banner()
        bruteforce()
        exit()

    if args.version:
       print("Version: %s" % version)
       exit()

    if args.file:
        resolve()
    else:
        Banner()
        print("[!] Please provide a file with domain names to resolve\n")
        print("[-] Use -h to see help")

    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    if args.version:
       print(version)
