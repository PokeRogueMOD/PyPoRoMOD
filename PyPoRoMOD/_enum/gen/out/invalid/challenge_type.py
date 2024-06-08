from enum import Enum


    """
    
An enum for all the challenge types. The parameter entries on these describe the
parameters to use when calling the applyChallenges function.

    """
    """
    
Challenges which modify what starters you can choose
@param args [0] {@link PokemonSpecies} The species to check
[1] {@link Utils.BooleanHolder} Sets to false if illegal, pass in true.

    """
class ChallengeType(Enum):
    STARTER_CHOICE = 0
    """
    
Challenges which modify how many starter points you have
@param args [0] {@link Utils.NumberHolder} The amount of starter points you have

    """
    STARTER_POINTS = 1
    """
    
Challenges which modify your starters in some way
Not Fully Implemented

    """
    STARTER_MODIFY = 2
    """
    
Challenges which limit which pokemon you can have in battle.
@param args [0] {@link Pokemon} The pokemon to check
[1] {@link Utils.BooleanHolder} Sets to false if illegal, pass in true.

    """
    POKEMON_IN_BATTLE = 3
    """
    
Adds or modifies the fixed battles in a run
@param args [0] integer The wave to get a battle for
[1] {@link FixedBattleConfig} A new fixed battle. It'll be modified if a battle exists.

    """
    FIXED_BATTLES = 4
