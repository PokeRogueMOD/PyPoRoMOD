"""
Refs:
    - Send session data: https://github.com/pagefaultgames/pokerogue/blob/a815b73d9644ec2eb486f8d0986531715167ca9c/src/system/game-data.ts#L1110
    - decrypt data: https://github.com/pagefaultgames/pokerogue/blob/a815b73d9644ec2eb486f8d0986531715167ca9c/src/system/game-data.ts#L69-L73
    - encrypt data: https://github.com/pagefaultgames/pokerogue/blob/a815b73d9644ec2eb486f8d0986531715167ca9c/src/system/game-data.ts#L63-L67
    - request: https://github.com/pagefaultgames/pokerogue/blob/d592187f2ce514c45e0417c703254a555c5a3fec/src/system/game-data.ts#L1096-L1101
    - get session save data: https://github.com/pagefaultgames/pokerogue/blob/d592187f2ce514c45e0417c703254a555c5a3fec/src/system/game-data.ts#L766
    - get system save data: https://github.com/pagefaultgames/pokerogue/blob/d592187f2ce514c45e0417c703254a555c5a3fec/src/system/game-data.ts#L271-L289
    - generate trainer and secret id: https://github.com/pagefaultgames/pokerogue/blob/d592187f2ce514c45e0417c703254a555c5a3fec/src/system/game-data.ts#L247-L248
"""

import random
import time
import json
from typing import Dict, List

from PyPoRoMOD.enum import (
    Achievements,
    SignatureSpecies,
    Species,
    Unlockables,
    VoucherType,
    PlayerGender,
    Gender,
    DexAttr,
    Nature,
    defaultStarterSpecies,
    speciesStarters,
    AbilityAttr,
)


