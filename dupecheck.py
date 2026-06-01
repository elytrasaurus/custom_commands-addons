# Scans a folder and checks file size and data content to locate exact duplicate files.
import os
import sys
import hashlib

def calculate_hash(path, block_size=65536):
    hasher = hashlib.md5()
    try:
        with open(path, 'rb') as f:
            buf = f.read(block_size)
            while len(buf) > 0:
                hasher.update(buf)
                buf = f.read(block_size)
        return hasher.hexdigest()
    except Exception:
        return None

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(target_dir):
        print(f"[-] Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"[+] Scanning maps and calculating file hashes inside: {target_dir}...")
    hashes = {}
    duplicates = []

    try:
        for root, _, files in os.walk(target_dir):
            # FIXED: Hard-block environmental spam from paths instantly
            if any(ignored in root.lower() for ignored in ['.venv', '.git', '__pycache__', 'site-packages']):
                continue

            for filename in files:
                filepath = os.path.join(root, filename)
                
                if os.path.islink(filepath):
                    continue
                try:
                    # Skip files smaller than 5KB (ignoring tiny empty metadata files)
                    if os.path.getsize(filepath) < 5120:
                        continue

                    file_hash = calculate_hash(filepath)
                    if not file_hash:
                        continue

                    if file_hash in hashes:
                        duplicates.append((filepath, hashes[file_hash]))
                    else:
                        hashes[file_hash] = filepath
                except Exception:
                    continue

        if not duplicates:
            print("[+] Scan complete: Zero duplicate file contents detected.")
            return

        print("\n=== DETECTED DUPLICATE COPIES ===")
        for dup, original in duplicates:
            print(f"\n[DUPLICATE]: {os.path.basename(dup)}")
            print(f"  -> Path: {dup}")
            print(f"  -> Original match is located at: {original}")
        print("=================================")

    except Exception as e:
        print(f"[-] Diagnostic check aborted: {e}")

if __name__ == "__main__":
    main()
