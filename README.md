# `Any usage of the PokéRogue API outside of the official site (pokerogue.net) is forbidden (The only approved external client at the time of writing is admiralbilly's offline version)`

> [!IMPORTANT]  
> **⚠️ The content of this repo is a proof of concept and is for educational purposes only! ⚠️**

> [!TIP]
> <ins>**I fixed the API implementation. Everything should work again! (12. June 2024)**</ins>

> [!CAUTION]
> This tool works, but since the game devs expcilite say its not allowed to use the API externally, I will not use the tool myself anymore. But I will use my MOD overlay, which does not use the API, but the game objects in your browser instead. This is harder to do since its not just editing json, but since mods where not mentioned i will go this route. You can still use this tool at your own risk, but I will only try to fix it if it breaks, so create an issue in that case. I will probably not notice this myself because I am trying to implement all account modification features in the overlay instead and have already implemented the most important features I need and want, besides json import/export!
> 
> This tool can cause your account to be flagged, I have had no problems so far, but be warned, you can read about it [here](https://www.reddit.com/r/pokerogue/comments/1d8ldlw/a_cheating_and_account_deletionwipe_followup/)!

> [!Note]
> Since i dont want any drama, but just dont want false claims to be spread around users and devs, i made the statement with proof that i made the egg generator and are not "overflowing values", this is a fun tool to glich accounts, so use it only on a test account, the account will be 100% flagged with this tool, but its only for the account you use, not ip related as far as i know, but i will never know since i dont play ladder or multiplayer! And yes I use ChatGPT 4o if you want to have a video tutorial how I do everything and what my tipps are with ChatGPT let me know im allways happy to share my knowlage. You can use my code for your project, the only thing that would be nice is a comment in the code saying its from me, or a mention in the readme, even if its at the bottom of the page. I will not take any legal action even if you "steal" my code without proper licensing, so feel free to explore it yourself!

# PyPoRoMOD

Welcome to the PyPoRoMOD! This project aims to analyze and modify the account and slot data. I just finished the API and a basic TypeScript to Python translator for Enums. The next step will be adding features, so stay tuned for new updates...

## Features

- [x]   API to interact with the game server (online and local)
- [x]   Account Manager
    - [x]   Add Accounts
    - [x]   Manage Accounts
    - [x]   Create PokeRogue Accounts
- [x]   Account MOD
    - [x]   Download trainer and slots to json
    - [x]   Upload trainer and slots to json
    - [x]   Select and generate eggs without using vouchers, by selecting the tier and gacha type
    - [x]   Hatch all eggs after the next battle
    - [x]   Unlock all starters T3 shiny with all forms and variants
    - [x]   Set high game stats
    - [x]   Set max save to use voucher count
    - [x]   Unlock all gamemodes (Endless, Spliced Endless, Daily)
    - [x]   Unlock all achievements
    - [x]   Unlock all vouchers
    - [x]   Max account with 1 command
    - [ ]   Automaticly unlock accounts.
    - [ ]   Edit slots (Add items, change pokemon level, enemys, etc.)

## [Discord Server](https://discord.gg/rsNPUcbrPT)

## [Video Tutorial](https://youtu.be/nYmoTRMg2-Y)

[![Video Tutorial](./resources/thumbnail.png)](https://youtu.be/nYmoTRMg2-Y)

## Contact

If you have any questions, suggestions, or need further assistance, feel free to reach out (Discord: mpb.rip).

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

### Acknowledgments

-   This project uses [Loguru](https://github.com/Delgan/loguru) which is licensed under the MIT License.
