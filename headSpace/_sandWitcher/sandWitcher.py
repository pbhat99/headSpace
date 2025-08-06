import nuke
import os

# --- GLOBALS ---
# Global storage of selected nodes and their positions
# Note: storing node references only valid during session
sandWitcherTargetNodes = []

# --- PATH ---
SANDWITCHER_PATH = os.path.expanduser('~/.nuke/sandWitcher')

# --- SELECTION & STORAGE ---

def store_selection():
    global sandWitcherTargetNodes
    selected = nuke.selectedNodes()
    sandWitcherTargetNodes = nuke.selectedNodes()


# --- TOOLSET MENU ACTIONS ---

def create_toolset(nk_path):
    """
    Returns a function that:
    - Stores current selection globally
    - Imports the specified toolset nk file
    """
    store_selection()
    nuke.nodePaste(nk_path)

# --- MENU BUILDING ---

def add_toolset_menu_items(menu, folder_path):
    """
    Recursively scan folder path and add toolset menus
    """
    for entry in sorted(os.listdir(folder_path)):
        full_path = os.path.join(folder_path, entry)
        if os.path.isdir(full_path):
            submenu = menu.addMenu(entry)
            add_toolset_menu_items(submenu, full_path)
        elif entry.endswith('.nk'):
            toolset_name = os.path.splitext(entry)[0]
            ts_menu = menu.addCommand(toolset_name, create_toolset(full_path))


def rebuild_sandwitcher_menu(menu=None):
    """
    Build or rebuild the SandWitcher Toolsets menu.
    """
    if not os.path.exists(SANDWITCHER_PATH):
        nuke.message(f"SandWitcher toolset path not found:\n{SANDWITCHER_PATH}")
        return
    menu = nuke.menu('Nodes').addMenu('SandWitcher Toolsets')
    add_toolset_menu_items(menu, SANDWITCHER_PATH)


# Call this function once when importing to set up menu immediately
rebuild_sandwitcher_menu()


# --- ONCREATE CALLBACK FUNCTION ---

def sandwitcher_on_create():
    """
    To be pasted into the SandWitcher placeholder Group node's onCreate callback.
    Uses the global selection saved before toolset import.
    """
    global sandWitcherTargetNodes, sandWitcherTargetPositions

    placeholder = nuke.thisNode()
    xpos, ypos = placeholder.xpos(), placeholder.ypos()

    if not sandWitcherTargetNodes:
        nuke.message("No SandWitcher target nodes found - please select node(s) before loading the toolset.")
        return

    # For example, process all saved target nodes or just first as needed
    for target_node in sandWitcherTargetNodes:
        if not target_node.Class():  # check node still exists
            continue

        pos = sandWitcherTargetPositions.get(target_node.name(), (xpos, ypos))
        target_node.setXpos(pos[0])
        target_node.setYpos(pos[1])

        # Example placeholder wiring logic:
        # Connect the node upstream/downstream around the placeholder node
        upstream = placeholder.input(0)
        if upstream:
            target_node.setInput(0, upstream)
        else:
            # No upstream: keep existing inputs if any
            pass

        # Connect downstream nodes to this target node
        for n in placeholder.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS):
            for i in range(n.inputs()):
                if n.input(i) == placeholder:
                    n.setInput(i, target_node)

    # Delete the placeholder node after wiring is done
    nuke.delete(placeholder)

    # Clear globals to avoid stale references
    sandWitcherTargetNodes = []
    sandWitcherTargetPositions = {}

# -- END OF FILE --
