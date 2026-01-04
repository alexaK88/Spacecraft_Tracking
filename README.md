What it should do:
1. Load TLE (Two-Line Element - a compact data format describing the orbit of an Earth-orbiting object for predicting its future position)
2. Propagate the orbit to a given time
3. Output position, latitude, longitude, altitude
4. Check visibility from a ground station

#### Notes for reference
- TLE = compressed orbit snapshot - we know this, we know the future
- SGP4 = physics-based predictor
- Skyfield = time + coordinate conversions
