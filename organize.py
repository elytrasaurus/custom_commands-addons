# Automatically sorts files into subfolders after prompting you twice for confirmation.
import os
import sys
import shutil

def main():
    # Use current folder as default if no directory path is given as an argument
    target_dir = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()

    if not os.path.isdir(target_dir):
        print(f"[-] Error: '{target_dir}' is not a valid directory.")
        sys.exit(1)

    # Extension mapping groups
    FILE_CATEGORIES = {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
        "Images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov", ".flv"],
        "Music": [".mp3", ".wav", ".flac", ".m4a"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
        "Executables": [".exe", ".msi"]
    }

    # Scan the directory to find out exactly what files WILL be moved
    files_to_move = []
    
    try:
        for entry in os.scandir(target_dir):
            if entry.is_file():
                filename = entry.name
                ext = os.path.splitext(filename)[1].lower()
                
                # Safeguard: Skip core toolkit script and layout files
                if filename.endswith(".py") or filename.endswith(".bat") or filename.endswith(".json"):
                    continue

                # See if the file matches any of our categories
                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        files_to_move.append((entry.path, filename, category))
                        break
    except Exception as e:
        print(f"[-] Error scanning directory layout: {e}")
        sys.exit(1)

    # If there are no loose files to move, exit early and cleanly
    if not files_to_move:
        print(f"[+] Directory '{target_dir}' is already fully clean and organized!")
        sys.exit(0)

    # --- FIRST SAFETY PROMPT ---
    print(f"\n[⚠️  ATTENTION - GATE 1/2] You are about to organize the following directory:")
    print(f" -> Path: {target_dir}")
    print(f" -> Total loose files found to organize: {len(files_to_move)}\n")
    
    confirm1 = input("Are you sure you want to automatically move these files? [Y/N]: ").strip().lower()
    
    if confirm1 != 'y' and confirm1 != 'yes':
        print("[-] Operation aborted at Gate 1. No files were touched.")
        sys.exit(0)

    # --- SECOND SAFETY PROMPT ---
    print(f"\n[⚠️  FINAL WARNING - GATE 2/2]")
    print(f" This will permanently rearrange files in this folder into subdirectories.")
    
    confirm2 = input("Are you ABSOLUTELY sure? This action cannot be easily undone. [Y/N]: ").strip().lower()
    
    if confirm2 != 'y' and confirm2 != 'yes':
        print("[-] Operation aborted at Gate 2. No files were touched.")
        sys.exit(0)
    # ----------------------------

    # If the user passed both gates, proceed with the automated sort loop
    print("\n[+] Both gates cleared! Organizing directory structure now...")
    moved_count = 0

    try:
        for src_path, filename, category in files_to_move:
            dest_folder = os.path.join(target_dir, category)
            
            # Make sure the category folder exists
            os.makedirs(dest_folder, exist_ok=True)
            
            # Move the file safely
            shutil.move(src_path, os.path.join(dest_folder, filename))
            print(f" -> Moved '{filename}' into {category}/")
            moved_count += 1

        print(f"\n[SUCCESS] Sorting complete! Automatically organized {moved_count} files.")
    except Exception as e:
        print(f"[-] Automation error during sorting sequence: {e}")

if __name__ == "__main__":
    main()
