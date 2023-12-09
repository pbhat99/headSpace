import nuke
import welcomeScreen
import welcome_helper

mainMenu = menuMaker()
nuke.menu('Nuke').addCommand(mainMenu + 'Welcome Screen', 'welcomeScreen.main()')


def addRecent():
	nkPath = nuke.Root().knob("name").value()
	if nkPath != "":
		welcome_helper.addToRecentFiles(nkPath)

nuke.addOnScriptSave(addRecent)
nuke.addOnScriptClose(addRecent)


#nuke.tprint('welcomescreen log')