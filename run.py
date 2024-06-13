from PyPoRoMOD.account_manager import AccountManager

AccountManager().run()

# import json
# from pathlib import Path
# from PyPoRoMOD.enum import speciesEggMoves


# # Create a dictionary with the species names and their corresponding move values as strings
# dict_data = {
#     species.value: [str(move.value) for move in moves]
#     for species, moves in speciesEggMoves.items()
# }

# # Define the directory and file path
# _DIR = Path(__file__).resolve().parent
# file_path = _DIR / "speciesEggMoves.json"

# # Write the dictionary to a JSON file
# with open(file_path, "w") as f:
#     json.dump(dict_data, f, indent=4)
