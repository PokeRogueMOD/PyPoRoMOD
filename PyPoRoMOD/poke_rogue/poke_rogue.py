import json
from pathlib import Path
import random
import time
from loguru import logger
from PyPoRoMOD.api.poke_rogue_api import PokeRogueAPI
from PyPoRoMOD.data_types.js_big_int import JSBigInt
from PyPoRoMOD.data_types.js_int import JSInt
from PyPoRoMOD.utils import ExitCommandLoop
from PyPoRoMOD.enum import (
    Achievements,
    SignatureSpecies,
    Species,
    Unlockables,
    VoucherType,
    speciesEggMoves,
)

from .mod import EggTier, GachaType, generate_eggs


class PokeRogue:
    _DIR = Path(__file__).resolve().parent
    _SAVE_PATH = _DIR.parent.parent / "accounts"

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

    username: str | None = None
    password: str | None = None
    display_name: str | None = None
    api: PokeRogueAPI | None = None
    trainer: dict = {}
    slots: dict = {}

    def __init__(self, username: str, password: str, display_name: str) -> None:
        self.username = username
        self.password = password
        self.display_name = display_name
        self.api = PokeRogueAPI(self.username, self.password)
        self.trainer = self.api.get_trainer() or {}
        self.slots = {s: self.api.get_slot(s) for s in range(5)}

        logger.info(f"Logged in <{self.display_name}> successfully.")

    def close(self):
        logger.debug("Stopping RogueEditor.")
        raise ExitCommandLoop

    def generate_eggs(self, upload=True):
        """Generate eggs by using user inputs."""
        try:
            egg_len = len(self.trainer.get("eggs", []) or [])

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
                self.api.set_trainer(self.trainer, self)

            logger.info(f"[{count}] eggs got generated.")

        except Exception as e:
            logger.exception(e)

    def set_hatch_waves_to_zero(self, upload=True):
        try:
            if (
                "eggs" not in self.trainer
                or self.trainer["eggs"] is None
                or len(self.trainer["eggs"]) == 0
            ):
                logger.info("No eggs to hatch.")
                return

            for egg in self.trainer["eggs"]:
                egg["hatchWaves"] = 0

            if upload:
                self.api.set_trainer(self.trainer, self)

            logger.info("All eggs will hatch after the next battle.")

        except Exception as e:
            logger.exception(e)

    def mod_starters(self, upload=True):
        try:
            if not "dexData" in self.trainer:
                self.trainer["dexData"] = {}
            if not "starterData" in self.trainer:
                self.trainer["starterData"] = {}
            if not "gameStats" in self.trainer:
                self.trainer["gameStats"] = {}
            dex_data = self.trainer["dexData"]
            starter_data = self.trainer["starterData"]
            game_stats = self.trainer["gameStats"]
            total_hatched = 0
            total_caught = 0
            total_seen = 0

            for s in Species:
                dex_id = str(s.value)
                hatched = random.randint(9999, 19999)
                total_hatched += hatched

                caught = random.randint(9999, 19999)
                total_caught += caught

                seen = int(caught * (1.5 + random.random()))
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

                dex_data[dex_id] = {
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
                moveset = (
                    [e.value for e in speciesEggMoves[s]]
                    if s in speciesEggMoves
                    else None
                )
                starter_data[dex_id] = {
                    "moveset": moveset,
                    "eggMoves": JSInt._MAX,
                    "candyCount": JSInt(caught + random.randint(99, 999)).value,
                    "friendship": JSInt._MAX,
                    "abilityAttr": JSInt._MAX,
                    "passiveAttr": 0 if dex_id in self.NO_PASSIVE else 3,
                    "valueReduction": 10,
                    "classicWinCount": 1,
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
                self.api.set_trainer(self.trainer, self)

            logger.info("All starter pokemon modded.")

        except Exception as e:
            logger.exception(e)

    def mod_game_stats(self, number=JSInt._SAVE, upload=True):
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
            game_stats["highestMoney"] = JSBigInt._MAX
            game_stats["legendaryEggsPulled"] = number
            game_stats["legendaryPokemonCaught"] = number
            game_stats["legendaryPokemonHatched"] = number
            game_stats["legendaryPokemonSeen"] = number
            game_stats["manaphyEggsPulled"] = number
            game_stats["mythicalPokemonCaught"] = number
            game_stats["mythicalPokemonHatched"] = number
            game_stats["mythicalPokemonSeen"] = number
            game_stats["playTime"] = number
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
                self.api.set_trainer(self.trainer, self)

            logger.info("All game stats updated.")

        except Exception as e:
            logger.exception(e)

    def trainer_download(self):
        trainer_dir = self._SAVE_PATH / self.username
        trainer_dir.mkdir(parents=True, exist_ok=True)
        trainer_file = trainer_dir / "trainer.json"

        try:
            with open(trainer_file, "w") as f:
                f.write(json.dumps(self.trainer, indent=2))
                logger.info(f"Downloaded trainer data -> '{trainer_file}'")

        except Exception as e:
            logger.exception(e)

    def trainer_upload(self):
        trainer_dir = self._SAVE_PATH / self.username
        trainer_file = trainer_dir / "trainer.json"

        if not trainer_file.exists():
            logger.info(f"Download the trainer data first.")

        try:
            with open(trainer_file, "rb") as f:
                json_data = json.load(f)
                self.api.set_trainer(json_data, self)
                logger.info("Uploaded trainer data.")

        except Exception as e:
            logger.exception(e)

    def slots_download(self):
        trainer_dir = self._SAVE_PATH / self.username
        trainer_dir.mkdir(parents=True, exist_ok=True)

        saved_slots = []
        try:
            for i, slot in enumerate(self.slots.values()):
                if slot is not None:
                    slot_counter = i + 1
                    with open(trainer_dir / f"slot {slot_counter}.json", "w") as f:
                        f.write(json.dumps(slot, indent=4))
                        saved_slots.append(str(slot_counter))

            if len(saved_slots) == 0:
                logger.info("No gamesave data to download!")
            else:
                file_str = f"slot [{', '.join(saved_slots)}].json"
                logger.info(f"Downloaded gamesave data -> {trainer_dir / file_str}")

        except Exception as e:
            logger.exception(e)

    def slots_upload(self):
        trainer_dir = self._SAVE_PATH / self.username

        uploaded_slots = []
        try:
            for i, slot in enumerate(self.slots.values()):
                if slot is not None:
                    slot_counter = i + 1
                    file_path = trainer_dir / f"slot {slot_counter}.json"
                    if file_path.exists():
                        with open(file_path, "rb") as f:
                            json_data = json.load(f)
                            self.api.set_slot(i, json_data)

                            uploaded_slots.append(str(slot_counter))

            if len(uploaded_slots) == 0:
                logger.info("No slots to upload, download them first.")
            else:
                file_str = f"slot [{', '.join(uploaded_slots)}].json"
                logger.info(f"Uploaded gamesave data -> {trainer_dir / file_str}")

        except Exception as e:
            logger.exception(e)

    def account_download(self):
        self.trainer_download()
        self.slots_download()

    def account_upload(self):
        self.trainer_upload()
        self.slots_upload()

    def set_vouchers(self, number=JSInt._SAVE, upload=True):
        try:
            self.trainer["voucherCounts"] = {
                str(enum.value): number for enum in VoucherType
            }

            if upload:
                self.api.set_trainer(self.trainer, self)

            logger.info(f"Set all vouchers count to [{number}].")

        except Exception as e:
            logger.exception(e)

    def unlock_modes(self, upload=True):
        try:
            self.trainer["unlocks"] = {str(enum.value): True for enum in Unlockables}

            if upload:
                self.api.set_trainer(self.trainer, self)

            logger.info("All modes unlocked.")

        except Exception as e:
            logger.exception(e)

    def unlock_achievements(self, upload=True):
        try:
            timestamp_ms = int(time.time() * 1000)

            self.trainer["achvUnlocks"] = {
                achievement.name: timestamp_ms for achievement in Achievements
            }

            if upload:
                self.api.set_trainer(self.trainer, self)

            logger.info("All achievements unlocked.")

        except Exception as e:
            logger.exception(e)

    def unlock_vouchers(self, upload=True):
        try:
            timestamp_ms = int(time.time() * 1000)

            self.trainer["voucherUnlocks"] = {
                trainer.name: timestamp_ms for trainer in SignatureSpecies
            }

            if upload:
                self.api.set_trainer(self.trainer, self)

            logger.info("All vouchers unlocked.")

        except Exception as e:
            logger.exception(e)

    def one_click_max(self):
        try:
            self.unlock_modes()
            self.unlock_achievements()
            self.unlock_vouchers()
            self.mod_game_stats()
            self.mod_starters()
            self.set_vouchers()
            self.set_hatch_waves_to_zero()

            logger.info("Account maxed out.")

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
        # Also use the official key replacements to save more disk space and also gzip the data and save it as a blob.
        # Implement the export to json in the gui and download it from there as a json with the trainer and all slots included, where empty slots are None

        # Reverse the legendary egg code to see if you can somehow select the legendary this way or is it only the 50% chance, search it in the src code!

        func = {
            "0": self.close,
            "1": self.account_download,
            "2": self.account_upload,
            "3": self.trainer_download,
            "4": self.trainer_upload,
            "5": self.slots_download,
            "6": self.slots_upload,
            "7": self.generate_eggs,
            "8": self.set_hatch_waves_to_zero,
            "9": self.mod_starters,
            "10": self.mod_game_stats,
            "11": self.set_vouchers,
            "12": self.unlock_modes,
            "13": self.unlock_achievements,
            "14": self.unlock_vouchers,
            "15": self.one_click_max,
        }

        cmd = "\n".join(
            [
                "╔═════════════════════════ PyPoRoMOD COMMANDS ════════════════════════╗",
                "╠═ 0: Close.                                                          ║",
                "║                                                                     ║",
                "╠═ 1: Download ALL account data to JSON.                              ║",
                "╠═ 2: Upload ALL account data to JSON.                                ║",
                "╠═ 3: Download trainer data to JSON.                                  ║",
                "╠═ 4: Upload trainer data to JSON.                                    ║",
                "╠═ 5: Download slots data 1-5 to JSON if they exist.                  ║",
                "╠═ 6: Upload slots data 1-5 to JSON if they exist.                    ║",
                "║                                                                     ║",
                "╠═ 7: Generate eggs.                                                  ║",
                "╠═ 8: Hatch all eggs after next battle.                               ║",
                "╠═ 9: Unlock all starter pokemon forms and variants shiny t3.         ║",
                "╠═ 10: Set game stats to high values.                                 ║",
                "╠═ 11: Set vouchers to max save to use amount.                        ║",
                "╠═ 12: Unlock all game modes.                                         ║",
                "╠═ 13: Unlock all achievements.                                       ║",
                "╠═ 14: Unlock all vouchers.                                           ║",
                "║                                                                     ║",
                "╠═ 15: 1-Click max account.                                           ║",
                "╚═════════════════════════════════════════════════════════════════════╝",
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
