import nuke
import readFromWrite
import versionToLatest
import recursiveRead

def superRead():
    selected_nodes = nuke.selectedNodes()

    # If nothing is selected, run recursive logic
    if not selected_nodes:
        print('No selection: running recursive search.')
        recursiveRead.recursive_read()
        return

    for node in selected_nodes:
        node_class = node.Class()
        
        # 1. Handle Write nodes (Create Reads)
        if node_class in ['Write', 'WriteGeo', 'DeepWrite']:
            readFromWrite.readwrites()
            print('Processed Write node: ' + node.name())

        # 2. Handle nodes with a 'file' knob (Version Up)
        elif 'file' in node.knobs():
            versionToLatest.versionToLatest()
            print('Versioned up: ' + node.name())

        # 3. Fallback for everything else
        else:
            print('Non-file node selected (' + node.name() + '): running recursive logic.')
            recursiveRead.recursive_read()

mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'superRead', 'superRead()', 'alt+r', shortcutContext=2, icon = 'pbIcon.png')
