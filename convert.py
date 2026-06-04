# Converts files
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "pillow",
# ]
# ///

import os
import sys
from PIL import Image

def print_usage():
    print("Custom Commands Converter Utility")
    print("Usage:  convert <input_file> <target_format>")
    print("Examples:")
    print("  convert image.png jpg")
    print("  convert photo.jpg ico")
    print("  convert icon.png png  (Can be used to re-save/optimize)")

def convert_image(input_path, target_ext):
    if not os.path.exists(input_path):
        print(f"Error: File '{input_path}' not found.")
        return False

    # Normalize extension format
    target_ext = target_ext.lower().replace(".", "")
    
    # Split the original path to keep the same file name
    base_path, _ = os.path.splitext(input_path)
    output_path = f"{base_path}.{target_ext}"

    try:
        print(f"Opening {input_path}...")
        with Image.open(input_path) as img:
            # Handle transparency issues when converting PNG to JPG
            if target_ext in ["jpg", "jpeg"] and img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            
            print(f"Converting and saving to {output_path}...")
            img.save(output_path)
            print("Conversion successful!")
            return True
    except Exception as e:
        print(f"Conversion failed: {e}")
        return False

def main():
    if len(sys.argv) < 3:
        print_usage()
        sys.exit(1)

    input_file = sys.argv[1]
    target_format = sys.argv[2]
    
    # Basic router based on file extension
    _, ext = os.path.splitext(input_file.lower())
    
    image_extensions = ['.png', '.jpg', '.jpeg', '.bmp', '.webp', '.ico']
    
    if ext in image_extensions:
        success = convert_image(input_file, target_format)
        sys.exit(0 if success else 1)
    else:
        print(f"Unsupported input file type: {ext}")
        print("Currently supported input types: PNG, JPG, JPEG, BMP, WEBP, ICO")
        sys.exit(1)

if __name__ == "__main__":
    main()
