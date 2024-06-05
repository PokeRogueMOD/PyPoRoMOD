from loguru import logger


class ExitCommandLoop(Exception):
    """Custom exception to break the command loop."""

    pass


class AccountDeleted(Exception):
    """Custom exception to break the command loop."""

    pass


class CommandLoop:
    """
    Class to handle a loop that prompts the user for commands and executes corresponding functions.
    """

    def __init__(self, command_generator, functions: dict, ignore_delete: bool = False):
        """
        Initializes the CommandLoop instance.

        Parameters:
        command_generator (callable): A callable that generates the list of strings to be displayed.
        functions (dict): A dictionary mapping command strings to their corresponding functions.
        ignore_delete (bool): Flag to ignore AccountDeleted exception if set to True.
        """
        self.command_generator = command_generator
        self.functions = functions
        self.ignore_delete = ignore_delete

    def update_commands(
        self, command_generator: callable = None, functions: dict = None
    ):
        """
        Updates the command lines and functions.

        Parameters:
        command_generator (callable): A new callable that generates the list of strings to be displayed.
        functions (dict): A new dictionary mapping command strings to their corresponding functions.
        """
        if command_generator is not None:
            self.command_generator = command_generator
        if functions is not None:
            self.functions = functions

    def run(self):
        """
        Runs the command loop, prompting the user for commands and executing the corresponding functions.
        """
        nl = "\n"
        while True:
            command_lines = self.command_generator()
            logger.info(f"{nl}{nl.join(command_lines)}")
            command = input("Command: ")
            try:
                if command in self.functions:
                    self.functions[command]()
                else:
                    logger.info("Command not found!")
            except ExitCommandLoop:
                logger.debug("Exiting the command loop. (ExitCommandLoop)")
                break
            except AccountDeleted:
                logger.debug("Exiting the command loop. (AccountDeleted)")
                if not self.ignore_delete:
                    raise


class LoopManager:
    """
    Class to manage multiple command loops and maintain the application context.
    """

    def __init__(self):
        self.context = {
            "selected_account": None,
            "selected_account_str": None,
            "accounts": [],
            "anonymize": False,
        }
        self.command_loops = []

    def update_context(self, key, value):
        self.context[key] = value
        self.update_all_loops()

    def update_all_loops(self):
        for loop in self.command_loops:
            loop.update_commands(
                command_generator=loop.command_generator, functions=loop.functions
            )

    def register_loop(self, command_generator, functions):
        loop = CommandLoop(command_generator, functions)
        self.command_loops.append(loop)
        return loop

    def remove_loop(self, loop):
        if loop in self.command_loops:
            self.command_loops.remove(loop)

    def run_all_loops(self):
        for loop in self.command_loops:
            loop.run()
