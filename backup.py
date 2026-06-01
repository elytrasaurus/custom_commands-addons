# Let's you back up files to a separate directory.
# /// script
# dependencies = []
# ///
import sys
import os
import shutil
from datetime import datetime

def main():
    if len(sys.argv) < 2:
        print("Usage: backup <file_or_folder_path> [target_backup_directory]")
        sys.exit(1)

    source = sys.argv[1]
    # Default to a local 'Backups' folder if target isn't specified
    dest_base = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.getcwd(), "Backups")

    if not os.path.exists(source):
        print(f"[-] Error: Source target '{source}' does not exist.")
        sys.exit(1)

    # Generate a unique folder name using the current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.basename(os.path.abspath(source))
    backup_folder = os.path.join(dest_base, f"backup_{base_name}_{timestamp}")

    try:
        if not os.path.exists(backup_folder):
            os.makedirs(backup_folder)

        if os.path.isdir(source):
            # Target is a folder; copy the directory tree structure
            final_dest = os.path.join(backup_folder, base_name)
            shutil.copytree(source, final_dest)
        else:
            # Target is a single file; copy it over cleanly
            shutil.copy2(source, backup_folder)

        print(f"\n[SUCCESS] Backup complete!")
        print(f" -> Destination: {backup_folder}")

    except Exception as e:
        print(f"[-] Backup architecture failure: {e}")

if __name__ == "__main__":
    main()
