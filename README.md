# Async-Resolver

It's all about speed resolved 1000 domains using this script and it only took 0m0.204s to resolve.

<a href="https://ibb.co/S3j90XR"><img src="https://i.ibb.co/71f6VJ2/aioresolver.png" alt="aioresolver" border="0"></a>

### How it works?

aioresolver uses python-adns module which provides python binding of asynchronous DNS resolver library. While searching for some good examples to use it I found <a href="https://github.com/pkrumins/adns/blob/master/async_dns.py">async_dns.py</a> shared by <a href="https://twitter.com/pkrumins/">@pkrumins</a> I used it's class AsyncResolver in this tool to quickly resolve domains and also modified it to get the CNAME of the domains.

## Features

- Fast: Resolves domains asynchronously.
- Simple to use: Does not require list of resolvers to work.
- Also Resolves CNAMES and provides option to save the resolved cnames in csv format host,cname.
- Provides raw output in json format.
- Easy to integerate in workflow turn off banner using `-b` flag to pipe **stdout** in other tools.


## Install aioresolver

```bash
> sudo apt-get install python-adns ( for python3 you can use https://github.com/trolldbois/python3-adns I haven't tried this)
> sudo pip install json
> git clone https://github.com/tauh33dkhan/aioresolver.git
> cd aioresolver
```



# Usage


| Flag       | Description                                                | Example                              |
|------------|------------------------------------------------------------|--------------------------------------|
| -f         | File with domain names to resolve                         | aioresolver -f tesla.com   |
| -o | Use this option to save resolved domains to a file                  | aioresolver -f tesla.txt -o alive.txt          |
| -c         | Use this option to resolve CNAME, returns resolved domains in Host,CNAME format                  |  aioresolver -f tesla.txt -c     |
| -cO        | Use this option to resolve CNAME and save result in a csv file                                | aioresolver -f tesla.txt -cO cname.csv                       |
| -r         | Save raw output in a json file(raw.json)                   | aioresolver -f tesla.txt -r         |
| -i    | Intensity - Number of domains to resolves at once, Default=100                          | aioresolver -f tesla.txt -i 500        |
| -d    |   | async-resolver -d example.com -w wordlist.txt
| -w    | Wordlist to use for bruteforcing    | async-resolver -d example.com -w wordlist.txt    |
| -b   | Use this option to turn off banner                                       | aioresolver -f tesla.txt -b  |


#### 1. Resolving Domains
```bash
> aioresolver.py -f tesla.txt   
```
This will resolve all the domains in tesla.txt file and returns all the live or resolved domains, use <b>-o</b> option to save them in a file

#### 2. Resolving CNAMES
```bash
> aioresolver.py -f tesla.txt -c
```

This will resolve all the domains in tesla.txt file and returns CNAME of all the live domains in <b>csv</b> format Host,CNAME, use -cO option to save them in a file

#### 3. Raw output 
```bash
> aioresolver.py -f tesla.txt -r
```
This will resolve all the domains in tesla.txt and saves the raw result in the raw.json file in following format 
```json
{"host":["ip","CNAME"],"host":["None","None"]}
```
if a domain is not resolved then you will see None in the value

#### 4. Bruteforce

Async-Resolver provides bruteforcing options to find new domains

```bash
> async-resolver -d example.com -w wordlist.txt
```

#### 5. Turn off Banner

```bash
> async-resolver -f tesla.txt -b | httprobe
```

This will turn off the banner so you can pipe resolved domains to other tools like httprobe

## Note: 
Make sure to remove duplicate entries from your file before using this tool other wise it will hang for forever.

## Contact Me

<a href=https://twitter.com/tauh33dkhan/ target="_blank">@tauh33dkhan</a>


## Thanks
<a href="https://twitter.com/pkrumins/">@pkrumins</a> for sharing AsyncResolver class
