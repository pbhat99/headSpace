import json
import os

PREFS_FILE = os.path.join(os.path.expanduser("~"), ".nuke", "tabtabtab_prefs.json")

DEFAULTS = {
    "tabtabtab_enabled": True,
    "space_mode_order": ["anchored_fuzzy", "non_anchored_fuzzy", "consecutive"],
}


class TabtabtabPrefs:
    def __init__(self, prefs_file=PREFS_FILE):
        self._prefs_file = prefs_file
        self._prefs = self._load()

    def _load(self):
        if os.path.exists(self._prefs_file):
            with open(self._prefs_file, "r") as f:
                loaded = json.load(f)
            return {**DEFAULTS, **loaded}
        return dict(DEFAULTS)

    def get(self, key):
        return self._prefs.get(key, DEFAULTS.get(key))

    def set(self, key, value):
        self._prefs[key] = value

    def save(self):
        with open(self._prefs_file, "w") as f:
            json.dump(self._prefs, f, indent=2)

    def reload(self):
        self._prefs = self._load()


prefs_singleton = TabtabtabPrefs()
