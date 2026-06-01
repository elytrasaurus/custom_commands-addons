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

    print(f"[+] Filtering system files and scanning directory contents inside: {target_dir}...")
    hashes = {}
    duplicates = []

    # Directories we want to skip completely to avoid technical spam
    IGNORED_DIRS = {'.venv', '.git', '__pycache__', 'node_modules', '.idea', '.vscode'}
    # Minimum file size in bytes to check (10 KB) to ignore tiny identical files
    MIN_SIZE_BYTES = 10 * 1024 

    try:
        for root, dirs, files in os.walk(target_dir):
            # Modifying dirs in-place tells os.walk to completely skip walking into ignored folders
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for filename in files:
                filepath = os.path.join(root, filename)
                
                if os.path.islink(filepath):
                    continue

                try:
                    # Check size first to filter out tiny configurations
                    file_size = os.path.getsize(filepath)
                    if file_size < MIN_SIZE_BYTES:
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
            print("[+] Scan complete: Zero duplicate file contents detected (ignoring system/empty files).")
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
