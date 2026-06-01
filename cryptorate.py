# Track crypto.
# /// script
# dependencies = []
# ///
import sys
import json
import urllib.request

def main():
    # Fetches live public spot conversion indices from Coinbase
    url = "https://api.coinbase.com/v2/prices/USD/spot"
    print("[+] Pulling down active currency ticker matrices...")
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            raw_data = response.read().decode('utf-8')
            
        parsed = json.loads(raw_data)
        data_list = parsed.get("data", [])
        
        # Filter down to interesting baseline assets
        targets = {"BTC", "ETH", "SOL", "LTC", "DOGE"}
        
        print("\n==========================================")
        print("       LIVE DIGITAL ASSET VALUATIONS       ")
        print("==========================================")
        print(f" {'ASSET SYMBOL':<16} | {'MARKET VALUE (USD)':<20}")
        print("------------------------------------------")
        
        for asset in data_list:
            base = asset.get("base")
            if base in targets:
                amount = float(asset.get("amount", 0))
                print(f"  {base:<14} | ${amount:,.2f}")
                
        print("==========================================")
        
    except Exception as e:
        print(f"[-] Marketplace connection time out: {e}")

if __name__ == "__main__":
    main()
