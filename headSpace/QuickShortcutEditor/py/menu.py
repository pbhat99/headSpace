# QuickShortcutEditor v1.3 - Max van Leeuwen


import QuickShortcutEditor
import os

# get script path parent folder
thisScript = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# replace backwards slashes with forwards slashes, append the user file name at the end
Keyboard_Shortcuts = thisScript.replace('\\', '/') + '/Keyboard_Shortcuts.txt'

# call function
QuickShortcutEditor.assignfromFile(Keyboard_Shortcuts)