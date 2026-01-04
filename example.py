from spacetrack_client import SpaceTrackClient

USERNAME = "alesksandrak@gmail.com"
PASSWORD = "jxAU5m6.AcYxEV8"

client = SpaceTrackClient(USERNAME, PASSWORD)

tle1, tle2 = client.get_latest_tle(25544)

print(tle1)
print(tle2)
