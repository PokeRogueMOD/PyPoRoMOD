from loguru import logger
from PyPoRoAnal.api.poke_rogue_api import PokeRogueAPI


class PokeRogue:
    def __init__(self, username: str, password: str, display_name: str) -> None:
        self.username = username
        self.password = password
        self.display_name = display_name
        self.api = PokeRogueAPI(self.username, self.password)
        
    def run(self):
        # I need a function to check if the starter pokemon are still the default
        # and if there is no game slot, the account is still locked
        # In this case i want a prompt and a function to unlock the account
        # (By adding a new game save with a random starter pokemon)
        # First hardcoeded, then play to wave 2 or 3 so i can unlock all)
        
        # Use only classes and code based on source code to generate a perfect trainer dex
        # Use the defined JSnumbers for automatic clamping to prevent not savable trainer data
        
        # Add Gamesave modder, to add items, edit luck, enemys and everything what you can edit
        # Check how to set the gamesave to a specific wave by generating new enemy data based on the seed
        # and a function to roll back the wave to a earlier
        
        # Later save all the trainer and slot data into a db, so you can store different account versions
        # And backup the original account data, so if a user dont likes the result, he can just rollback the account to the
        # original saved version.
        logger.info("Not implemented yet, comming soon...")
