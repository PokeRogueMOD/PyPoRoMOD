# `Any usage of the PokéRogue API outside of the official site (pokerogue.net) is forbidden (The only approved external client at the time of writing is admiralbilly's offline version)`

> [!IMPORTANT]  
> **The content of this repo is a proof of concept and is for educational purposes only!**

> [!CAUTION]
> This tool **is currently not working** and is no longer actively used or maintained by me.
> 
> The game developers have explicitly stated that using the API externally is **not allowed**, so I’ve decided to stop using this tool myself. Instead, I now use [my MOD overlay `JsPoRoMOD`](https://github.com/PokeRogueMOD/JsPoRoMOD), which **does not use the API**. It interacts directly with the in-browser game object. This method is more complex (it’s not just editing JSON), but since mods were not explicitly forbidden, I’ve chosen to go this route.
>
> _Remember to be alert at all times. Stay aware of your surroundings._

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
