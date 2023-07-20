<h1 align="center">
Hunters Eye 🧿
</h1>

<p align="center">
    <img src="HunterEyes.svg" height="50%" width="50%" Setfill=None>
</p>


<p align="center">
HuntersEye is designed for Bug Bounty Hunters, and Security Researchers to monitor new subdomains and certificates for specified domains. The primary goal is to streamline and expedite the process of monitoring newly registered subdomains and SSL certificates related to specified target domains. The rapid identification and penetration of new subdomains a is crucial for bug bounty hunting.
</p>

<h3 align="center">
  Be one step ahead with HuntersEye.
</h3>

## Installation 🏗️

```
pip3 install -r requirements.txt
```

## Usage 🛠 

Filter newly issued certificates by domain
```
python3 HuntersEye.py -d tesla.com
```

Filter newly issued certificates by domains from the file
```
python3 HuntersEye.py -df domains.txt
```

Filter newly issued certificates by domains from file and notify on telegram with the output file
```
python3 HuntersEye.py -df domains.txt -telegram config.yaml -o output.json
```

## Telegram Config File 🔖
```
telegram:
  - id: "tel"
    telegram_api_key: "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    telegram_chat_id: "XXXXXXXXXX"
    telegram_parsemode: "Markdown"
```

## Running from Docker 🐳

Build
```
docker build -t hunterseye .
```

Run
```
docker run -v $(pwd)/data:/data  -ti hunterseye -df data/domains.txt -telegram data/config.yaml -o /data/output.json
```

## Parameters 🧰 

Parameter | Description | Type
------------ | ------------- | -------------
--domain / -d | Domain Filter | String
--domain-file / -df |Domains Filter| File
--top-level-domain / -df| TLD Filter | String
-telegram| Telegram Config File | File
--output-file / -o | Root domain used for CloudFlare Bypass| File
-f |STDOut Filter (text/json)| String

## Use Cases 📑

### Create a subdomain bruteforce wordlist

```
timeout 24h python3 HuntersEye.py -tld io -o output.json
cat output.json |jq -r '.domain' | dsieve -f 3 | awk -F '.' '{print $1}' | sort -u | tee subdomain_bruteforce.txt
```

[Dsieve](https://github.com/trickest/dsieve) from [Trickest](https://github.com/trickest/)

### Check the presence of web application on new subdomain

```
python3 HuntersEye.py -d target.tld -o output.json
cat output.json | jq -r '.domain' | httpx -tech-detect -status-code -title -web-server -ip -cdn -asn -o httpx_output.txt
``` 
[httpx](https://github.com/projectdiscovery/httpx) from [ProjectDiscovery](https://github.com/projectdiscovery)


### Vulnerability Scanning
```
python3 HuntersEye.py -d target.tld -o output.json
cat output.json | jq -r '.domain' | nuclei -o nuclei_output
```
[nuclei](https://github.com/projectdiscovery/nuclei) from [ProjectDiscovery](https://github.com/projectdiscovery)


### Port Scanning
```
python3 HuntersEye.py -d target.tld -o output.json
cat output.json | jq -r '.domain' | naabu -tp 10000 -o naabu_output.txt
```
[naabu](https://github.com/projectdiscovery/naabu) from [ProjectDiscovery](https://github.com/projectdiscovery)


## Contact Me 📇

[LinkedIn - Milan Jovic](https://www.linkedin.com/in/milan-jovic-sec/)

[Shift Security Consulting - Linkedin](https://www.linkedin.com/company/shift-security-consulting)

[Shift Security Consulting - Secure Your Digital Future](https://shiftsecurityconsulting.com)

[Twitter - Milan Jovic](https://twitter.com/milanshiftsec)
