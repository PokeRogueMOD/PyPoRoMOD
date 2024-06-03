from PyPoRoAnal import WSpecies, PokeRogueAPI

username = input("Username: ")
password = input("Password: ")
test = PokeRogueAPI(username, password)
trainer = test.get_trainer()
print(test.set_trainer(trainer))