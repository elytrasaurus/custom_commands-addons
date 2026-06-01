# Watches your memory usage.
# /// script
# dependencies = ["psutil"]
# ///
import os
import sys
import time
import psutil

def get_bar(percent, width=20):
    filled = int(width * percent / 100)
    return "█" * filled + "░" * (width - filled)

def main():
    print("Starting Live System Watcher... Press Ctrl+C to exit.")
    time.sleep(1)
    try:
        while True:
            os.system('cls' if os.name == 'nt' else 'clear')
            cpu = psutil.cpu_percent(interval=None)
            ram = psutil.virtual_memory()
            
            print("==================================================")
            print("         LIVE SYSTEM HARDWARE WATCHER             ")
            print("==================================================")
            print(f" CPU Usage: [{get_bar(cpu)}] {cpu}%")
            print(f" RAM Usage: [{get_bar(ram.percent)}] {ram.percent}%")
            print("--------------------------------------------------")
            print(f" {'PID':<8} {'Process Name':<25} {'Memory':<15}")
            print("--------------------------------------------------")
            
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    processes.append(proc.info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            processes.sort(key=lambda x: x['memory_info'].rss if x['memory_info'] else 0, reverse=True)
            for p in processes[:5]:
                mem_mb = (p['memory_info'].rss // (1024**2)) if p['memory_info'] else 0
                print(f" {p['pid']:<8} {str(p['name']):<25} {mem_mb:<5} MB")
            print("==================================================")
            time.sleep(1.5)
    except KeyboardInterrupt:
        print("\nExiting cleanly.")
        sys.exit(0)

if __name__ == "__main__":
    main()
