#!/usr/bin/env python3
"""
Mallard Token Stats Fetcher for Bithomp API
Designed to run in GitHub Actions
"""

import json
import requests
import os
import sys

# Get API key from environment variable
API_KEY = os.environ.get('BITHOMP_API_KEY')

if not API_KEY:
    print('ERROR: BITHOMP_API_KEY environment variable not set')
    sys.exit(1)

ISSUER = 'raaoPU9crbLGEFCMyh8moNH4gipsHJY3wN'
CURRENCY = '4D414C4C41524400000000000000000000000000'

# API endpoint for token information
API_URL = f'https://bithomp.com/api/v2/token/{ISSUER}/{CURRENCY}'

def fetch_token_data():
    """Fetch token data from Bithomp API"""
    headers = {
        'x-bithomp-token': API_KEY
    }
    
    try:
        print('Fetching Mallard token stats...')
        response = requests.get(API_URL, headers=headers, timeout=10)
        response.raise_for_status()
        
        token_data = response.json()
        print(f'Received data: {json.dumps(token_data, indent=2)}')
        
        # Extract relevant data
        stats = {
            'trustlines': token_data.get('trustlines', 0),
            'holders': token_data.get('holders', 0),
            'supply': float(token_data.get('supply', 0)),
            'marketCap': calculate_market_cap(token_data)
        }
        
        # Write to stats.json
        with open('stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        
        print('Stats updated successfully:')
        print(json.dumps(stats, indent=2))
        return stats
        
    except requests.exceptions.RequestException as e:
        print(f'Error fetching data: {e}')
        stats = {
            'trustlines': 0,
            'holders': 0,
            'supply': 0,
            'marketCap': 0
        }
        with open('stats.json', 'w') as f:
            json.dump(stats, f, indent=2)
        sys.exit(1)
    except Exception as e:
        print(f'Unexpected error: {e}')
        sys.exit(1)

def calculate_market_cap(token_data):
    """Calculate market cap from token data"""
    if 'marketCap' in token_data:
        return float(token_data['marketCap'])
    
    if 'price' in token_data and 'supply' in token_data:
        price = float(token_data['price'])
        supply = float(token_data['supply'])
        return price * supply
    
    if 'priceInXrp' in token_data and 'supply' in token_data:
        price_xrp = float(token_data['priceInXrp'])
        supply = float(token_data['supply'])
        return price_xrp * supply
    
    return 0

if __name__ == '__main__':
    fetch_token_data()
