import json
from pathlib import Path
from PyPoRoMOD.account_manager import AccountManager
from PyPoRoMOD.api.account_unlocker import AccountUnlocker

AccountManager().run()
# _DIR = Path(__file__).resolve().parent
# with open(_DIR / 'accounts' / 'generated_trainer.json', 'w') as f:
#     json.dump(AccountUnlocker.get_new_trainer(), f, indent=4)
