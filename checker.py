import requests
import json
import random
import argparse
from decimal import Decimal
from faker import Faker
from colorama import Fore, Style, init

init(autoreset=True)  # Initialize colorama

def get_random_headers():
    fake = Faker()
    return {
        'User-Agent': fake.user_agent(),
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.layerzero.foundation/',
        'Origin': 'https://www.layerzero.foundation',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
    }

def parse_proxy(proxy_string):
    parts = proxy_string.split(':')
    if len(parts) == 2:
        return f"http://{proxy_string}"
    elif len(parts) == 4:
        return f"http://{parts[2]}:{parts[3]}@{parts[0]}:{parts[1]}"
    elif len(parts) >= 3:
        protocol = parts[0].lower()
        if protocol not in ('http', 'https', 'socks4', 'socks5'):
            protocol = 'http'
        return f"{protocol}://{':'.join(parts[1:])}"
    else:
        return None

def load_proxies(proxy_file):
    with open(proxy_file, 'r') as f:
        return [parse_proxy(line.strip()) for line in f if parse_proxy(line.strip())]

def check_allocation(address, proxies, max_retries=3):
    url = f"https://www.layerzero.foundation/api/proof/{address}"
    headers = get_random_headers()
    
    for _ in range(max_retries):
        try:
            proxy = random.choice(proxies) if proxies else None
            proxy_dict = {'http': proxy, 'https': proxy} if proxy else None
            
            response = requests.get(url, headers=headers, proxies=proxy_dict, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                amount = Decimal(data['amount']) / Decimal('1e18')
                round1 = Decimal(data['round1']) / Decimal('1e18')
                round2 = Decimal(data['round2']) / Decimal('1e18')
                return address, round1, round2, amount
            else:
                # Print the error message from the API response
                print(Fore.RED + f"{address} | {response.text.strip()}")
                return None
        except requests.RequestException as e:
            print(Fore.YELLOW + f"Request failed for {address}: {str(e)}")
    
    print(Fore.RED + f"All attempts failed for {address}")
    return None

def main():
    parser = argparse.ArgumentParser(description="Check LayerZero allocations with proxy support")
    parser.add_argument('--proxy', help="Path to proxy file")
    parser.add_argument('--no-proxy', action='store_true', help="Run without proxies")
    args = parser.parse_args()

    proxies = [] if args.no_proxy else (load_proxies(args.proxy) if args.proxy else [])

    print(Fore.CYAN + "Wallet                                     | Round 1    | Round 2    | Total")
    print(Fore.CYAN + "-" * 80)

    total_round1 = Decimal('0')
    total_round2 = Decimal('0')
    total_amount = Decimal('0')
    checked_addresses = set()

    with open('wallet.txt', 'r') as file:
        for line in file:
            address = line.strip()
            if address in checked_addresses:
                continue
            checked_addresses.add(address)
            
            result = check_allocation(address, proxies)
            if result:
                addr, r1, r2, total = result
                print(Fore.GREEN + f"{addr} | {r1:10.2f} | {r2:10.2f} | {total:10.2f}")
                total_round1 += r1
                total_round2 += r2
                total_amount += total

    print(Fore.CYAN + "-" * 80)
    print(Fore.MAGENTA + Style.BRIGHT + f"{'TOTAL':42} | {total_round1:10.2f} | {total_round2:10.2f} | {total_amount:10.2f}")

if __name__ == "__main__":
    main()
