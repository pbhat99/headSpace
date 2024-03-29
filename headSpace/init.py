import os
import nuke




#This will add all folders to the nuke plugin path.
#This will ease updating folder or delete conflicting script.

def initAddPath():
    directory = os.path.dirname(__file__) #folder path of this file location
    file_paths = []
    results = next(os.walk(directory, followlinks=False))[1] #list of only one level walk
    results.sort(reverse=True)
    for dirpath in results:
        if dirpath[0] != "." and dirpath[0] != "_":
            nuke.pluginAddPath(dirpath) # adding available paths


if nuke.GUI:
    nuke.tprint('Loading Custom Tools by Prasannakumar T Bhat\n' + __file__) # Let me confirm loading of this file in nuke terminal
    initAddPath()
else:
    nuke.tprint('skipped (no GUI)')

def savePreferencesToFile():
    '''
    Save current preferences to the prefencesfile in the .nuke folder.
    Pythonic alternative to the 'ok' button of the preferences panel.
    '''

    nukeFolder = os.path.expanduser('~') + '/.nuke/'
    preferencesFile = nukeFolder + 'preferences%i.%i.nk' %(nuke.NUKE_VERSION_MAJOR,nuke.NUKE_VERSION_MINOR)

    preferencesNode = nuke.toNode('preferences')

    customPrefences = preferencesNode.writeKnobs( nuke.WRITE_USER_KNOB_DEFS | nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT | nuke.TO_VALUE )
    customPrefences = customPrefences.replace('\n','\n  ')

    preferencesCode = 'Preferences {\n inputs 0\n name Preferences%s\n}' %customPrefences 

    # write to file
    openPreferencesFile = open( preferencesFile , 'w' )
    openPreferencesFile.write( preferencesCode )
    openPreferencesFile.close()


#nuke.pluginAddPath('./Cattery')
#nuke.ViewerProcess.register("Title_of_Gizmo",nuke.Node,("Your_Saved_Gizmo_Name", ""))