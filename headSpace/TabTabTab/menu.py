import nuke
import tabtabtab_nuke
import tabtabtab_prefs
import tabtabtab_prefs_dialog

try:
    if tabtabtab_prefs.prefs_singleton.get("tabtabtab_enabled"):
        tabtabtab_nuke.registerNukeAction()
except Exception:
    import traceback
    traceback.print_exc()

edit_menu = nuke.menu("Nuke").findItem("Edit")

def _find_item_index(parent_menu, item_name):
    for position, menu_item in enumerate(parent_menu.items()):
        if menu_item.name() == item_name:
            return position
    return -1

project_settings_index = _find_item_index(edit_menu, "Project Settings...")
insert_index = project_settings_index + 1

edit_menu.addCommand(
    "Tabtabtab Preferences...",
    tabtabtab_prefs_dialog.show_prefs_dialog,
    index=insert_index,
)
