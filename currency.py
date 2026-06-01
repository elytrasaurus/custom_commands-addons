# Fetches open-source economic asset tables to evaluate direct trading value exchanges.
import sys
import json
import urllib.request

def main():
    if len(sys.argv) < 4:
        print("Usage: currency <amount> <from_currency> <to_currency>")
        print("Example: currency 100 USD EUR")
        sys.exit(1)

    try:
        amount = float(sys.argv[1])
    except ValueError:
        print("[-] Error: Numerical amount parameter string could not be parsed.")
        sys.exit(1)

    base = sys.argv[2].upper().strip()
    target = sys.argv[3].upper().strip()

    # Using a free, reliable, registration-free exchange engine fallback URL
    url = f"https://open.er-api.com/v6/latest/{base}"
    print(f"[+] Syncing financial asset valuations against {base} trading metrics...\n")

    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as res:
            data = json.loads(res.read().decode('utf-8'))

        if data.get("result") == "error":
            print(f"[-] Evaluation Error: Currency token identifier base '{base}' is invalid.")
            return

        rates = data.get("rates", {})
        if target not in rates:
            print(f"[-] Evaluation Error: Currency destination identifier label '{target}' is invalid.")
            return

        exchange_multiplier = rates[target]
        final_calculation = amount * exchange_multiplier

        print("==============================================")
        print(f" STARTING SUM   : {amount:,.2f} {base}")
        print(f" CONVERSION RATE: 1 {base} = {exchange_multiplier:.4f} {target}")
        print("----------------------------------------------")
        print(f" EXCHANGE VALUE : {final_calculation:,.2f} {target}")
        print("==============================================")

    except Exception as e:
        print(f"[-] Network transaction failure checking trade matrices: {e}")

if __name__ == "__main__":
    main()
