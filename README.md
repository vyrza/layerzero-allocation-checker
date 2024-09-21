# LayerZero Allocation Checker

This script checks the LayerZero token allocation for Ethereum addresses using the LayerZero API. It supports proxy usage for making requests.

## Features

- Checks LayerZero token allocation for multiple Ethereum addresses
- Supports proxy usage for API requests
- Displays allocation results in a neat, colored table format
- Calculates and displays total allocation across all addresses

## Requirements

- Python 3.6+
- Required Python packages: `requests`, `faker`, `colorama`

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/layerzero-allocation-checker.git
   cd layerzero-allocation-checker
   ```

2. Install required packages:
   ```
   pip install requests faker colorama
   ```

## Usage

1. Create a `wallet.txt` file with one Ethereum address per line.

2. (Optional) Create a `proxies.txt` file with one proxy per line if you want to use proxies.

3. Run the script:
   ```
   python checker.py
   ```

   To use proxies:
   ```
   python checker.py --proxy proxies.txt
   ```

   To run without proxies:
   ```
   python checker.py --no-proxy
   ```

## Output

The script will display a table with the following columns:
- Wallet address
- Round 1 allocation
- Round 2 allocation
- Total allocation

At the end, it will show the total allocation across all addresses.

## Disclaimer

This script is for educational purposes only. Please use responsibly and in accordance with LayerZero's terms of service.
