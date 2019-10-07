<h1 align="center">MongoPWN</h1>

<p align="center">Search for unauthenticated mongoDB services with Shodan and Masscan</p>

<p align="center">
  <a href="https://python.org">
    <img src="https://img.shields.io/static/v1.svg?label=Python&message=3.6.8&color=blue&style=popout-square" alt="Discord Server">
  </a>
    
  <a href="https://discord.gg/3nfQadt">
    <img src="https://img.shields.io/discord/264666918034604032.svg?color=%237289DA&label=Discord&style=popout-square"                                                              alt="Discord Server">
  </a>
  </p>

## TESTED ON

*  **Kali Linux - Rolling Edition**

## PREREQUISITES

* Python >= 3.6.8

* [Masscan](https://github.com/robertdavidgraham/masscan)

* Shodan API key (optional)

## FEATURES

* Checks for Open MongoDB instances on the Internet with Shodan or Masscan

* You can also provide your own Host List

* Stores hosts IPs with open authintication in `open_instances-[datetime].txt`

## INSTALLATION

* Clone the repo
`git clone https://github.com/Assassinumz/mongoPWN.git`

* Install the requirements
`pip install -r requirements.txt`
            or
`python3 -m pip install -r requirements.txt`

* (optional) Enter your Shodan API Key in [config.json](config.json) (you can also do it while running the tool)
```
{
  "KEY" : "Your Key  Here"      # Change null to your key
}
```

* Run the tool
`python main.py`


