from enum import Enum
import json
import random
import string
import time
import requests
import random
from urllib.parse import urljoin
from loguru import logger
from typing import Any, Dict, Optional

from .account_unlocker import AccountUnlocker
from PyPoRoMOD.enum import GameDataType


class LoginError(Exception):
    """Custom exception for login failures."""

    pass


class NewAccountError(Exception):
    """Custom exception for login failures."""

    pass


class PokeRogueAPI:
    """
    API client for interacting with the PokeRogue service.

    Source: https://github.com/pagefaultgames/pokerogue/blob/12bd22f2ca2204af125a4faab985c4d2b9017aea/src/utils.ts#L265
    """

    SESSION_ID_KEY = "pokerogue_sessionId"
    BASE_URL = "https://api.pokerogue.net"

    def __init__(
        self,
        username: str,
        password: str,
        is_local: bool = False,
        server_url: str = "http://localhost:8000",
    ):
        """
        Initializes the PokeRogueAPI client.

        Args:
            username (str): The username for authentication.
            password (str): The password for authentication.
            is_local (bool, optional): Whether to use a local server URL. Defaults to False.
            server_url (str, optional): The URL of the local server. Defaults to "http://localhost:8000".
        """
        self.api_url = server_url if is_local else self.BASE_URL
        self.session = requests.Session()
        self.username = username
        self.password = password
        self.headers = self._generate_random_headers()
        self.client_session_id = self.get_client_session_id()

        self.secret_id: Optional[str] = None
        self.trainer_id: Optional[str] = None
        self.last_session_slot: Optional[str] = -1

        self._login()

    @staticmethod
    def _generate_random_headers() -> Dict[str, str]:
        """
        Generates random headers for the session.

        Returns:
            Dict[str, str]: The generated headers.
        """
        chrome_major_versions = list(range(110, 126))
        sec_ch_ua_platform = ["Windows", "Macintosh", "X11"]
        platforms = [
            "Windows NT 10.0; Win64; x64",
            "Windows NT 6.1; Win64; x64",
            "Macintosh; Intel Mac OS X 10_15_7",
            "Macintosh; Intel Mac OS X 11_2_3",
            "X11; Linux x86_64",
            "X11; Ubuntu; Linux x86_64",
        ]

        random_platform = random.choice(platforms)
        random_sec_ch_ua_platform = random.choice(sec_ch_ua_platform)
        random_chrome_major_version = random.choice(chrome_major_versions)

        headers = {
            "Accept": "application/x-www-form-urlencoded",
            "Content-Type": "application/x-www-form-urlencoded",
            "Origin": "https://pokerogue.net",
            "Referer": "https://pokerogue.net/",
            "Sec-Ch-Ua": f'"Google Chrome";v="{random_chrome_major_version}", "Chromium";v="{random_chrome_major_version}", "Not.A/Brand";v="24"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": f'"{random_sec_ch_ua_platform}"',
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "User-Agent": f"Mozilla/5.0 ({random_platform}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random_chrome_major_version}.0.0.0 Safari/537.36",
        }

        return headers

    def _get_json_headers(self) -> None:
        """
        Sets the headers for the session.

        Args:
            headers (Dict[str, str]): The headers to set for the session.
        """
        json_headers = self.headers.copy()

        FLAG = "application/json"
        json_headers["Accept"] = FLAG
        json_headers["Content-Type"] = FLAG
        return json_headers

    @staticmethod
    def get_client_session_id(length=32, seeded=False):
        """Src: https://github.com/pagefaultgames/pokerogue/blob/20a3a4f60fe58a5fe929a51dff76a5db64080492/src/utils.ts#L9-L19"""
        characters = string.ascii_letters + string.digits
        result = []

        if seeded:
            # Create a seeded random number generator
            rng = random.Random()
            for i in range(length):
                random_index = rng.randint(0, len(characters) - 1)
                result.append(characters[random_index])
        else:
            for _ in range(length):
                random_index = random.randint(0, len(characters) - 1)
                result.append(characters[random_index])

        return "".join(result)

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Dict[str, Any] = {"datatype": GameDataType.SYSTEM.value},
        do_raise: bool = True,
        headers: bool = None,
    ) -> requests.Response:
        """
        Sends a request to the specified endpoint using the specified method.

        Args:
            method (str): The HTTP method to use (e.g., "get", "post").
            endpoint (str): The API endpoint to send the request to.
            data (Optional[Dict[str, Any]], optional): The form data to send in the request. Defaults to None.
            json (Optional[Dict[str, Any]], optional): The JSON data to send in the request. Defaults to None.
            params (Dict[str, Any], optional): The query parameters for the request. Defaults to {"datatype": 0}.

        Returns:
            requests.Response: The response from the API.
        """
        url = urljoin(self.api_url, endpoint)

        response = self.session.request(
            method,
            url,
            params=params,
            data=data if method != "get" else None,
            json=json if method != "get" else None,
            headers=(headers or self.headers),
        )

        if do_raise:
            response.raise_for_status()

        return response

    def get(
        self,
        endpoint: str,
        params: Dict[str, Any] = {"datatype": GameDataType.SYSTEM.value},
        do_raise: bool = True,
        headers: bool = None,
    ) -> requests.Response:
        """
        Sends a GET request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to.
            params (Dict[str, Any], optional): The query parameters for the request. Defaults to {"datatype": 0}.

        Returns:
            requests.Response: The response from the API.

        Src Code: https://github.com/pagefaultgames/pokerogue/blob/90aa9b42099a770fdbfca2dbfb94cc571b5032b7/src/utils.ts#L304-L317
        """
        return self._request(
            "get", endpoint, params=params, do_raise=do_raise, headers=headers
        )

    def post(
        self,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        params: Dict[str, Any] = {"datatype": GameDataType.SYSTEM.value},
        do_raise: bool = True,
        headers: bool = None,
    ) -> requests.Response:
        """
        Sends a POST request to the specified endpoint.

        Args:
            endpoint (str): The API endpoint to send the request to.
            data (Optional[Dict[str, Any]], optional): The form data to send in the request. Defaults to None.
            json (Optional[Dict[str, Any]], optional): The JSON data to send in the request. Defaults to None.
            params (Dict[str, Any], optional): The query parameters for the request. Defaults to {"datatype": 0}.

        Returns:
            requests.Response: The response from the API.

        Src Code: https://github.com/pagefaultgames/pokerogue/blob/90aa9b42099a770fdbfca2dbfb94cc571b5032b7/src/utils.ts#L319-L335
        """
        return self._request("post", endpoint, data, json, params, do_raise, headers)

    def _login(self) -> None:
        """
        Logs in to the PokeRogue API and sets the authorization header.

        Source: https://github.com/pagefaultgames/pokerogue/blob/50c1f8aee461a45d8f69de8f02a452a34b59f78b/src/ui/login-form-ui-handler.ts#L64
        """
        try:
            response = self.post(
                "account/login",
                data={"username": self.username, "password": self.password},
                params={},
            )
            logger.debug(response)

            self.headers["authorization"] = response.json()["token"]

            self.json_headers = self._get_json_headers()

        except Exception as e:
            logger.info("Couldn't Login! (Incorrect credentials or server down.)")
            logger.exception(e)
            raise LoginError()

    def _verify(self):
        try:
            # verify session?
            response = self.post(
                "savedata/system/verify",
                json={"clientSessionId": self.client_session_id},
                params={},
                headers=self.json_headers,
            )
            response.raise_for_status()
            return response.json()

        except Exception as e:
            logger.exception(e)

    def get_trainer(self) -> Optional[Dict[str, Any]]:
        """
        Retrieves trainer data from the API.

        Source: https://github.com/pagefaultgames/pokerogue/blob/3ef495c12688532d3b4e1c097bca3d3c5cea3b57/src/system/game-data.ts#L338

        Returns:
            Optional[Dict[str, Any]]: The trainer data, or None if an error occurs.
        """
        try:
            response_info = self.get(
                "account/info",
                do_raise=False,
                params={
                    "datatype": GameDataType.SYSTEM.value,
                    "clientSessionId": self.client_session_id,
                },
            )
            response_system = self.get(
                "savedata/system",
                do_raise=False,
                params={
                    "datatype": GameDataType.SYSTEM.value,
                    "clientSessionId": self.client_session_id,
                },
            )

            logger.debug(response_info)
            logger.debug(response_system)

            if response_system.status_code == 404:
                logger.info(
                    f"You need to atleast play a gamesave unil stage 2 for this tool to work!"
                )
                # Does not work (400 Client Error, data should be correct!)
                # trainer = AccountUnlocker.get_new_trainer()
                # self.set_new_trainer(trainer)
                raise NewAccountError()
            else:
                trainer: dict = response_system.json()

            info: dict = response_info.json()

            logger.debug("Trainer data data downloaded.")

            self.trainer_id = trainer["trainerId"]
            self.secret_id = trainer["secretId"]
            self.last_session_slot = info["lastSessionSlot"]

            logger.debug(
                f"[{self.trainer_id = }] & [{self.secret_id = }] & [{self.last_session_slot = }]"
            )

            return trainer

        except NewAccountError:
            raise NewAccountError()
        except Exception as e:
            logger.exception(e)
            return None

    def set_trainer(self, trainer: Dict[str, Any], parent) -> bool:
        """
        Updates trainer data on the API.

        Source:
            - https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/common.go#L56
            - https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/endpoints.go#L410
            - https://github.com/pagefaultgames/pokerogue/blob/20a3a4f60fe58a5fe929a51dff76a5db64080492/src/system/game-data.ts#L302

        Args:
            trainer (Dict[str, Any]): The trainer data to update.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            verify = self._verify()
            if verify.get("valid", False):
                trainer["timestamp"] = int(time.time() * 1000)
                # session = parent.slots[self.last_session_slot]
                # new_data = {
                #     "system": trainer,
                #     "session": session,
                #     "sessionSlotId": self.last_session_slot,
                #     "clientSessionId": self.client_session_id,
                # }
                # response = self.post(
                #     "savedata/updateall",
                #     json=new_data,
                #     params={},
                #     headers=self.json_headers,
                # )

                response = self.post(
                    "savedata/update",
                    json=trainer,
                    params={
                        "datatype": GameDataType.SYSTEM.value,
                        "clientSessionId": self.client_session_id,
                    },
                    headers=self.json_headers,
                )
                logger.debug(response)

                is_success = response.status_code == 200

                if is_success:
                    logger.debug(f"Trainer data uploaded.")
                else:
                    logger.debug(f"Couldn't upload trainer data.")

                return is_success
            else:
                logger.info("Session not valid.")

        except Exception as e:
            logger.exception(e)
            return False

    def set_new_trainer(self, trainer: str) -> bool:
        """
        Updates trainer data on the API.

        Source:
            - https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/common.go#L56
            - https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/endpoints.go#L410
            - https://github.com/pagefaultgames/pokerogue/blob/20a3a4f60fe58a5fe929a51dff76a5db64080492/src/system/game-data.ts#L302

        Args:
            trainer (Dict[str, Any]): The trainer data to update.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            self._verify()
            response = self.post(
                "savedata/update",
                json=trainer,
                params={
                    "datatype": GameDataType.SYSTEM.value,
                    "clientSessionId": self.client_session_id,
                },
                headers=self.headers,
            )
            logger.debug(response)

            is_success = response.status_code == 200

            if is_success:
                logger.debug(f"New Trainer data set.")
            else:
                logger.debug(f"Couldn't set new trainer data.")

            return is_success

        except Exception as e:
            logger.exception(e)
            return False

    def get_slot(self, slot_index: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves data for a specific slot from the API.

        Source: https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/common.go#L55

        Args:
            slot_index (int): The index of the slot to retrieve data for.

        Returns:
            Optional[Dict[str, Any]]: The slot data, or None if an error occurs.
        """
        try:
            response = self.get(
                "savedata/session",
                params={
                    "datatype": GameDataType.SESSION.value,
                    "clientSessionId": self.client_session_id,
                    "slot": slot_index,
                },
                do_raise=False,
            )
            logger.debug(response)

            if response.status_code == 404:
                return None

            slot: dict = response.json()

            if slot:
                logger.debug(f"Slot [{slot_index + 1}] data downloaded.")
            else:
                logger.debug(f"Couldn't download slot [{slot_index + 1}] data.")

            return slot

        except Exception as e:
            logger.exception(e)
            return None

    def set_slot(self, slot_index: int, data: Dict[str, Any]) -> bool:
        """
        Updates data for a specific slot on the API.

        Source: https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/common.go#L56
        https://github.com/pagefaultgames/rogueserver/blob/68caa148f6a965f01ea503d42f56daad6799e5f7/api/endpoints.go#L410

        Args:
            slot_index (int): The index of the slot to update.
            data (Dict[str, Any]): The data to update for the slot.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            if self.trainer_id is None or self.secret_id is None:
                # To update the trainer and secret id.
                self.get_trainer()

            response = self.post(
                "savedata/update",
                json=data,
                params={
                    "datatype": GameDataType.SESSION.value,
                    "slot": slot_index,
                    "clientSessionId": self.client_session_id,
                    "trainerId": self.trainer_id,
                    "secretId": self.secret_id,
                },
                headers=self.json_headers,
            )
            logger.debug(response)

            is_success = response.status_code == 200

            if is_success:
                logger.debug(f"Slot [{slot_index + 1}] data uploaded.")
            else:
                logger.warning(f"Couldn't upload slot [{slot_index + 1}] data.")

            return is_success

        except Exception as e:
            logger.exception(e)
            return False

    @classmethod
    def create_account(cls, username: str, password: str) -> bool:
        """
        Updates data for a specific slot on the API.

        Source: https://github.com/pagefaultgames/pokerogue/blob/12bd22f2ca2204af125a4faab985c4d2b9017aea/src/ui/registration-form-ui-handler.ts#L81

        Args:
            slot_index (int): The index of the slot to update.
            data (Dict[str, Any]): The data to update for the slot.

        Returns:
            bool: True if the update is successful, False otherwise.
        """
        try:
            response = requests.post(
                urljoin(cls.BASE_URL, "account/register"),
                data={"username": username, "password": password},
                headers=cls._generate_random_headers(),
            )
            logger.debug(response)

            response.raise_for_status()

            is_success = response.status_code == 200

            if is_success:
                logger.debug(f"Created account.")
            else:
                logger.warning(f"Couldn't created account.")

            return is_success

        except Exception as e:
            logger.exception(e)
            return False

    def close(self) -> None:
        """
        Closes the session and clears the instance attributes.
        """
        self.session.close()
        self.session = None
        self.secret_id = None
        self.trainer_id = None
        self.last_session_slot = None
        self.api_url = None
        self.username = None
        self.password = None
        self.headers = None
