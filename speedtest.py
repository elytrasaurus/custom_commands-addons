# Checks your internet speed.
# /// script
# dependencies = []
# ///
import sys
import time
import urllib.request

def main():
    # Uses a safe, public 10MB test file hosted by a reliable infrastructure provider
    url = "https://speed.cloudflare.com/__down?bytes=10485760" 
    print("[+] Initializing internet network speed gauge...")
    print("[+] Downloading 10MB package block to calculate throughput...")
    
    start_time = time.time()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            _ = response.read()
        end_time = time.time()
        
        total_time = end_time - start_time
        # 10 Megabytes = 80 Megabits
        mbits = 80.0
        speed = mbits / total_time
        
        print("\n======================================")
        print("         NETWORK SPEED RESULTS        ")
        print("======================================")
        print(f" Time Elapsed : {total_time:.2f} seconds")
        print(f" Download Speed: {speed:.2f} Mbps (Megabits/sec)")
        print("======================================")
        
    except Exception as e:
        print(f"\n[-] Speed gauge interrupted: {e}")

if __name__ == "__main__":
    main()
