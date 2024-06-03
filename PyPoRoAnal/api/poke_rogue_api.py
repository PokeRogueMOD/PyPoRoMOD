import json
import requests
import random
from urllib.parse import urljoin
from loguru import logger


class LoginError(Exception):
    """Custom exception for login failures."""

    pass


class PokeRogueAPI:
    BASE_URL = "https://api.pokerogue.net"

    def __init__(
        self, username, password, is_local=False, server_url="http://localhost:8000"
    ):
        self.api_url = server_url if is_local else self.BASE_URL
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.headers = self.generate_random_headers()

        self._login()

    def get(self, endpoint, data=None):
        return self._request("get", endpoint, data=data)

    def post(self, endpoint, data=None):
        return self._request("post", endpoint, data=data)

    def put(self, endpoint, data=None):
        return self._request("put", endpoint, data=data)

    def delete(self, endpoint, data=None):
        return self._request("delete", endpoint, data=data)

    def _request(self, method, endpoint, data=None):
        url = urljoin(self.api_url, endpoint)
        response = self.session.request(
            method,
            url,
            params={"datatype": 0},
            data=data if method != "get" else None,
            headers=self.headers,
        )
        response.raise_for_status()
        return response

    def set_headers(self, headers):
        self.session.headers.update(headers)

    def close(self):
        self.session.close()

    def generate_random_headers(self):
        chrome_major_versions = list(range(110, 126))
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 6.1; Win64; x64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Ubuntu; Linux x86_64",
        ]

        random_platform = random.choice(platforms)
        random_chrome_major_version = random.choice(chrome_major_versions)

        headers = {
            "Accept": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://pokerogue.net/",
            "Sec-Ch-Ua": f'"Google Chrome";v="{random_chrome_major_version}", "Chromium";v="{random_chrome_major_version}", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": random_platform.split(";")[0],
            "User-Agent": f"Mozilla/5.0 ({random_platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random_chrome_major_version}.0.0.0 Safari/537.36",
        }

        return headers

    def _login(self):
        """
        Src: https://github.com/pagefaultgames/pokerogue/blob/50c1f8aee461a45d8f69de8f02a452a34b59f78b/src/ui/login-form-ui-handler.ts#L64
        """
        try:
            response = self.post(
                "account/login", {"username": self.username, "password": self.password}
            )
            self.headers["authorization"] = response.json()["token"]

        except Exception as e:
            logger.info("Could't Login! (Incorrect credentials or server down.)")
            logger.exception(e)
            raise LoginError()

    def get_trainer(self):
        """
        Src: https://github.com/pagefaultgames/pokerogue/blob/50c1f8aee461a45d8f69de8f02a452a34b59f78b/src/system/game-data.ts#L301
        """
        try:
            return self.get("savedata/get").json()

        except Exception as e:
            logger.exception(e)

    def set_trainer(self, trainer):
        """
        Src: https://github.com/pagefaultgames/pokerogue/blob/50c1f8aee461a45d8f69de8f02a452a34b59f78b/src/system/game-data.ts#L301
        """
        try:
            return self.post("savedata/update", json.dumps(trainer)).status_code == 200

        except Exception as e:
            logger.exception(e)
            return False
