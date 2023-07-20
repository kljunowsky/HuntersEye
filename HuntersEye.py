import logging
import sys
import datetime
import certstream
import json
import argparse
import requests
import yaml


def print_callback(message, context, single_domain, domain_list, tld_filter, output_format, telegram_webhook, output_file):
    logging.debug("Message -> {}".format(message))

    if message['message_type'] == "heartbeat":
        return

    if message['message_type'] == "certificate_update":
        all_domains = message['data']['leaf_cert']['all_domains']

        if len(all_domains) == 0:
            domain = "NULL"
        else:
            domain = all_domains[0]

        # Filter against specified domain and top level domain (TLD)
        if single_domain and not domain.endswith(single_domain):
            return

        if domain_list and not any(domain.endswith(d) for d in domain_list):
            return

        if tld_filter:
            all_domains = [domain for domain in all_domains if domain.endswith(tld_filter)]
        
        timestamp = datetime.datetime.now().strftime('%d/%m/%y %H:%M:%S')
        for subdomain in all_domains:
            if (not single_domain or subdomain.endswith(single_domain)) or \
               (not domain_list or any(subdomain.endswith(d) for d in domain_list)):
                output_data = {
                    'timestamp': timestamp,
                    'domain': subdomain,
                    'san': ", ".join(message['data']['leaf_cert']['all_domains'][1:])
                }

                if output_format == 'json':
                    print(json.dumps(output_data))
                else:
                    print("[{}] {} (SAN: {})".format(timestamp, subdomain, output_data['san']))
                sys.stdout.flush()

                if output_file:
                    save_to_file(output_file, output_data)

                # Trigger Telegram webhook
                if telegram_webhook:
                    trigger_telegram_webhook(telegram_webhook, output_data)


def load_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file]
    return domains




def trigger_telegram_webhook(config_file, data):
    with open(config_file, 'r') as file:
        config = yaml.safe_load(file)

    for telegram_config in config.get('telegram', []):
        api_key = telegram_config.get('telegram_api_key')
        chat_id = telegram_config.get('telegram_chat_id')
        parse_mode = telegram_config.get('telegram_parsemode')

        payload = {
            'text': f"New domain found\nTimestamp: {data['timestamp']}\nDomain: {data['domain']}\nSAN: {data['san']}",
            'chat_id': chat_id,
            'parse_mode': parse_mode
        }

        headers = {
            'Content-Type': 'application/json'
        }

        url = f"https://api.telegram.org/bot{api_key}/sendMessage"
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code != 200:
            logging.warning("Failed to trigger Telegram webhook. Status code: %d", response.status_code)

def save_to_file(output_file, data):
    with open(output_file, 'a') as file:
        file.write(json.dumps(data) + '\n')


def load_domains_from_file(file_path):
    with open(file_path, 'r') as file:
        domains = [line.strip() for line in file]
    return domains


def main():
    parser = argparse.ArgumentParser(description='SSL Certificate Filter')
    parser.add_argument('-d', '--domain', help='Filter certificates by domain')
    parser.add_argument('-df', '--domain-file', help='Filter certificates by domains from file')
    parser.add_argument('-tld', '--top-level-domain', help='Filter certificates by top-level domain (TLD)')
    parser.add_argument('-f', '--output-format', choices=['json', 'stdout'], default='stdout',
                        help='Output format for filtered certificates')
    parser.add_argument('-telegram', '--telegram-webhook', help='Telegram webhook URL')
    parser.add_argument('-o', '--output-file', help='Output file for filtered certificates')

    args = parser.parse_args()

    domain_list = None
    if args.domain_file:
        domain_list = load_domains_from_file(args.domain_file)

    logging.basicConfig(format='[%(levelname)s:%(name)s] %(asctime)s - %(message)s', level=logging.INFO)

    certstream.listen_for_events(lambda msg, ctx: print_callback(msg, ctx, args.domain, domain_list, args.top_level_domain,
                                                                 args.output_format, args.telegram_webhook,
                                                                 args.output_file),
                                 url='wss://certstream.calidog.io/')


if __name__ == "__main__":
    main()
