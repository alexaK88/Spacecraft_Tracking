'''
EarthSatellite: Skyfield's object representing a satellite defined by a TLE
load: used to load time scales and planetary data
datetime: used to define UTC time (critical for orbit propagation)
'''

from skyfield.api import EarthSatellite, load
from datetime import datetime, timezone

# ISS:
    # these two strings encode the orbit at a specific epoch
    # Skyfield doesn't recompute orbital elements
    # it feeds them directly into SGP4
TLE_LINE1 = "1 25544U 98067A   26003.21020602  .00015578  00000-0  28954-3 0  9991"
TLE_LINE2 = "2 25544  51.6329  36.1624 0007549 334.7101  25.3517 15.49059586546183"

def propagate_satellite(tle1, tle2, timestamp):
    '''
    Function that takes TLE and time
    :param tle1:
    :param tle2:
    :param timestamp:
    :return: the satellite's state at time timestamp
    '''
    # -> load timescale <- :

    # Orbital propagation is time-sensitive down to milliseconds
    # Skyfield uses precise Earth time standards (UTC, TT, TAI)
    # This avoids common beginner errors with naive datetimes
    ts = load.timescale()

    # Skyfield parses the TLE, stores orbital elements and prepares an SGP4 propagator
    # no orbit is computed here yet!
    satellite = EarthSatellite(tle1, tle2, "SAT")

    # Python time -> Skyfield time
    # SGP4 needs time relative to the TLE epoch
    # Skyfield handles leap seconds and Earth rotation internally
    # datetime must be UTC
    t = ts.from_datetime(timestamp)

    # Orbit propagation
    # 1. SGP4 computes delta_t from TLE epoch
    # 2. SGP4 propagates the satelite forward
    # 3. Outputs position in an Earth-centered inertial frame (ECI)
    position = satellite.at(t)

    # Extract ECI coordinates - a 3D vector in kms relative to Earth's center
    geocentric = position.position.km
    # convert to Earth-fixed coordinates
    subpoint = position.subpoint()

    return {
        "eci_km": geocentric,
        "latitude_deg": subpoint.latitude.degrees,
        "longitude_deg": subpoint.longitude.degrees,
        "altitude_km": subpoint.elevation.km,
    }

if __name__ == "__main__":
    now = datetime.now(timezone.utc)

    # run propagation
    state = propagate_satellite(TLE_LINE1, TLE_LINE2, now)

    print(f"Time (UTC): {now.isoformat()}")
    print(f"ECI position (km): {state['eci_km']}")
    print(f"Lat: {state['latitude_deg']:.3f}°")
    print(f"Lon: {state['longitude_deg']:.3f}°")
    print(f"Alt: {state['altitude_km']:.2f} km")