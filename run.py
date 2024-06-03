from PyPoRoAnal import WSpecies, PokeRogueAPI

username = input("Username: ")
password = input("Password: ")

test = PokeRogueAPI(username, password)
trainer = test.get_trainer()
print(f"{test.set_trainer(trainer) = }")

slot = test.get_slot(0)
print(f"{test.set_slot(0, slot) = }")

# test = PokeRogueAPI.create_account("NewAccountName", "NewAccountPassword")
# print(test)