class AccountUnlocker:
    MAX_INT_ATTR_VALUE = 2**31

    @classmethod
    def trainer_2_str(cls, obj):
        if isinstance(obj, int):
            if obj <= cls.MAX_INT_ATTR_VALUE:
                return obj
            else:
                return str(obj)
        raise TypeError("Type not serializable")

    @staticmethod
    def rand_int(range: int, min: int = 0) -> int:
        """
        Generate a random integer within a specified range.

        Args:
            range (int): The maximum value for the range.
            min (int, optional): The minimum value for the range. Defaults to 0.

        Returns:
            int: A random integer within the specified range.
        """
        if range == 1:
            return min
        return random.randint(min, min + range - 1)

    @classmethod
    def get_new_trainer(cls) -> Dict[str, object]:
        """
        Generate a new trainer with default values.

        Returns:
            Dict[str, object]: A dictionary containing the new trainer's attributes.
        """
        data = {
            "trainerId": cls.rand_int(65536, 1),
            "secretId": cls.rand_int(65536, 1),
            "gender": PlayerGender.FEMALE.value,
            "dexData": cls.init_dex_data(),
            "starterData": cls.init_starter_data(),
            "gameStats": cls.get_new_game_stats(),
            "unlocks": {str(enum.value): False for enum in Unlockables},
            "achvUnlocks": {},
            "voucherUnlocks": {},
            "voucherCounts": {str(enum.value): 0 for enum in VoucherType},
            "eggs": [],
            "eggPity": [0] * 4,
            "unlockPity": [0] * 4,
            "gameVersion": "1.0.4",
            "timestamp": int(time.time() * 1000),
        }
        return json.loads(json.dumps(data, default=cls.trainer_2_str))  # data

    @classmethod
    def get_new_game_stats(cls) -> Dict[str, int]:
        """
        Generate default game statistics.

        Returns:
            Dict[str, int]: A dictionary containing the default game statistics.
        """
        return {
            "playTime": 0,
            "battles": 0,
            "classicSessionsPlayed": 0,
            "sessionsWon": 0,
            "ribbonsOwned": 0,
            "dailyRunSessionsPlayed": 0,
            "dailyRunSessionsWon": 0,
            "endlessSessionsPlayed": 0,
            "highestEndlessWave": 0,
            "highestLevel": 0,
            "highestMoney": 0,
            "highestDamage": 0,
            "highestHeal": 0,
            "pokemonSeen": 0,
            "pokemonDefeated": 0,
            "pokemonCaught": 0,
            "pokemonHatched": 0,
            "legendaryPokemonSeen": 0,
            "legendaryPokemonCaught": 0,
            "legendaryPokemonHatched": 0,
            "mythicalPokemonSeen": 0,
            "mythicalPokemonCaught": 0,
            "mythicalPokemonHatched": 0,
            "shinyPokemonSeen": 0,
            "shinyPokemonCaught": 0,
            "shinyPokemonHatched": 0,
            "pokemonFused": 0,
            "trainersDefeated": 0,
            "eggsPulled": 0,
            "rareEggsPulled": 0,
            "epicEggsPulled": 0,
            "legendaryEggsPulled": 0,
            "manaphyEggsPulled": 0,
        }

    @classmethod
    def init_dex_data(cls) -> Dict[str, Dict[str, object]]:
        """
        Initialize the dex data with default values for all species.

        Returns:
            Dict[str, Dict[str, object]]: A dictionary containing the default dex data for all species.
        """
        data = {}
        for species in Species:
            species_value = str(species.value)
            data[species_value] = {
                "seenAttr": 0,
                "caughtAttr": 0,
                "natureAttr": 0,
                "seenCount": 0,
                "caughtCount": 0,
                "hatchedCount": 0,
                "ivs": [0, 0, 0, 0, 0, 0],
            }

        defaultStarterAttr = (
            DexAttr.NON_SHINY.value
            | DexAttr.MALE.value
            | DexAttr.DEFAULT_VARIANT.value
            | DexAttr.DEFAULT_FORM.value
        )
        neutralNatures = [
            Nature.HARDY,
            Nature.DOCILE,
            Nature.SERIOUS,
            Nature.BASHFUL,
            Nature.QUIRKY,
        ]

        for species in defaultStarterSpecies:
            species_value = str(species.value)
            nature = random.choice(neutralNatures)
            entry = data[species_value]
            entry["seenAttr"] = defaultStarterAttr
            entry["caughtAttr"] = defaultStarterAttr
            entry["natureAttr"] = 2 ** (nature.value + 1)
            entry["ivs"] = [10] * 6

        return data

    @classmethod
    def init_starter_data(cls) -> Dict[int, Dict[str, object]]:
        """
        Initialize starter data with default values.

        Returns:
            Dict[int, Dict[str, object]]: A dictionary containing the default starter data.
        """
        starterData = {}
        starterSpeciesIds = [species.value for species in speciesStarters.keys()]

        for speciesId in starterSpeciesIds:
            speciesId_value = str(speciesId)
            starterData[speciesId_value] = {
                "moveset": None,
                "eggMoves": 0,
                "candyCount": 0,
                "friendship": 0,
                "abilityAttr": (
                    AbilityAttr.ABILITY_1.value
                    if Species(speciesId) in defaultStarterSpecies
                    else 0
                ),
                "passiveAttr": 0,
                "valueReduction": 0,
                "classicWinCount": 0,
            }

        return starterData

    @classmethod
    def getSpeciesDefaultDexAttr(
        cls, species: Species, forSeen: bool = False, optimistic: bool = False
    ) -> int:
        """
        Get the default dex attributes for a species.

        Args:
            species (Species): The species to get attributes for.
            forSeen (bool, optional): Whether the attributes are for seen status. Defaults to False.
            optimistic (bool, optional): Whether to use optimistic attributes. Defaults to False.

        Returns:
            int: The combined default dex attributes for the species.
        """
        ret = 0
        species_value = str(species.value)
        dexEntry = cls.init_dex_data()[species_value]
        attr = dexEntry["caughtAttr"]
        ret |= (
            DexAttr.SHINY.value
            if optimistic and (attr & DexAttr.SHINY.value)
            else DexAttr.NON_SHINY.value
        )
        ret |= (
            DexAttr.MALE.value
            if (attr & DexAttr.MALE.value) or not (attr & DexAttr.FEMALE.value)
            else DexAttr.FEMALE.value
        )
        ret |= (
            DexAttr.DEFAULT_VARIANT.value
            if optimistic and (attr & DexAttr.SHINY.value)
            else (
                DexAttr.VARIANT_3.value
                if (attr & DexAttr.VARIANT_3.value)
                else (
                    DexAttr.VARIANT_2.value
                    if (attr & DexAttr.VARIANT_2.value)
                    else DexAttr.DEFAULT_VARIANT.value
                )
            )
        )
        ret |= DexAttr.DEFAULT_FORM.value
        return ret
