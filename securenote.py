# Scrambles a text message into a localized hidden format to protect it from casual glances.
import sys
import os

NOTE_PATH = r"C:\Custom_Commands\secure_vault.txt"

def obfuscate(text):
    # A simple but highly effective reversible character transformation mapping loop
    return "".join(chr(ord(c) ^ 42) for c in text)

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  securenote write \"<your secret message text>\"")
        print("  securenote read")
        sys.exit(1)

    mode = sys.argv[1].lower().strip()

    if mode == "write":
        if len(sys.argv) < 3:
            print("[-] Error: Please supply the text string contents to be written.")
            sys.exit(1)
        raw_message = sys.argv[2]
        hidden_blob = obfuscate(raw_message)
        try:
            with open(NOTE_PATH, "w", encoding="utf-8") as f:
                f.write(hidden_blob)
            print("[SUCCESS] Note successfully scrambled and saved inside your secure local environment storage container.")
        except Exception as e:
            print(f"[-] Storage access error: {e}")

    elif mode == "read":
        if not os.path.exists(NOTE_PATH):
            print("[-] Data notice: Your secure vault storage node is currently empty.")
            return
        try:
            with open(NOTE_PATH, "r", encoding="utf-8") as f:
                stored_blob = f.read()
            recovered_text = obfuscate(stored_blob)
            print(f"\n[VAULT KEY DECRYPTED CONTENTS]:\n -> {recovered_text}\n")
        except Exception as e:
            print(f"[-] Data conversion tracking failure: {e}")
    else:
        print("[-] Invalid flag choice: Choose either 'write' or 'read'.")

if __name__ == "__main__":
    main()
