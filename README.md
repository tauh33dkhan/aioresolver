# AioResolver
[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)
[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/tauh33dkhan/aioresolver/issues)
[![version](https://img.shields.io/badge/version-v2.0-blue.svg?style=flat)](https://github.com/tauh33dkhan/aioresolver)

aioresolver is a fast DNS resolver tool it is capable of resolving over one thousand domain names in 0.2 seconds with accuracy targeting those who seek to resolve a lot of domain names. aioresolver uses python-adns module which provides Python binding of <a href="https://www.gnu.org/software/adns/">adns</a> that let's you perform DNS queries of your choice.

### Features

- Fast: Resolves domain names asynchronously.
- Bruteforce option to find new subdomains.
- Provides option to filter hosts that resolves to same IP address.
- Provides option to use custom DNS resolvers (Default: `/etc/resolv.conf`)
- Supports A, CNAME, MX, TXT, SOA, NS and PTR query
- Easy to integerate in workflow turn off banner using `-s` flag to pipe **stdout** in other tools.


<a href="https://ibb.co/S3j90XR"><img src="https://i.ibb.co/71f6VJ2/aioresolver.png" alt="aioresolver" border="0"></a>


### Prerequisite

aioresolver requires python-adns module if you are still using python-2.7 you can install it using package manager.

```bash
> apt-get install python-adns
```
### For python3

There is python3 port for adns is available to install it follow the steps given below or use the docs available here https://www.freshports.org/dns/py-adns/:

1. First download and install current release of adns_libraries.
```
sudo apt-get install libadns1-dev
wget http://www.chiark.greenend.org.uk/~ian/adns/adns.tar.gz
tar -xvf adns.tar.gz
cd adns-1.5.0/
./configure
make
sudo make install
```
2. Download and install python3 port of adns
```
git clone --depth 1 https://github.com/trolldbois/python3-adns.git
cd python3-adns
sudo python3 setup.py install
```

### Install aioresolver
```
sudo pip3 install json
git clone https://github.com/tauh33dkhan/aioresolver.git
cd aioresolver
```


### Usage


| Flag       | Description                                                | Example                              |
|------------|------------------------------------------------------------|--------------------------------------|
| -f         | File with list of hosts to resolve                         | aioresolver -f tesla.com   |
| -o | Use this option to save output to a file                  | aioresolver -f tesla.txt -o alive.txt          |
| -d         | Domain to bruteforce                  |  aioresolver -d example.com -w wordlist.txt     |
| -w        | Wordlist to use for subdomain bruteforcing                                | aioresolver -d example.com -w                      |
| -c       | Resolve CNAME (dedicated arg for CNAME)                                                | aioresolver -f tesla.txt -c                           |
| -resp       | Use this options to show response                                      | aioresolver -f tesla.txt -c -resp                              |
| -query       | Query record [A, CNAME, TXT, MX, SOA,NS and PTR                                                | aioresolver -f tesla.txt -query MX                            |
| -t       | Filter hosts that resolves to same IP                                               | aioresolver -f tesla.txt -t                              |
| -i    | Intensity - Number of domain names to resolves at once, Default=100                          | aioresolver -f tesla.txt -i 500        |
| -r    | Text file containing list of DNS resolvers | aioresolver -f tesla.txt -r resolvers.txt|
| -s   | Use this option to turn off banner                                       | aioresolver -f tesla.txt -s  |
| --version       | Show version                                                | aioresolver --version                              |


#### 1. Resolving Domains

```bash
> aioresolver.py -f tesla.txt   
```
This will resolve domains names in tesla.txt file and returns all the live domains, use <b>-resp</b> options to print `A` record and <b>-o</b> option to save output in a file.


#### 2. Query CNAME

```bash
> aioresolver.py -f tesla.txt -c -resp
```
This will extract CNAME record of all the domain names in tesla.txt file, use <b>-o</b> option to save output in a file.

#### 3. Query TXT/MX/NS/SOA record
```bash
> aioresolver.py -f tesla.txt -query MX -resp
```
This will extract MX record of all the domain names in tesla.txt file, output is given in json format which you can read using jq.
```json
{"host1":["ANSWER1","ANSWER2"],"host2":["ANSWER1","ANSWER2", "ANSWER3"]}
```
#### 4. Bruteforce

aioresolver provides bruteforce option to find new subdomains.

```bash
> aioresolver -d example.com -w wordlist.txt
```

#### 5. PTR query

aioresolver can be used to extract hostnames from given range using PTR query.
```bash
> aioresolver -f rangefile.txt -resp
```

#### 6. Using custom list of resolver

aioreoslver can be used with custom list of resolvers by using `-r` flag, by default aioresolver uses resolvers in `/etc/resolv.conf` file.
```bash
> cat resolvers.txt
8.8.8.8
1.1.1.1
9.9.9.9
> aioresolver -f tesla.txt -r resolvers.txt
```

#### 6. Turn off Banner

```bash
> aioresolver -f tesla.txt -s | httprobe
```

This will turn off the banner so you can pipe resolved domain names to other tools like httprobe


### Contact Me

<a href="https://twitter.com/tauh33dkhan/">@tauh33dkhan</a> 

### Credits and Thanks
<a href="https://twitter.com/pkrumins/">@pkrumins</a> for sharing <a href="https://github.com/pkrumins/adns/blob/master/async_dns.py">async_dns.py</a> library which inspired and helped me to create this tool.
