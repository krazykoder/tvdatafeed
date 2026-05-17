#!/usr/bin/env python3
"""
Script to download raw websocket data for symbols and save to .ws files
"""
import sys
import os

# Add parent directory to path to import tvDatafeed
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tvDatafeed import tvData

# List of symbols to download
SYMBOLS = [
    ('KLAC', 'NASDAQ'),
    ('AAPL', 'NASDAQ'),
    ('AMD', 'NASDAQ'),
    ('MU', 'NASDAQ'),
    ('AVGO', 'NASDAQ'),
]

def download_raw_data():
    """Download raw websocket data for symbols"""
    tv = tvData()  # no-login method
    
    print(f"Downloading raw websocket data for {len(SYMBOLS)} symbols...")
    
    for symbol, exchange in SYMBOLS:
        try:
            print(f"\n[*] Downloading {symbol} from {exchange}...")
            raw_data = tv.get_financials(symbol, exchange, debug=True)
            
            # Save to file
            filename = f"{symbol}_{exchange}.ws"
            filepath = os.path.join(os.path.dirname(__file__), filename)
            
            with open(filepath, 'w') as f:
                f.write(raw_data)
            
            # Print some stats
            print(f"    ✓ Saved to {filename}")
            print(f"    ✓ File size: {len(raw_data)} bytes")
            
            # Print first 200 chars to see format
            print(f"    ✓ First 200 chars: {raw_data[:200]}")
            
        except Exception as e:
            print(f"    ✗ Error downloading {symbol}: {e}")
    
    print("\n[+] Download complete!")
    print(f"[+] Raw data files saved in: {os.path.dirname(__file__)}")

if __name__ == '__main__':
    download_raw_data()
