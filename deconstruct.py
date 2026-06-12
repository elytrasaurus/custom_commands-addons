# Creates a file tree for your current folder.
import os
import sys

def print_usage():
    print("Custom Commands Project Deconstructor (deconstruct)")
    print("Usage:  deconstruct [max_depth]")
    print("        Generates a clean layout tree of the current directory.")
    print("\nExample:")
    print("  deconstruct")
    print("  deconstruct 2  (Limits how deep into folders it scans)")

def generate_tree(dir_path, prefix="", max_depth=None, current_depth=0):
    # Stop if we hit a user-defined depth limit
    if max_depth is not None and current_depth > max_depth:
        return

    try:
        # Filter out common clutter items you usually don't want in a clean tree layout
        ignored_items = {'.git', '__pycache__', '.venv', 'node_modules', '.uv'}
        items = [i for i in os.listdir(dir_path) if i not in ignored_items]
        
        # Sort so directories appear neatly or files are grouped alphabetically
        items.sort(key=lambda s: (not os.path.isdir(os.path.join(dir_path, s)), s.lower()))
    except Exception as e:
        print(f"{prefix}[Error reading directory: {e}]")
        return

    count = len(items)
    for i, item in enumerate(items):
        path = os.path.join(dir_path, item)
        is_last = (i == count - 1)
        
        # Select branch characters based on position
        connector = "└── " if is_last else "├── "
        
        # Format names: add a trailing slash to directories to explicitly show they are folders
        display_name = f"{item}/" if os.path.isdir(path) else item
        print(f"{prefix}{connector}{display_name}")
        
        # Recursively dive into folders
        if os.path.isdir(path):
            next_prefix = prefix + ("    " if is_last else "│   ")
            generate_tree(path, next_prefix, max_depth, current_depth + 1)

def main():
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "/?"]:
        print_usage()
        sys.exit(0)

    max_depth = None
    if len(sys.argv) > 1:
        try:
            max_depth = int(sys.argv[1])
        except ValueError:
            print(f"[-] Invalid depth argument: '{sys.argv[1]}'. Must be an integer.")
            print_usage()
            sys.exit(1)

    # Use the name of the current folder as the root anchor
    root_name = os.path.basename(os.getcwd()) or os.getcwd()
    print(f"{root_name}/")
    
    # Start tracing the tree elements
    generate_tree(os.getcwd(), max_depth=max_depth)

if __name__ == "__main__":
    main()
