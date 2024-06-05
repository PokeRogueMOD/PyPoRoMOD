import random
from loguru import logger
from PyPoRoMOD.api.poke_rogue_api import PokeRogueAPI
from PyPoRoMOD.data_types.js_big_int import JSBigInt
from PyPoRoMOD.data_types.js_int import JSInt
from PyPoRoMOD.utils import ExitCommandLoop

from .mod import EggTier, GachaType, generate_eggs


class PokeRogue:
    NO_PASSIVE = [
        "25",
        "35",
        "39",
        "106",
        "107",
        "113",
        "122",
        "124",
        "125",
        "126",
        "143",
        "183",
        "185",
        "202",
        "226",
        "315",
        "358",
        "4122",
    ]

    username = None
    password = None
    display_name = None
    api = None
    trainer = None
    slots = None

    def __init__(self, username: str, password: str, display_name: str) -> None:
        self.username = username
        self.password = password
        self.display_name = display_name
        self.api = PokeRogueAPI(self.username, self.password)
        self.trainer = self.api.get_trainer()
        self.slots = {s: self.api.get_trainer(s) for s in range(5)}

        logger.info(f"Logged in <{self.display_name}> successfully.")

    def close(self):
        logger.debug("Stopping RogueEditor.")
        raise ExitCommandLoop

    def generate_eggs(self, upload=True):
        """Generate eggs by using user inputs."""
        try:
            egg_len = len(self.trainer.get("eggs", []))

            if egg_len >= 75:
                replace_or_add = input(
                    f"You have [75 (max)] eggs, replace eggs? (0: Cancel, 1: Replace): "
                )
                if replace_or_add == "2":
                    replace_or_add = "1"
            else:
                replace_or_add = input(
                    f"You have [{egg_len}] eggs, add or replace eggs? (0: Cancel, 1: Replace, 2: Add): "
                )

            if replace_or_add not in ["1", "2"]:
                raise ValueError("Invalid replace_or_add selected!")

            max_count = 75 - egg_len if replace_or_add == "2" else 75

            count = int(
                input(f"How many eggs do you want to have? (0 - {max_count})(number): ")
            )

            tier = input(
                "What tier should the eggs have? (1: Common, 2: Rare, 3: Epic, 4: Legendary, 5: Manaphy): "
            )

            # Generatate fake eggs
            match tier:
                case "1":
                    tier = EggTier.COMMON
                case "2":
                    tier = EggTier.RARE
                case "3":
                    tier = EggTier.EPIC
                case "4":
                    tier = EggTier.LEGENDARY
                case "5":
                    tier = EggTier.MANAPHY
                case _:
                    raise ValueError("Invalid tier selected!")

            gacha_type = input(
                "What gacha type do you want to have? (1: Move, 2: Legendary, 3: Shiny): "
            )
            match gacha_type:
                case "1":
                    gacha_type = GachaType.MOVE
                case "2":
                    gacha_type = GachaType.LEGENDARY
                case "3":
                    gacha_type = GachaType.SHINY
                case _:
                    raise ValueError("Invalid gacha_type selected!")

            hatch_waves = int(
                input("After how many waves should they hatch? (0-100)(number): ")
            )

            egg_generator = generate_eggs(tier, gacha_type, hatch_waves)
            new_eggs = [next(egg_generator) for _ in range(count)]

            match replace_or_add:
                case "1":
                    self.trainer["eggs"] = new_eggs
                case "2":
                    if "eggs" not in self.trainer:
                        self.trainer["eggs"] = []

                    self.trainer["eggs"].extend(new_eggs)

            if upload:
                self.api.set_trainer(self.trainer)

            logger.info(f"[{count}] eggs got generated.")

        except Exception as e:
            logger.exception(e)

    def set_hatch_waves_to_zero(self, upload=True):
        try:
            if "eggs" not in self.trainer or len(self.trainer["eggs"]) == 0:
                logger.info("No eggs to hatch.")
                return

            for egg in self.trainer["eggs"]:
                egg["hatchWaves"] = 0

            if upload:
                self.api.set_trainer(self.trainer)

            logger.info("All eggs will hatch after the next battle.")

        except Exception as e:
            logger.exception(e)

    def mod_starters(self, upload=True):
        try:
            dex_data = self.trainer["dexData"]
            starter_data = self.trainer["starterData"]
            game_stats = self.trainer["gameStats"]
            total_hatched = 0
            total_caught = 0
            total_seen = 0

            for entry in dex_data.keys():
                hatched = random.randint(9999, 19999)
                total_seen += hatched

                caught = random.randint(9999, 19999)
                total_caught += caught

                seen = caught * (1.5 + random.random())
                total_seen += seen

                """
                Src Code: https://github.com/pagefaultgames/pokerogue/blob/4b36d38acbdc2d80448727b08bb77ab1b33c6207/src/system/game-data.ts#L149C1-L158C1
                export interface DexEntry {
                    seenAttr: bigint;
                    caughtAttr: bigint;
                    natureAttr: integer,
                    seenCount: integer;
                    caughtCount: integer;
                    hatchedCount: integer;
                    ivs: integer[];
                }

                """

                dex_data[entry] = {
                    "seenAttr": JSBigInt._MAX,
                    "caughtAttr": JSBigInt._MAX,
                    "natureAttr": JSInt._MAX,
                    "seenCount": JSInt(seen).value,
                    "caughtCount": JSInt(caught).value,
                    "hatchedCount": JSInt(hatched).value,
                    "ivs": [31, 31, 31, 31, 31, 31],
                }

                """
                Src Code: https://github.com/pagefaultgames/pokerogue/blob/4b36d38acbdc2d80448727b08bb77ab1b33c6207/src/system/game-data.ts#L193C1-L202C2
                export interface StarterDataEntry {
                    moveset: StarterMoveset | StarterFormMoveData;
                    eggMoves: integer;
                    candyCount: integer;
                    friendship: integer;
                    abilityAttr: integer;
                    passiveAttr: integer;
                    valueReduction: integer;
                    classicWinCount: integer;
                }


                """

                starter_data[entry] = {
                    "moveset": None,
                    "eggMoves": JSInt._MAX,
                    "candyCount": JSInt(caught + random.randint(99, 999)).value,
                    "friendship": JSInt._MAX,
                    "abilityAttr": JSInt._MAX,
                    "passiveAttr": 0 if entry in self.NO_PASSIVE else 3,
                    "valueReduction": 2,
                    "classicWinCount": 0,
                }

            game_stats["battles"] = JSInt(
                total_caught + random.randint(99, total_caught)
            ).value
            game_stats["pokemonDefeated"] = JSInt(
                total_seen + random.randint(99, total_caught)
            ).value
            game_stats["pokemonHatched"] = JSInt(total_hatched).value
            game_stats["pokemonCaught"] = JSInt(total_caught).value
            game_stats["pokemonSeen"] = JSInt(total_seen).value
            game_stats["shinyPokemonCaught"] = JSInt(
                (total_caught + total_hatched) // 100
            ).value

            if upload:
                self.api.set_trainer(self.trainer)

            logger.info("All starter pokemon modded.")

        except Exception as e:
            logger.exception(e)

    def mod_game_stats(self, number=9999, upload=True):
        try:
            game_stats = self.trainer["gameStats"]

            game_stats["classicSessionsPlayed"] = number // 10
            game_stats["dailyRunSessionsPlayed"] = number
            game_stats["dailyRunSessionsWon"] = number
            game_stats["eggsPulled"] = number
            game_stats["endlessSessionsPlayed"] = number
            game_stats["epicEggsPulled"] = number
            game_stats["highestDamage"] = number
            game_stats["highestEndlessWave"] = number
            game_stats["highestHeal"] = number
            game_stats["highestLevel"] = number
            game_stats["highestMoney"] = number
            game_stats["legendaryEggsPulled"] = number
            game_stats["legendaryPokemonCaught"] = number
            game_stats["legendaryPokemonHatched"] = number
            game_stats["legendaryPokemonSeen"] = number
            game_stats["manaphyEggsPulled"] = number
            game_stats["mythicalPokemonCaught"] = number
            game_stats["mythicalPokemonHatched"] = number
            game_stats["mythicalPokemonSeen"] = number
            game_stats["playTime"] = number * 1000
            game_stats["pokemonFused"] = number
            game_stats["rareEggsPulled"] = number
            game_stats["ribbonsOwned"] = number
            game_stats["sessionsWon"] = number
            game_stats["shinyPokemonHatched"] = number
            game_stats["shinyPokemonSeen"] = number
            game_stats["subLegendaryPokemonCaught"] = number
            game_stats["subLegendaryPokemonHatched"] = number
            game_stats["subLegendaryPokemonSeen"] = number
            game_stats["trainersDefeated"] = number

            if upload:
                self.api.set_trainer(self.trainer)

            logger.info("All game stats updated.")

        except Exception as e:
            logger.exception(e)

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

        func = {
            "0": self.close,
            "1": self.generate_eggs,
            "2": self.set_hatch_waves_to_zero,
            "3": self.mod_starters,
            "4": self.mod_game_stats,
        }

        cmd = "\n".join(
            [
                "<------------------------- POKEROGUE COMMANDS ------------------------>",
                "0: Close.",
                "1: Generate eggs.",
                "2: Hatch all eggs after next battle.",
                "3: Mod starters.",
                "4: Hatch all eggs after next battle.",
                "-----------------------------------------------------------------------",
            ]
        )

        while True:
            logger.info(f"\n{cmd}")
            command = input("Command: ")

            if command in func:
                try:
                    func[command]()
                except ExitCommandLoop:
                    logger.info("Stopped RogueEditor.")
                    break

                except Exception as e:
                    logger.exception(e)

            else:
                logger.info("Command not found!")
