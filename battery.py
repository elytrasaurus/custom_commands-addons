# Shows current laptop battery percentages, charging profiles, and design metrics.
import sys
import shutil

try:
    import psutil
except ImportError:
    # Handle environment check dynamically
    import subprocess
    subprocess.run(["pip", "install", "psutil"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    import psutil

def main():
    battery = psutil.sensors_battery()
    if not battery:
        print("[-] Hardware Notice: No battery architecture or tracking system located on this device hardware layout.")
        sys.exit(0)

    percent = battery.power_plugged
    seconds = battery.secsleft
    
    print("\n=== SYSTEM HARDWARE POWER SHELF ===")
    print(f" Current Charge Level : {battery.percent}%")
    print(f" Power State Status   : {'CONNECTED & CHARGING' if percent else 'DISCONNECTED / RUNNING ON BATTERY'}")
    
    if not percent:
        if seconds == psutil.POWER_TIME_UNKNOWN:
            print(" Estimated Time Left  : Calculating throughput parameters...")
        else:
            mins, secs = divmod(seconds, 60)
            hours, mins = divmod(mins, 60)
            print(f" Estimated Time Left  : {hours}h {mins}m remaining")
    else:
        print(" Estimated Time Left  : Infinite (Connected directly to power grid matrix)")
    print("===================================")

if __name__ == "__main__":
    main()
