# Let's you see any file in hexadecimal form.
# /// script
# dependencies = []
# ///
import sys
import os

def main():
    if len(sys.argv) < 2:
        print("Usage: hexview <file_path> [bytes_to_read]")
        sys.exit(1)

    file_path = sys.argv[1]
    # Default to reading the first 256 bytes if not specified
    max_bytes = int(sys.argv[2]) if len(sys.argv) > 2 else 256

    if not os.path.isfile(file_path):
        print(f"[-] Error: File '{file_path}' not found.")
        sys.exit(1)

    print(f"=== HEX VIEW: {os.path.basename(file_path)} (First {max_bytes} bytes) ===")
    try:
        with open(file_path, "rb") as f:
            data = f.read(max_bytes)

        for i in range(0, len(data), 16):
            chunk = data[i:i+16]
            # Create hex representation
            hex_str = " ".join(f"{b:02X}" for b in chunk)
            # Create readable printable ASCII representation
            ascii_str = "".join(chr(b) if 32 <= b <= 126 else "." for b in chunk)
            
            # Align the output formatting
            print(f"{i:08X}:  {hex_str.ljust(47)}  |{ascii_str}|")
            
    except Exception as e:
        print(f"[-] Error parsing file binary: {e}")

if __name__ == "__main__":
    main()
