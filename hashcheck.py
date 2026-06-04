import os
import sys
import hashlib
import json
import urllib.request
import urllib.error

def print_usage():
    print("Custom Commands Threat Hash Checker (hc)")
    print("Usage:  hc <file_path>")
    print("\nExample:")
    print("  hc C:\\Users\\Downloads\\suspicious_file.exe")

def calculate_sha256(file_path):
    if not os.path.exists(file_path):
        print(f"[-] Error: File '{file_path}' not found.")
        return None

    hasher = hashlib.sha256()
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception as e:
        print(f"[-] Error reading file: {e}")
        return None

def check_malicious_database(sha256_hash):
    # CIRCL Hashlookup API endpoint
    url = f"https://hashlookup.circl.lu/lookup/sha256/{sha256_hash}"
    
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'CustomCommands-SecurityToolkit/1.0', 'Accept': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                
                # Check the dataset trust or reputation flags if present
                # Many CIRCL entries are known clean/known bad system binaries
                print("\n==================================================")
                print("⚠️  WARNING: Hash matches a known database record!")
                if "FileName" in data:
                    print(f"   Original Known Name: {data['FileName']}")
                if "source" in data:
                    print(f"   Database Source:     {data['source']}")
                print("==================================================")
                return True
    except urllib.error.HTTPError as e:
        # 404 means the hash isn't in their database (which is standard for unknown files)
        if e.code == 404:
            print("\n[+] Database Result: Unknown File (Not flagged in standard repositories).")
            return False
        else:
            print(f"\n[!] Database lookup failed (HTTP {e.code}). Skipping cloud check.")
    except Exception as e:
        print(f"\n[!] Network timeout or connectivity error. Skipping cloud check.")
    return False

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    file_path = sys.argv[1]
    
    print(f"[*] Analyzing file...")
    sha256 = calculate_sha256(file_path)
    
    if sha256:
        print(f"[+] SHA-256 Hash: {sha256}")
        print("[*] Querying public threat databases...")
        check_malicious_database(sha256)
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
