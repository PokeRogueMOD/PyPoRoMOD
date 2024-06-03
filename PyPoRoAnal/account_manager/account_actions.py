from loguru import logger
from getpass import getpass

from ..utils import ExitCommandLoop, AccountDeleted
from ..poke_rogue.poke_rogue import PokeRogue


class AccountActions:
    def __init__(self, loop_manager):
        self._LOOP = loop_manager

        self.commands = {
            "0": self.cancel,
            "1": self.account_settings,
            "2": self.run_account_modder,
        }
        self.commands_settings = {
            "0": self.cancel,
            "1": self.account_settings_edit,
            "2": self.account_settings_delete,
        }

    def get_name_string(self):
        account = self._LOOP.context["selected_account"]
        anonymize = self._LOOP.context["anonymize"]
        username = account["username"]
        if anonymize:
            return f"<{username[:2]}...{username[-2:]}>"
        else:
            return f"<{username}>"

    def get_account_credentials(self):
        account = self._LOOP.context["selected_account"]
        return account["username"], account["password"]

    def command_generator(self):
        name_string = self.get_name_string()
        return [
            "╔═════════════════════════ ACCOUNT ACTIONS ════════════════════════╗",
           f"╠══ {name_string}",
            "╠══════════════════════════════════════════════════════════════════╣",
            "╠═ 0: Cancel.",
            "╠═ 1: Manage account.",
            "╠═ 2: Account Modding (P).",
            "╚══════════════════════════════════════════════════════════════════╝",
        ]

    def command_settings_generator(self):
        name_string = self.get_name_string()
        return [
            "╔════════════════════════ ACCOUNT SETTINGS ════════════════════════╗",
           f"╠══   {name_string}",
            "╠══════════════════════════════════════════════════════════════════╣",
            "╠═ 0: Cancel.",
            "╠═ 1: Edit account username and password.",
            "╠═ 2: Delete.",
            "╚══════════════════════════════════════════════════════════════════╝",
        ]

    def cancel(self):
        logger.info("Closing the account manager.")
        raise ExitCommandLoop

    def run_bot(self):
        logger.info("Bot not implemented yet.")
        return

    def run_account_modder(self):
        modder = PokeRogue(*self.get_account_credentials(), self.get_name_string())
        modder.run()
        return

    def account_settings(self):
        self.loop = self._LOOP.register_loop(
            self.command_settings_generator, self.commands_settings
        )

        try:
            self.loop.run()
        except AccountDeleted:
            logger.debug("Account was deleted, going back to main Menu.")
            raise ExitCommandLoop
        except ExitCommandLoop:
            logger.info("Closing the account settings.")

        self._LOOP.remove_loop(self.loop)

    def account_settings_edit(self):
        account = self._LOOP.context["selected_account"]
        new_username = input("Enter new username (leave blank to keep current): ")
        new_password = getpass("Enter new password (leave blank to keep current): ")

        if new_username:
            account["username"] = new_username
            self._LOOP.update_context("selected_account", account)

        if new_password:
            account["password"] = new_password

        logger.info("Account details updated.")
        self._LOOP.context["manager"].save_accounts()  # Save the updated accounts list

    def account_settings_delete(self):
        account = self._LOOP.context["selected_account"]
        name_string = self.get_name_string()
        confirm = input(
            f"Do you want to delete {name_string}? (1: Yes, 2: No)(number): "
        )

        if confirm == "1":
            self._LOOP.context["manager"].delete_account(account)
            logger.info("Account deleted.")
            raise AccountDeleted

    def run(self):
        self.loop = self._LOOP.register_loop(self.command_generator, self.commands)

        try:
            self.loop.run()
        except ExitCommandLoop:
            logger.info("Going back to main Menu.")

        self._LOOP.remove_loop(self.loop)
