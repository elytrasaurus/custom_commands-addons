# Allows you to input a folder tree, and it creates all the files.
import os
import sys

def print_usage():
    print("Custom Commands Project Structuralizer (struct)")
    print("Usage: struct")
    print("       Type or paste your tree layout (e.g., copied from text or a prompt).")
    print("       When finished, press Ctrl+Z and then press Enter to build it.")

def parse_and_create_tree(lines):
    # Track folder anchors at different depths
    # Level 0 anchors to the current directory where you run the command
    level_dirs = {0: os.getcwd()}
    
    for line in lines:
        clean_line = line.rstrip()
        if not clean_line.strip():
            continue
            
        # Determine depth by measuring the layout symbols and spaces
        stripped = clean_line.lstrip(' │├└─\t')
        indentation_length = len(clean_line) - len(stripped)
        
        # Calculate nesting depth (roughly groups indentation levels)
        depth = (indentation_length // 4) + 1 if indentation_length > 0 else 0
        
        # Check if explicitly defined as a directory with trailing slashes
        is_dir = stripped.endswith('/') or stripped.endswith('\\')
        name = stripped.strip('/\\ ')
        
        # Handle multi-file shortcut strings like: "main.py and gui.py"
        if " and " in name:
            names_to_process = [n.strip() for n in name.split(" and ")]
        else:
            names_to_process = [name]

        for item_name in names_to_process:
            parent_dir = level_dirs.get(depth, os.getcwd())
            target_path = os.path.join(parent_dir, item_name)
            
            # Simple heuristic: If it contains a dot and isn't marked as a folder, it's a file
            if '.' in item_name and not is_dir:
                os.makedirs(parent_dir, exist_ok=True)
                if not os.path.exists(target_path):
                    with open(target_path, 'w', encoding='utf-8') as f:
                        f.write("") # Create an empty file
                    print(f"[+] File:   {os.path.relpath(target_path)}")
            else:
                # It's a directory
                os.makedirs(target_path, exist_ok=True)
                print(f"[└──] Folder: {os.path.relpath(target_path)}")
                # Register this new directory for any deeper nested child items
                level_dirs[depth + 1] = target_path

def main():
    # If parameters are passed, or if it's hitting standard help flags
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "/?"]:
        print_usage()
        sys.exit(0)

    print("--- Structuralizer: Target -> Current Directory ---")
    print("Paste or type your layout tree structure below.")
    print("When finished, press Ctrl+Z and then press Enter to generate it.")
    print("-------------------------------------------------------")
    
    try:
        # Capture the entire input block until EOF (Ctrl+Z) just like write.py
        tree_content = sys.stdin.read()
        lines = tree_content.splitlines()
        
        if lines:
            print("\n[*] Generating structural elements...")
            parse_and_create_tree(lines)
            print("[Success] Project scaffolded successfully!")
        else:
            print("\n[Cancelled] No inputs detected.")
            
    except KeyboardInterrupt:
        print("\n[Cancelled] Operation aborted by user.")
    except Exception as e:
        print(f"\n[Error] Failure during execution: {e}")

if __name__ == "__main__":
    main()
