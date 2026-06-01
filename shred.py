# Permanently deletes a file that you chose.
# /// script
# dependencies = []
# ///
import os
import sys

def main():
    if len(sys.argv) < 2:
        print("Usage: shred <file_path>")
        sys.exit(1)

    target_file = sys.argv[1]

    if not os.path.isfile(target_file):
        print(f"[-] Error: '{target_file}' is not a valid file.")
        sys.exit(1)

    print(f"[!] WARNING: Shredding will permanently destroy '{target_file}'. The owner (elytrasaurus) is not responsible if this program causes damage.")
    confirm = input("Are you absolutely sure? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        sys.exit(0)

    try:
        file_size = os.path.getsize(target_file)
        print("[+] Sanitizing data sectors with binary zeros...")
        with open(target_file, "ba+", buffering=0) as f:
            f.write(b'\x00' * file_size)
        os.remove(target_file)
        print("[SUCCESS] File wiped and destroyed permanently.")
    except Exception as e:
        print(f"[-] Error shredding file: {e}")

if __name__ == "__main__":
    main()
