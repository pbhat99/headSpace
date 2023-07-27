#----------------------------------------------------------------------------------------------------------
# pb Preferences
# Inspired :) from W_Hotbox
#----------------------------------------------------------------------------------------------------------

import nuke
import os

def addToPreferences(knobObject, tooltip = None):
    '''
    Add a knob to the preference panel.
    Save current preferences to the prefencesfile in the .nuke folder.
    '''

    if knobObject.name() not in preferencesNode.knobs().keys():

        if tooltip != None:
            knobObject.setTooltip(tooltip)

        preferencesNode.addKnob(knobObject)
        savePreferencesToFile()
        return preferencesNode.knob(knobObject.name())

def savePreferencesToFile():
    '''
    Save current preferences to the prefencesfile in the .nuke folder.
    Pythonic alternative to the 'ok' button of the preferences panel.
    '''

    nukeFolder = os.path.expanduser('~') + '/.nuke/'
    preferencesFile = nukeFolder + 'preferences{}.{}.nk'.format(nuke.NUKE_VERSION_MAJOR, nuke.NUKE_VERSION_MINOR)

    preferencesNode = nuke.toNode('preferences')

    customPrefences = preferencesNode.writeKnobs( nuke.WRITE_USER_KNOB_DEFS | nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT | nuke.TO_VALUE )
    customPrefences = customPrefences.replace('\n','\n  ')

    preferencesCode = 'Preferences {\n inputs 0\n name Preferences%s\n}' %customPrefences

    # write to file
    openPreferencesFile = open( preferencesFile , 'w' )
    openPreferencesFile.write( preferencesCode )
    openPreferencesFile.close()

def deletePreferences():
    '''
    Delete all the W_hotbox related items in the properties panel.
    '''

    firstLaunch = True
    for i in preferencesNode.knobs().keys():
        if 'pb' in i:
            preferencesNode.removeKnob(preferencesNode.knob(i))
            firstLaunch = False

    #remove TabKnob
    try:
        preferencesNode.removeKnob(preferencesNode.knob('pbLabel'))
    except:
        pass

    if not firstLaunch:
        savePreferencesToFile()

def addPreferences():
    '''
    Add knobs to the preferences needed for this module to work properly.
    '''
    
    addToPreferences(nuke.Tab_Knob('pbLabel','pbTools'))
    addToPreferences(nuke.Text_Knob('pbGeneralLabel','<b>pb Tools</b>'))

    #Launch Label knob
    addToPreferences(nuke.Text_Knob('hotboxLaunchLabel','<b>Launch</b>'))

    #shortcut knob
    knob = nuke.String_Knob('hotboxShortcut','Shortcut')
    knob.setValue('`')

    tooltip = ("The key that triggers the Hotbox. Should be set to a single key without any modifier keys. "
                "Spacebar can be defined as 'space'. Nuke needs be restarted in order for the changes to take effect.")

    addToPreferences(knob, tooltip)
    global shortcut
    shortcut = preferencesNode.knob('hotboxShortcut').value()

    #reset shortcut knob
    knob = nuke.PyScript_Knob('hotboxResetShortcut','set', 'W_hotbox.resetMenuItems()')
    knob.clearFlag(nuke.STARTLINE)
    tooltip = "Apply new shortcut."

    addToPreferences(knob, tooltip)

    #hide the iconLocation knob if environment varible called 'W_HOTBOX_HIDE_ICON_LOC' is set to 'true' or '1'
    preferencesNode.knob('hotboxIconLocation').setVisible(True)
    if 'W_HOTBOX_HIDE_ICON_LOC' in os.environ.keys():
        if os.environ['W_HOTBOX_HIDE_ICON_LOC'].lower() in ['true','1']:
            preferencesNode.knob('hotboxIconLocation').setVisible(False)

    savePreferencesToFile()

def updatePreferences():
    '''
    Check whether the hotbox was updated since the last launch. If so refresh the preferences.
    '''

    allKnobs = preferencesNode.knobs().keys()

    #Older versions of the hotbox had a knob called 'iconLocation'.
    #This was a mistake and the knob was supposed to be called
    #'hotboxIconLocation', similar to the rest of the knobs.

    forceUpdate = False

    if 'iconLocation' in allKnobs and 'hotboxIconLocation' not in allKnobs:

        currentSetting = preferencesNode.knob('iconLocation').value()

        #delete 'iconLocation'
        preferencesNode.removeKnob(preferencesNode.knob('iconLocation'))

        #re-add 'hotboxIconLocation'
        iconLocationKnob = nuke.File_Knob('hotboxIconLocation','Icons location')
        iconLocationKnob.setValue(currentSetting)
        addToPreferences(iconLocationKnob)

        forceUpdate = True

    allKnobs = preferencesNode.knobs().keys()
    proceedUpdate = True

    if 'hotboxVersion' in allKnobs or forceUpdate:

        if not forceUpdate:
            try:
                if float(version) == float(preferencesNode.knob('hotboxVersion').value()):
                    proceedUpdate = False
            except:
                proceedUpdate = True

        if proceedUpdate:
            currentSettings = {knob:preferencesNode.knob(knob).value() for knob in allKnobs if knob.startswith('hotbox') and knob != 'hotboxVersion'}

            #delete all the preferences
            deletePreferences()

            #re-add all the knobs
            addPreferences()

            #restore
            for knob in currentSettings.keys():
                try:
                    preferencesNode.knob(knob).setValue(currentSettings[knob])
                except:
                    pass

            #save to file
            savePreferencesToFile()

    # nuke 12.2v4 and 13 bug. The last tab wont be shown. Workaround is to add an extra tab
    customTabs = [k.name() for k in preferencesNode.knobs().values() if isinstance(k, nuke.Tab_Knob)]
    if customTabs and customTabs[-1] == 'hotboxLabel':

        # make new tab and hide it
        dummyTab = nuke.Tab_Knob('hotboxDummyTab', 'Dummy')
        dummyTab.setFlag(0x00040000)

        addToPreferences(dummyTab)




#add knobs to preferences
preferencesNode = nuke.toNode('preferences')
homeFolder = os.getenv('HOME').replace('\\','/') + '/.nuke'

#updatePreferences()
addPreferences()