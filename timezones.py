# Displays current live timestamps from configured global metropolitan standard time matrices.
import datetime

def get_utc_offset_time(offset_hours):
    # Calculates explicit offset paths cleanly without forcing heavy external module imports
    utc = datetime.datetime.now(datetime.timezone.utc)
    return utc + datetime.timedelta(hours=offset_hours)

def main():
    # Pre-configured key urban target locations and their structural standard offsets from UTC
    CITIES = {
        "LOS ANGELES (PST) ": -8,
        "NEW YORK    (EST) ": -5,
        "LONDON      (GMT) ": 0,
        "PARIS       (CET) ": 1,
        "TOKYO       (JST) ": 9,
        "SYDNEY      (AEST)": 10
    }

    print("\n=== GLOBAL CLOCK SYNCHRONIZATION BOARD ===")
    for city, offset in CITIES.items():
        city_time = get_utc_offset_time(offset)
        formatted_stamp = city_time.strftime("%Y-%m-%d  |  %I:%M:%S %p")
        print(f" -> {city} : {formatted_stamp}")
    print("==========================================\n")

if __name__ == "__main__":
    main()
