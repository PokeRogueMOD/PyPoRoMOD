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


class Mode(Enum):
    MESSAGE = 0
    TITLE = 1
    COMMAND = 2
    FIGHT = 3
    BALL = 4
    TARGET_SELECT = 5
    MODIFIER_SELECT = 6
    SAVE_SLOT = 7
    PARTY = 8
    SUMMARY = 9
    STARTER_SELECT = 10
    EVOLUTION_SCENE = 11
    EGG_HATCH_SCENE = 12
    CONFIRM = 13
    OPTION_SELECT = 14
    MENU = 15
    MENU_OPTION_SELECT = 16
    SETTINGS = 17
    SETTINGS_DISPLAY = 18
    SETTINGS_AUDIO = 19
    SETTINGS_GAMEPAD = 20
    GAMEPAD_BINDING = 21
    SETTINGS_KEYBOARD = 22
    KEYBOARD_BINDING = 23
    ACHIEVEMENTS = 24
    GAME_STATS = 25
    VOUCHERS = 26
    EGG_LIST = 27
    EGG_GACHA = 28
    LOGIN_FORM = 29
    REGISTRATION_FORM = 30
    LOADING = 31
    SESSION_RELOAD = 32
    UNAVAILABLE = 33
    OUTDATED = 34
    CHALLENGE_SELECT = 35
