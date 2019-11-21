#!/usr/bin/env python
#-*- coding: utf-8 -*-
#
#
#                           MongoPWN
#         A simple script to find open mongoDB instances 
#                 on the internet using shodan
#                         
#                      by: Assassin umz


import os, platform, requests
import argparse, shodan
from pymongo import MongoClient
from colorama import init, Fore, Style


init(convert=True)
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
end = Style.RESET_ALL
open_instances = 0


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--input', help="Hosts IPs file path, must be in seperate lines")
group.add_argument('-s', '--shodan', help="Get a list of hosts from shodan, provide the API key")
group.add_argument('-m', '--masscan', help="Get a list of hosts from masscan, provide the speed at which the scan takes place (example: 1000000)")

parser.add_argument('-o', '--output', help='Output open Hosts IPs to a file')
args = parser.parse_args()


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

        print(f"{green}[+]{end} {ip}            ")

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
    
    with open(file, 'r') as f:
        lines = f.readlines()
    
    return lines
    

def Shodan():
    banner()

    print(f"{yellow}[=]{end} Getting MongoDB Hosts from shodan")

    api = shodan.Shodan(args.shodan)
    lines = []
    results = api.search("MongoDB", limit=1000)

    for result in results['matches']:
        ip = result['ip_str']
        lines.append(ip)
    
    return lines


def Masscan():
    banner()

    print(f"{yellow}[=]{end} Checking for masscan installation")
    
    if not os.path.isfile('/usr/bin/masscan'):
        print(f"{red}[-]{end} Make sure you've installed Masscan and it's present in the '/usr/bin/' directory")
        exit(0)

    banner()
    print(f"{yellow}[=]{end} Getting MongoDB Hosts from masscan")

    input(f"{yellow}[=]{end} If you cannot wait for the scan to finish hit 'ctrl/cmd + c' to stop the scan and wait a few seconds. Hit ENTER to contine")
    
    try:
        os.system(f"masscan 0.0.0.0/0 -p27017 --exclude 255.255.255.255 --rate {args.masscan} --open-only | awk '{print $6}' > masscan.txt")
    except KeyboardInterrupt:
        pass

    lines = InputFile('masscan.txt')
    return lines


def main():
    banner()

    try:
        requests.get('https://google.com')
        pass
    except:
        print(f"{red}[-]{end} Network Issue, make sure your network connection is working and retry")
        exit(0)


    if args.input != None:
        lines = InputFile(args.input)

    elif args.shodan != None:
        lines = Shodan()

    elif args.masscan != None:
        lines = Masscan()

    else:
        exit(0)

    print(f"{yellow}[=]{end} Scanning {len(lines)} hosts\n")

    i = 1
    for line in lines:
        ip = line.strip('\n')
        Check(ip)
        print(f"{green}[+]{end} Scanned {i}/{len(lines)} hosts", end="\r")
        i += 1

    print(f"{green}[+]{end} Found {open_instances} open hosts out of {len(lines)}")
    print("Thank You")


if __name__ == "__main__":
    main()

