from spacetrack_client import SpaceTrackClient
from catalog import build_catalog
from user_selection import search_for_spacecraft
from tle_tracker import propagate_satellite
from datetime import datetime, timezone


USERNAME = "alesksandrak@gmail.com"
PASSWORD = ""

def main():
    client = SpaceTrackClient(USERNAME, PASSWORD)

    print("Fetching spacecraft catalog...")
    raw_catalog = client.get_active_payloads(limit=1000)
    catalog = build_catalog(raw_catalog)

    print(f"{len(catalog)} spacecraft loaded.\n")

    query = input("Type spacecraft name (partial is OK): ")

    matches = search_for_spacecraft(catalog, query)

    if not matches:
        print("No spacecraft found.")
        return

    print("\nMatches:")
    for i, sat in enumerate(matches[:10]):
        print(f"[{i}] {sat['name']} (NORAD {sat['norad_id']})")

    choice = int(input("\nSelect spacecraft number: "))
    selected = matches[choice]

    print(f"\nSelected: {selected['name']}")

    tle1, tle2 = client.get_latest_tle(selected["norad_id"])

    state = propagate_satellite(
        tle1,
        tle2,
        datetime.now(timezone.utc)
    )

    print("\nCurrent State:")
    print(f"Latitude:  {state['latitude_deg']:.3f}°")
    print(f"Longitude: {state['longitude_deg']:.3f}°")
    print(f"Altitude:  {state['altitude_km']:.2f} km")


if __name__ == "__main__":
    main()

