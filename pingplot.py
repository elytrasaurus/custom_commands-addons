# Pings a stable server once per second and draws a real-time graph to track connection spikes.
import os
import sys
import time
import subprocess
import re

def get_ping_time(host):
    # Cross-platform ping invocation profile
    cmd = ["ping", "-n", "1", "-w", "1000", host]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if proc.returncode != 0:
        return None
    # Parse milliseconds using regex matching patterns
    match = re.search(r"time[<=](\d+)ms", proc.stdout)
    return int(match.group(1)) if match else None

def main():
    target_host = sys.argv[1] if len(sys.argv) > 1 else "1.1.1.1"
    print(f"[+] Monitoring real-time line stability map for: {target_host}")
    print("[+] Press Ctrl+C inside your execution layout window to drop tracing and return home.\n")

    try:
        while True:
            ms = get_ping_time(target_host)
            if ms is None:
                print(f" {time.strftime('%H:%M:%S')} | [-] TIMEOUT OR PACKET LOSS ENCOUNTERED")
            else:
                # Generate a small adaptive textual bar graph based on response speed scales
                bars = "█" * min(ms // 10, 50)
                if not bars:
                    bars = "▏"
                print(f" {time.strftime('%H:%M:%S')} | {ms:>3} ms | {bars}")
            time.sleep(1.0)
    except KeyboardInterrupt:
        print("\n[+] Session closed successfully. Pipeline cleared.")

if __name__ == "__main__":
    main()
