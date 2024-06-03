import json
from pathlib import Path
from getpass import getpass
from loguru import logger

from .account_actions import AccountActions
from PyPoRoAnal.utils import LoopManager, ExitCommandLoop
from PyPoRoAnal.api.poke_rogue_api import PokeRogueAPI


class AccountManager:
    _LOOP = LoopManager()

    # System Paths
    _DIR_ = Path(__file__).resolve().parent
    _ROOT_ = _DIR_.parent.parent
    _ACCOUNTS_ = _ROOT_ / "accounts"
    _CREDENTIALS_ = _ACCOUNTS_ / "credentials"

    def __init__(self):
        # Ensure the accounts folder exists
        self._CREDENTIALS_.mkdir(parents=True, exist_ok=True)

        self.accounts_file = self._CREDENTIALS_ / "accounts.json"
        self.settings_file = self._CREDENTIALS_ / "settings.json"

        self.accounts = self.load_accounts()
        self.settings = self.load_settings()

        self._LOOP.update_context("accounts", self.accounts)
        self._LOOP.update_context("anonymize", self.settings.get("anonymize", False))
        self._LOOP.update_context("manager", self)

    def load_accounts(self):
        if self.accounts_file.exists():
            with self.accounts_file.open("r") as file:
                return json.load(file).get("accounts", [])
        return []

    def save_accounts(self):
        with self.accounts_file.open("w") as file:
            json.dump({"accounts": self.accounts}, file, indent=4)

    def load_settings(self):
        if self.settings_file.exists():
            with self.settings_file.open("r") as file:
                return json.load(file)
        else:
            return {"anonymize": False}

    def save_settings(self):
        with self.settings_file.open("w") as file:
            json.dump(self.settings, file, indent=4)

    def add_account(self):
        username = input("Enter username: ")
        password = getpass("Enter password (input hidden): ")
        self.accounts.append({"username": username, "password": password})
        self._LOOP.update_context("accounts", self.accounts)
        self.save_accounts()
        logger.info(f"Account for {username} added successfully.")
        self.run()  # Re-register the loop after adding an account

    def delete_account(self, account):
        self.accounts = [acc for acc in self.accounts if acc != account]
        self._LOOP.update_context("accounts", self.accounts)
        self.save_accounts()
        logger.info(f"Account for {account['username']} deleted successfully.")

    def get_display_name(self, name):
        if self.settings["anonymize"]:
            return f"<{name[:2]}...{name[-2:]}>"
        else:
            return f"<{name}>"

    def display_accounts(self):
        return [
            f"Select {self.get_display_name(a['username'])}." for a in self.accounts
        ]

    def toggle_anonymize(self):
        self.settings["anonymize"] = not self.settings["anonymize"]
        self._LOOP.update_context("anonymize", self.settings["anonymize"])
        self.save_settings()
        logger.info(f"Anonymize setting is now set to {self.settings['anonymize']}.")

    def select_account(self, account_index):
        account = self.accounts[account_index]
        self._LOOP.update_context("selected_account", account)
        AccountActions(self._LOOP).run()

    def register_account(self):
        username = input("Enter username: ")
        password = getpass("Enter password (input hidden): ")
        try:
            was_created = PokeRogueAPI.create_account(username, password)
        except Exception as e:
            logger.exception(e)
            was_created = False
            
        if was_created:
            self.accounts.append({"username": username, "password": password})
            self._LOOP.update_context("accounts", self.accounts)
            self.save_accounts()
            logger.info(f"Account for {username} created and added successfully.")
            self.run()  # Re-register the loop after adding an account
        else:
            logger.info(f"Could not create {username}.")
            

    def close_manager(self):
        logger.debug("Closing Account Manager.")
        raise ExitCommandLoop()

    def command_generator(self):
        cmds = [
            "╔═════════════════════════ ACCOUNT MANAGER COMMANDS ════════════════════════╗",
            "╠═ 0: Close.                                                                ║",
            "╠═ 1: Toggle anonymize account names.                                       ║",
            "╠═ 2: Add account.                                                          ║",
            "╠═ 3: Register PokeRogue account.                                           ║",
            "╠═══════════════════════════════════════════════════════════════════════════╣"
        ]
        account_cmds = self.display_accounts()
        for i, cmd in enumerate(account_cmds, start=4):
            cmds.append(f"╠═ {i}: {cmd}")
        cmds.append(
            "╚═══════════════════════════════════════════════════════════════════════════╝"
        )
        return cmds

    def run(self):
        def generate_commands():
            cmds = {
                "0": self.close_manager,
                "1": self.toggle_anonymize,
                "2": self.add_account,
                "3": self.register_account,
            }
            for i in range(4, 4 + len(self.accounts)):
                cmds[str(i)] = lambda idx=i: self.select_account(idx - 4)
            return cmds

        loop = self._LOOP.register_loop(self.command_generator, generate_commands())

        try:
            loop.run()
        except ExitCommandLoop:
            logger.debug("Account Manager `ExitCommandLoop` received, exiting.")
        except KeyboardInterrupt:
            logger.debug("Account Manager `KeyboardInterrupt` received, exiting.")
            exit()

        self._LOOP.remove_loop(loop)
        logger.info("Closed Account Manager.")
