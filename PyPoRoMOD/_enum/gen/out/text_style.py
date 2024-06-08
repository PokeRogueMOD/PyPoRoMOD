"""
BSD 3-Clause License

Copyright (c) 2024, Philipp Reuter
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions, and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions, and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from enum import Enum


class TextStyle(Enum):
    MESSAGE = 0
    WINDOW = 1
    WINDOW_ALT = 2
    BATTLE_INFO = 3
    PARTY = 4
    PARTY_RED = 5
    SUMMARY = 6
    SUMMARY_ALT = 7
    SUMMARY_RED = 8
    SUMMARY_BLUE = 9
    SUMMARY_PINK = 10
    SUMMARY_GOLD = 11
    SUMMARY_GRAY = 12
    SUMMARY_GREEN = 13
    MONEY = 14
    STATS_LABEL = 15
    STATS_VALUE = 16
    SETTINGS_LABEL = 17
    SETTINGS_SELECTED = 18
    SETTINGS_LOCKED = 19
    TOOLTIP_TITLE = 20
    TOOLTIP_CONTENT = 21
    MOVE_INFO_CONTENT = 22
