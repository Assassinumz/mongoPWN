#!/bin/python3
#
#                           MongoPWN
#         A simple script to find open mongoDB instances 
#                 on the internet using shodan
#                         
#                      by: Assassin umz


import os, platform
import argparse, shodan
from pymongo import MongoClient
from colorama import init, Fore, Style

init(convert=True)
red = Fore.RED
green = Fore.GREEN
yellow = Fore.YELLOW
end = Style.RESET_ALL


parser = argparse.ArgumentParser()

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-i', '--input', help="Hosts IPs file path, must be in seperate lines")
group.add_argument('-s', '--shodan', help="Get a list of hosts from shodan, provide the API key")

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


def main(lines):
    banner()

    #TODO: Add Counter
    print(f"{yellow}[=]{end} Scanning {len(lines)} hosts\n")
    open_instances = 0

    for line in lines:
        ip = line.strip('\n')
        client = MongoClient(str(ip), socketTimeoutMS=1000, serverSelectionTimeoutMS=1000)
        if client is None:
            continue

        try:
            dbs = client.list_database_names()

            print(f"{green}[+]{end} {ip}")

            if args.output != None:
                with open(args.output, 'a') as f:
                    f.write(f"{ip}\n")
            open_instances+=1                
            continue

        except Exception:
            continue
    
    print(f"{green}[+]{end} Found {open_instances} open hosts out of {len(lines)}")
    print("Thank You")


def InputFile(file):

    if not os.path.isfile(file):
        print(f"{red}[-]{end} File Does not exist")
        exit(0)
    
    with open(file, 'r') as f:
        lines = f.readlines()
    
    main(lines)
    

def Shodan():
    banner()

    print(f"{yellow}[=]{end} Getting MongoDB Hosts from shodan")

    api = shodan.Shodan(args.shodan)
    lines = []
    results = api.search("MongoDB", limit=1000)

    for result in results['matches']:
        ip = result['ip_str']
        lines.append(ip)
    
    main(lines)


if args.input != None:
    InputFile(args.input)

elif args.shodan != None:
    Shodan()

else:
    exit(0)

#TODO: Add masscan

