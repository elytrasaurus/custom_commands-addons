# Automatically scans a folder and sorts loose files into subfolders based on extension.
import os
import sys
import shutil

def main():
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

    print(f"[+] Organizing directory structure: {target_dir}")
    moved_count = 0

    try:
        for entry in os.scandir(target_dir):
            if entry.is_file():
                filename = entry.name
                ext = os.path.splitext(filename)[1].lower()
                
                # Skip hiding or organizing your toolkit files if running inside it
                if filename.endswith(".py") or filename.endswith(".bat") or filename.endswith(".json"):
                    continue

                for category, extensions in FILE_CATEGORIES.items():
                    if ext in extensions:
                        dest_folder = os.path.join(target_dir, category)
                        os.makedirs(dest_folder, exist_ok=True)
                        shutil.move(entry.path, os.path.join(dest_folder, filename))
                        moved_count += 1
                        break

        print(f"[SUCCESS] Sorting complete. Cleaned up and moved {moved_count} files.")
    except Exception as e:
        print(f"[-] Automation error during sorting sequence: {e}")

if __name__ == "__main__":
    main()
