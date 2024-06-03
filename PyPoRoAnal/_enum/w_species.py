# extended_enum.py
from .gen import Species


class WSpecies:
    """Wrapper class for the Species enum."""

    def __init__(self, species):
        if not isinstance(species, Species):
            raise ValueError("Invalid species")
        self.species = species

    def describe(self):
        return f"{self.species.name} is a valid option with value {self.species.value}"

    @classmethod
    def get_all_options(cls):
        return [cls(species) for species in Species]

    @classmethod
    def get_default_starter(cls):
        return [
            Species.BULBASAUR,
            Species.CHARMANDER,
            Species.SQUIRTLE,
            Species.CHIKORITA,
            Species.CYNDAQUIL,
            Species.TOTODILE,
            Species.TREECKO,
            Species.TORCHIC,
            Species.MUDKIP,
            Species.TURTWIG,
            Species.CHIMCHAR,
            Species.PIPLUP,
            Species.SNIVY,
            Species.TEPIG,
            Species.OSHAWOTT,
            Species.CHESPIN,
            Species.FENNEKIN,
            Species.FROAKIE,
            Species.ROWLET,
            Species.LITTEN,
            Species.POPPLIO,
            Species.GROOKEY,
            Species.SCORBUNNY,
            Species.SOBBLE,
            Species.SPRIGATITO,
            Species.FUECOCO,
            Species.QUAXLY,
        ]

    def __str__(self):
        return self.species.name

    def __repr__(self):
        return f"<PRSpecies: {self.species.name}>"
