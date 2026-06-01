# Lists files inside your current directory sorted by exactly how much space they take up.
# /// script
# dependencies = []
# ///
import os
import sys

def format_size(bytes_size):
    """Converts raw bytes to a human-readable string format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(target_dir):
        print(f"[-] Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    print(f"[+] Scanning directory and indexing object footprints: {target_dir}\n")
    
    file_list = []
    try:
        for entry in os.scandir(target_dir):
            if entry.is_file():
                file_list.append((entry.name, entry.stat().st_size))
        
        # Sort items highest footprint to lowest footprint
        file_list.sort(key=lambda x: x[1], reverse=True)

        print("==================================================")
        print(f" {'FILE NAME':<32} | {'STORAGE SIZE':<15}")
        print("==================================================")
        
        if not file_list:
            print("  (No files found inside this target directory location)")
        
        for name, size in file_list[:25]: # Caps out viewing layout to top 25 biggest files
            short_name = name if len(name) <= 30 else name[:27] + "..."
            print(f"  {short_name:<30} | {format_size(size):<15}")
            
        print("==================================================")

    except Exception as e:
        print(f"[-] System mapping error: {e}")

if __name__ == "__main__":
    main()
