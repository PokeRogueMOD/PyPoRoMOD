"""
BSD 3-Clause License

Copyright (c) 2024, Philipp Reuter
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from enum import Enum


class Biome(Enum):
    TOWN = 0
    PLAINS = 1
    GRASS = 2
    TALL_GRASS = 3
    METROPOLIS = 4
    FOREST = 5
    SEA = 6
    SWAMP = 7
    BEACH = 8
    LAKE = 9
    SEABED = 10
    MOUNTAIN = 11
    BADLANDS = 12
    CAVE = 13
    DESERT = 14
    ICE_CAVE = 15
    MEADOW = 16
    POWER_PLANT = 17
    VOLCANO = 18
    GRAVEYARD = 19
    DOJO = 20
    FACTORY = 21
    RUINS = 22
    WASTELAND = 23
    ABYSS = 24
    SPACE = 25
    CONSTRUCTION_SITE = 26
    JUNGLE = 27
    FAIRY_CAVE = 28
    TEMPLE = 29
    SLUM = 30
    SNOWY_FOREST = 31
    ISLAND = 40
    LABORATORY = 41
    END = 50
