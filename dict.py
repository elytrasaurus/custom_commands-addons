# Connects to a free open API dictionary to look up lexical syntax, meanings, and word types.
import sys
import json
import urllib.request

def main():
    if len(sys.argv) < 2:
        print("Usage: dict <english_word>")
        sys.exit(1)

    word = sys.argv[1].lower().strip()
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    print(f"[+] Querying global vocabulary dictionary maps for: '{word}'...\n")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))

        entry = data[0]
        print(f"📖 WORD      : {entry['word'].upper()}")
        if "phonetic" in entry:
            print(f"🔊 PHONETIC  : {entry['phonetic']}")

        for meaning in entry.get("meanings", []):
            part = meaning.get("partOfSpeech", "unknown")
            print(f"\n[{part.upper()}]")
            for idx, definition in enumerate(meaning.get("definitions", []), 1):
                print(f"  {idx}. {definition.get('definition')}")
                if "example" in definition:
                    print(f"     * Example: \"{definition.get('example')}\"")
                if idx >= 3: # Limit layout spillover blocks to top 3 matching meanings
                    break
        print("")
    except Exception:
        print(f"[-] Data check error: The vocabulary catalog cannot find a match for '{word}'.")

if __name__ == "__main__":
    main()
