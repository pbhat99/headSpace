import nuke
import welcomeScreen
import welcome_helper


nuke.menu('Nuke').addCommand('-{ pb }-/Welcome Screen', 'welcomeScreen.main()')


def addRecent():
	nkPath = nuke.Root().knob("name").value()
	if nkPath != "":
		welcome_helper.addToRecentFiles(nkPath)

nuke.addOnScriptSave(addRecent)
nuke.addOnScriptClose(addRecent)


nuke.tprint('welcomescreen log')