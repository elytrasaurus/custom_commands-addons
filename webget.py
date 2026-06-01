# Downloads files from a URL while showing a live progress bar.
# /// script
# dependencies = []
# ///
import os
import sys
import urllib.request

def progress_callback(count, block_size, total_size):
    if total_size <= 0: return
    percent = min(100, int(count * block_size * 100 / total_size))
    sys.stdout.write(f"\rDownloading package... [{percent}%]")
    sys.stdout.flush()

def main():
    if len(sys.argv) < 2:
        print("Usage: webget <url> [custom_name]")
        sys.exit(1)
    url = sys.argv[1]
    output_name = sys.argv[2] if len(sys.argv) > 2 else url.split("/")[-1].split("?")[0]
    if not output_name: output_name = "download.bin"

    print(f"[+] Downloading: {url}")
    try:
        opener = urllib.request.build_opener()
        opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url, output_name, reporthook=progress_callback)
        print(f"\n[SUCCESS] Saved as '{output_name}'")
    except Exception as e:
        print(f"\n[-] Download failed: {e}")

if __name__ == "__main__":
    main()
