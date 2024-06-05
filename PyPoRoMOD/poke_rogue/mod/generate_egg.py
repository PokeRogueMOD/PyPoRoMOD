import json
import random
import time
from enum import Enum

# From PokeRogue Source Code
EGG_SEED = 1073741824


class GachaType(Enum):
    MOVE = 0
    LEGENDARY = 1
    SHINY = 2


class EggTier(Enum):
    COMMON = 0
    RARE = 1
    EPIC = 2
    LEGENDARY = 3
    MANAPHY = 4


# Function to generate valid ID ranges for a given tier
def get_id_range(tier):
    start = tier * EGG_SEED
    end = (tier + 1) * EGG_SEED - 1
    return start or 255, end


# Function to get a random ID within a specified range with step
def get_random_id_in_range(start, end, is_manaphy=False):
    if is_manaphy:
        return random.randrange(start, end + 1, 255)
    else:
        result = random.randint(start, end)
        result = result if result % 255 != 0 else result - 1
        result = result if result > 0 else 1
        return result


# Generator function
def generate_eggs(tier, gacha_type, hatch_waves):
    is_manaphy = tier.value == 4
    start, end = get_id_range(0 if is_manaphy else tier.value)

    while True:
        egg_id = get_random_id_in_range(start, end, is_manaphy)

        # Use the current timestamp in milliseconds
        timestamp = int(time.time() * 1000)

        # Create and yield the egg object
        yield {
            "id": egg_id,
            "gachaType": gacha_type.value,
            "hatchWaves": hatch_waves,
            "timestamp": timestamp,
        }
