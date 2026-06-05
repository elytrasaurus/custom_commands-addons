# Checks the hash of a file.
import os
import sys
import hashlib

def print_usage():
    print("Custom Commands Local Hash Checker (hc)")
    print("Usage:  hc <hash_type> <file_path>")
    print("Supported types: md5, sha1, sha256, sha512")
    print("\nExample:")
    print("  hc sha256 C:\\Users\\Downloads\\file.exe")

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    hash_type = sys.argv[1].lower()
    file_path = sys.argv[2]

    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)

    # Resolve the correct hashing algorithm
    if hash_type == 'md5':
        hasher = hashlib.md5()
    elif hash_type == 'sha1':
        hasher = hashlib.sha1()
    elif hash_type == 'sha256':
        hasher = hashlib.sha256()
    elif hash_type == 'sha512':
        hasher = hashlib.sha512()
    else:
        print(f"Unsupported hash type: '{hash_type}'. Use md5, sha1, sha256, or sha512.")
        sys.exit(1)

    # Stream file data efficiently
    try:
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        # Output exactly what you wanted: just the hash string
        print(hasher.hexdigest())
        sys.exit(0)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

