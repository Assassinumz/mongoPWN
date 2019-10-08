#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
#                           MongoPWN
#         A simple script to find open mongoDB instances 
#                 on the internet using shodan
#                         
#                      by: Assassin umz


import os, platform, requests, time
import argparse, shodan, threading
from pymongo import MongoClient
from colorama import init, Fore, Style

init(convert=True)
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
end = Style.RESET_ALL
open_instances = 0

start = time.perf_counter()

parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--input', help="Hosts IPs file path, must be in seperate lines")
group.add_argument('-s', '--shodan', help="Get a list of hosts from shodan, provide the API key")

parser.add_argument('-o', '--output', help='Output open Hosts IPs to a file')
args = parser.parse_args()


try:
    requests.get('https://google.com')
    pass
except:
    print(f"{red}[-]{end} Network Issue, make sure your network connection is working and retry")
    exit(0)


def cls():
    if platform.system().lower() == "windows":
        return os.system('cls')
    else:
        return os.system('clear')


def banner():
    cls()

    print('''
 {0}   |{1}                                       ______ _    _ _   _ 
 {0} .'|'.{1}                                     | ___ \ |  | | \ | |
 {0}/.'|\ \{1}   _ __ ___   ___  _ __   __ _  ___ | |_/ / |  | |  \| |
 {0}| /|'.|{1}  | '_ ` _ \ / _ \| '_ \ / _` |/ _ \|  __/| |/\| | . ` |
 {0} \ |\/{1}   | | | | | | (_) | | | | (_| | (_) | |   \  /\  / |\  |
 {0}  \|/{1}    |_| |_| |_|\___/|_| |_|\__, |\___/\_|    \/  \/\_| \_/
 {0}   `{1}                             __/ |
                                 |___/                        
                
                {0}By: Assassinumz{1}
'''.format(green, end))


def Check(ip):
    global open_instances
    client = MongoClient(str(ip), socketTimeoutMS=1000, serverSelectionTimeoutMS=1000)
    #if client is None:
    #    return

    try:
        dbs = client.list_database_names()

        print(f"{green}[+]{end} {ip}\r")

        if args.output != None:
            with open(args.output, 'a') as f:
                f.write(f"{ip}\n")
 
        open_instances+=1                

    except Exception:
        pass


def InputFile(file):
    

    if not os.path.isfile(file):
        print(f"{red}[-]{end} File Does not exist")
        exit(0)

    print(f"{yellow}[=]{end} Reading hosts from {args.input}\n")
    
    with open(file, 'r') as f:
        lines = f.readlines()
    
    return lines
    

def Shodan():

    print(f"{yellow}[=]{end} Getting MongoDB Hosts from shodan\n")

    api = shodan.Shodan(args.shodan)
    lines = []
    results = api.search("MongoDB", limit=1000)

    for result in results['matches']:
        ip = result['ip_str']
        lines.append(ip)
    
    return lines

def main():
    banner()

    if args.input != None:
        lines = InputFile(args.input)

    elif args.shodan != None:
        lines = Shodan()

    else:
        exit(0)
    threads = []
    #TODO: Add Counter
    print(f"{yellow}[=]{end} Scanning {len(lines)} hosts\n")

    for line in lines:
        ip = line.strip('\n')
        t = threading.Thread(target=Check, args=[ip])
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()

    print(f"{green}[+]{end} Found {open_instances} open hosts out of {len(lines)}")
    print("Thank You")


#TODO: Add masscan

if __name__ == "__main__":
    main()
    end = time.perf_counter()
    print(f"Finished in {round(end-start, 3)} seconds")