import os, sys, shodan, json, requests
from pymongo import MongoClient
from datetime import datetime as dt
from time import sleep


red ='\033[91m'
green= '\033[92m'
yellow = '\033[93m'
end= '\033[0m'


abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)


try:
    with open('config.json', 'r') as f:
        data = json.load(f)
    KEY = data['KEY']
    TOS = data['TOS']
except Exception:
    KEY = None
    TOS = None



def banner():
    os.system('clear')

    print('''
                                  ______ _    _ _   _ 
                                  | ___ \ |  | | \ | |   
 _ __ ___   ___  _ __   __ _  ___ | |_/ / |  | |  \| |
| '_ ` _ \ / _ \| '_ \ / _` |/ _ \|  __/| |/\| | . ` |
| | | | | | (_) | | | | (_| | (_) | |   \  /\  / |\  |
|_| |_| |_|\___/|_| |_|\__, |\___/\_|    \/  \/\_| \_/
                        __/ |                         
                       |___/

    By: Assassinumz
''')


def check():
    banner()
    if str(os.name) == 'nt':
        print(f"{red}[-]{end} This program is incompatible with windows. Retry in a Linux OS")
        sys.exit()

    if not os.path.isfile('/usr/bin/masscan'):
        print(f"{red}[-]{end} Make sure you've installed Masscan and it's present in the '/usr/bin/' directory")
        sys.exit()

    try:
        requests.get('https://google.com')
        pass
    except:
        print(f"{red}[-]{end} Network Issue, make sure your network connection is working and retry")
        sys.exit()

    if TOS != "Yes":
        print(f"{yellow}[=]{end} This tool is for educational purposes only, and complete responsibility of the End-User. Do not cause any harm to the Databases you find and inform the developers.")
        inp = input(f"Do you agree on the TOS ? (Y/N)\n-> ")
        
        if inp.lower() in ['n', 'no']:
            print("okay...")
            sys.exit()
        
        elif inp.lower() in ['y', 'yes']:
            data['TOS'] = "Yes"
            
            with open("config.json", 'w') as f:
                json.dump(data, f, indent=4)
        
        else:
            sys.exit()


def file_read():
    banner()
    file = input(f"{yellow}[=]{end} Enter File Location (Example: /root/host_list.txt):\n-> ")

    ips = []

    if os.path.isfile(file):
        with open(file, 'r') as f:
            hosts = f.readlines()

        for line in hosts:
            line = line.strip('\n')
            ips.append(line)
    
        return ips

    else:
        print(f"\n{red}[-]{end} File not found, make sure the path you've enter is right")
        input("Hit RETURN to continue")
        file_read()


def generate():
    banner()
    ips = []

    choice = int(input(f"{yellow}[=]{end} Choose a Scan method:\n1) Shodan\n2) Masscan\n-> "))
    
    if choice == 1:

        if KEY is None:
            KEY = input(f"\n{yellow}[=]{end} Enter your Shodan API key:\n-> ")

        api = shodan.Shodan(str(KEY))
      
        results = api.search("mongodb")
        
        for result in results['matches']:
            ip = result['ip_str']
            ips.append(ip)

        return ips

    elif choice == 2:
        input(f"{yellow}[=]{end} Once you have enough hosts hit 'ctrl + c' to stop the scan and wait a few seconds\nHit RETURN to continue")
        try:
            os.system("masscan 0.0.0.0/0 -p27017 --exclude 255.255.255.255 --open-only | awk '{print $6}' > masscan.txt")

        except KeyboardInterrupt:
            pass
        
        with open('masscan.txt', 'r') as f:
            lines = f.readlines()
        
        for line in lines:
            line = line.strip('\n')
            ips.append(line)
        
        return ips

        
def mongo_scan():
    banner()

    choose = input(f"{yellow}[=]{end} Do you want the program to generate a list of hosts running mongoDB ? (Y/N)\n-> ")

    if choose.lower() in ['n', 'no']:
        ips = file_read()
    
    elif choose.lower() in ['y', 'yes']:
        ips = generate()

    banner()
    print(f"{green}[+]{end} Found {len(ips)} hosts\n")

    filename = "open_instances" + str(dt.now().strftime('[%a, %d-%m-%Y %H.%M]')) +".txt"
    print(f"{yellow}[=]{end} Starting the scan\n")

    for ip in ips:
        client = MongoClient(str(ip), socketTimeoutMS=1000, serverSelectionTimeoutMS=1000)
        if client is None:
            print(f"{red}[-]{end} Failed : {ip}")
            continue

        try:
            dbs = client.list_database_names()

            print(f"{green}[+]{end} Found Open Instance: {ip}")

            with open(filename, 'a') as f:
                f.write(f"{ip}\n")
                
            continue

        except Exception:
            print(f"{red}[-]{end} Failed : {ip}")
            continue

    main()


def main():
    banner()

    print(f"{yellow}[=]{end} Choose an option:\n1) Scan\n0) Exit")
    # Todo : Connect to host option
    try:
        choose = int(input('-> '))
    except Exception:
        print(f"{red}[-]{end} Invalid Input")
        sleep(2)
        main()

    if choose == 0:
        sys.exit()

    elif choose == 1:
        mongo_scan()

    else:
        main()


if  __name__ == "__main__":
    check()
    main()