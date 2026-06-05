# Checks the SHA-256 hash of a file against a known threat database.
import os
import sys
import hashlib
import json
import urllib.request
import urllib.error

def print_usage():
    print("Custom Commands Hash Reputation Checker (hc)")
    print("Usage: hc <file_path>")
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

def check_database(sha256_hash):
    url = f"https://hashlookup.circl.lu/lookup/sha256/{sha256_hash}"
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'CustomCommands-SecurityToolkit/1.0', 'Accept': 'application/json'}
    )
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print("\n==================================================")
                print("[+] Hash located in public database registries.")
                
                # Fetch explicit name and trust scores
                file_name = data.get("FileName", data.get("filename", "Unknown File"))
                trust_score = data.get("hashlookup:trust", 50)  # Default score is 50
                source_db = data.get("source", "Unknown Database")
                
                print(f"  Registered Name: {file_name}")
                print(f"  Database Source: {source_db}")
                print(f"  Trust Threshold: {trust_score}/100")
                print("--------------------------------------------------")
                
                # Logic based on CIRCL's official trust taxonomy
                if trust_score > 50:
                    print("  [SAFE] Confirmed standard operating system/vendor binary.")
                elif trust_score < 50:
                    print("  [WARNING] High Threat Indicator! Degraded reputation score.")
                else:
                    print("  [NEUTRAL] Unranked Match: File logged but has neutral reputation.")
                print("==================================================")
                return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("\n[+] Database Result: Unknown File (Not logged or reported in this database).")
            return False
        else:
            print(f"\n[!] Database lookup failed (HTTP {e.code}). Skipping cloud check.")
    except Exception as e:
        print(f"\n[!] Network error or timeout. Skipping cloud check.")
    return False

def main():
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)
        
    file_path = sys.argv[1]
    print(f"[*] Calculating checksum attributes...")
    sha256 = calculate_sha256(file_path)
    
    if sha256:
        print(f"[+] SHA-256 Hash: {sha256}")
        print("[*] Contacting public hash verification service...")
        check_database(sha256)
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()

