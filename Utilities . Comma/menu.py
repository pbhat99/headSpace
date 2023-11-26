#-------------------------------------------------
# Comma by Adrian Pueyo
# Intelligent dot with auto-connection features
# adrianpueyo.com, 2017
version = "1.0"
#-------------------------------------------------

import nuke
def makeComma():
    import os
    dotNukeDir = os.path.normpath(os.path.expanduser('~/.nuke'))
    commaDefFile = dotNukeDir + "/commaDefault.nk"
    if os.path.isfile(commaDefFile):
        try:
            nuke.nodePaste(commaDefFile)
        except:
            nuke.message("Error loading Comma default. Making normal Comma.")
            nuke.createNode("Comma")
    else:
        nuke.createNode("Comma")

mainMenu = menuMaker()
nuke.menu("Nuke").addCommand(mainMenu + 'Comma','makeComma()',',',icon='Comma.png',index=6)
