import requests
from typing import Tuple

BASE_URL = "https://www.space-track.org"

class SpaceTrackClient:
    def __init__(self, username: str, password: str):
        self.session = requests.Session()
        self._login(username, password)

    def _login(self, username: str, password: str):
        login_url = f"{BASE_URL}/ajaxauth/login"
        payload = {
            "identity": username,
            "password": password,
        }

        response = self.session.post(login_url, data=payload)
        response.raise_for_status()

        cookies = self.session.cookies.get_dict()

        if not cookies:
            raise RuntimeError(f"Login failed for {username}"
                               f"Response preview: {response.text[:200]}")

    def get_latest_tle(self, norad_id: int) -> Tuple[str, str]:
        """
        Fetch latest TLE for a given NORAD catalog ID
        """
        url = (
            f"{BASE_URL}/basicspacedata/query/"
            f"class/tle/"
            f"NORAD_CAT_ID/{norad_id}/"
            f"orderby/EPOCH desc/"
            f"limit/1/"
            f"format/tle"
        )

        response = self.session.get(url)
        response.raise_for_status()

        lines = [l.strip() for l in response.text.splitlines() if l.strip()]

        if len(lines) < 2:
            raise ValueError("Invalid TLE response. Response was:\n{response.text[:300]")

        return lines[0], lines[1]