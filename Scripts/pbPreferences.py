#----------------------------------------------------------------------------------------------------------
# pb Preferences
#----------------------------------------------------------------------------------------------------------

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
        if 'hotbox' in i:
            preferencesNode.removeKnob(preferencesNode.knob(i))
            firstLaunch = False

    #remove TabKnob
    try:
        preferencesNode.removeKnob(preferencesNode.knob('hotboxLabel'))
    except:
        pass

    if not firstLaunch:
        savePreferencesToFile()

def addPreferences():
    '''
    Add knobs to the preferences needed for this module to work properly.
    '''
    
    addToPreferences(nuke.Tab_Knob('hotboxLabel','W_hotbox'))
    addToPreferences(nuke.Text_Knob('hotboxGeneralLabel','<b>General</b>'))

    #version knob to check whether the hotbox was updated
    knob = nuke.String_Knob('hotboxVersion','version')
    knob.setValue(version)
    addToPreferences(knob)
    preferencesNode.knob('hotboxVersion').setVisible(False)

    #location knob
    knob = nuke.File_Knob('hotboxLocation','Hotbox location')

    tooltip = "The folder on disk the Hotbox uses to store the Hotbox buttons. Make sure this path links to the folder containing the 'All','Single' and 'Multiple' folders."

    locationKnobAdded = addToPreferences(knob, tooltip)

    #icons knob
    knob = nuke.File_Knob('hotboxIconLocation','Icons location')
    knob.setValue(homeFolder +'/icons/W_hotbox')

    tooltip = "The folder on disk the where the Hotbox related icons are stored. Make sure this path links to the folder containing the PNG files."
    addToPreferences(knob, tooltip)

    #open manager button
    knob = nuke.PyScript_Knob('hotboxOpenManager','open hotbox manager','W_hotboxManager.showHotboxManager()')
    knob.setFlag(nuke.STARTLINE)

    tooltip = "Open the Hotbox Manager."

    addToPreferences(knob, tooltip)

    #open in file system button knob
    knob = nuke.PyScript_Knob('hotboxOpenFolder','open hotbox folder','W_hotbox.revealInBrowser(True)')

    tooltip = "Open the folder containing the files that store the Hotbox buttons. It's advised not to mess around in this folder unless you understand what you're doing."

    addToPreferences(knob, tooltip)

    #delete preferences button knob
    knob = nuke.PyScript_Knob('hotboxDeletePreferences','delete preferences','W_hotbox.deletePreferences()')

    tooltip = "Delete all the Hotbox related knobs from the Preferences Panel. After clicking this button the Preferences Panel should be closed by clicking the 'cancel' button."

    addToPreferences(knob, tooltip)

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

    #trigger mode knob
    knob = nuke.Enumeration_Knob('hotboxTriggerDropdown', 'Launch mode',['Press and Hold','Single Tap'])

    tooltip = ("The way the hotbox is launched. When set to 'Press and Hold' the Hotbox will appear whenever the shortcut is pressed and disappear as soon as the user releases the key. "
                "When set to 'Single Tap' the shortcut will toggle the Hotbox on and off.")

    addToPreferences(knob, tooltip)

    #close on click
    knob = nuke.Boolean_Knob('hotboxCloseOnClick','Close on button click')
    knob.setValue(False)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Close the Hotbox whenever a button is clicked (excluding submenus obviously). This option will only take effect when the launch mode is set to 'Single Tap'."

    addToPreferences(knob, tooltip)

    #execute on close
    knob = nuke.Boolean_Knob('hotboxExecuteOnClose','Execute button without click')
    knob.setValue(False)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Execute the button underneath the cursor whenever the Hotbox is closed."

    addToPreferences(knob, tooltip)

    #Rule/Class order
    knob = nuke.Enumeration_Knob('hotboxRuleClassOrder', 'Order',['Class - Rule', 'Rule - Class'])
    tooltip = "The order in which the buttons will be loaded."

    addToPreferences(knob, tooltip)

    #Manager startup default
    knob = nuke.Enumeration_Knob('hotboxOpenManagerOptions', 'Manager startup default',['Contextual','All','Rules', 'Contextual/All', 'Contextual/Rules'])
    knob.clearFlag(nuke.STARTLINE)

    tooltip = ("The section of the Manager that will be opened on startup.\n"
                "\n<b>Contextual</b> Open the 'Single' or 'Multiple' section, depending on selection."
                "\n<b>All</b> Open the 'All' section."
                "\n<b>Rules</b> Open the 'Rules' section."
                "\n<b>Contextual/All</b> Contextual if the selection matches a button in the 'Single' or 'Multiple' section, otherwise the 'All' section will be opened."
                "\n<b>Contextual/Rules</b> Contextual if the selection matches a button in the 'Single' or 'Multiple' section, otherwise the 'Rules' section will be opened.")

    addToPreferences(knob, tooltip)

    #Appearence knob
    addToPreferences(nuke.Text_Knob('hotboxAppearanceLabel','<b>Appearance</b>'))

    #color dropdown knob
    knob = nuke.Boolean_Knob('hotboxMirroredLayout', 'Mirrored')

    tooltip = ("By default the contextual buttons will appear at the top of the hotbox and the non contextual buttons at the bottom.")

    addToPreferences(knob, tooltip)

    #color dropdown knob
    knob = nuke.Enumeration_Knob('hotboxColorDropdown', 'Color scheme',['Maya','Nuke','Custom'])

    tooltip = ("The color of the buttons when selected.\n"
                "\n<b>Maya</b> Autodesk Maya's muted blue."
                "\n<b>Nuke</b> Nuke's bright orange."
                "\n<b>Custom</b> which lets the user pick a color.")

    addToPreferences(knob, tooltip)

    #custom color knob
    knob = nuke.ColorChip_Knob('hotboxColorCustom','')
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "The color of the buttons when selected, when the color dropdown is set to 'Custom'."

    addToPreferences(knob, tooltip)

    #hotbox center knob
    knob = nuke.Boolean_Knob('hotboxColorCenter','Colorize hotbox center')
    knob.setValue(True)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Color the center button of the hotbox depending on the current selection. When unticked the center button will be colored a lighter tone of grey."

    addToPreferences(knob, tooltip)

    #auto color text
    knob = nuke.Boolean_Knob('hotboxAutoTextColor','Auto adjust text color')
    knob.setValue(True)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "Automatically adjust the color of a button's text to its background color in order to keep enough of a difference to remain readable."

    addToPreferences(knob, tooltip)

    #fontsize knob
    knob = nuke.Int_Knob('hotboxFontSize','Font size')
    knob.setValue(8)

    tooltip = "The font size of the text that appears in the hotbox buttons, unless defined differently on a per-button level."

    addToPreferences(knob, tooltip)

    #fontsize manager's script editor knob
    knob = nuke.Int_Knob('hotboxScriptEditorFontSize','Font size script editor')
    knob.setValue(11)
    knob.clearFlag(nuke.STARTLINE)

    tooltip = "The font size of the text that appears in the hotbox manager's script editor."

    addToPreferences(knob, tooltip)

    addToPreferences(nuke.Text_Knob('hotboxItemsLabel','<b>Items per Row</b>'))

    #row amount selection knob
    knob = nuke.Int_Knob('hotboxRowAmountSelection', 'Selection specific')
    knob.setValue(3)

    tooltip = ("The maximum amount of buttons a row in the upper half of the Hotbox can contain. "
                "When the row's maximum capacity is reached a new row will be started. This new row's maximum capacity will be incremented by the step size.")

    addToPreferences(knob, tooltip)

    #row amount all knob
    knob = nuke.Int_Knob('hotboxRowAmountAll','All')
    knob.setValue(3)

    tooltip = ("The maximum amount of buttons a row in the lower half of the Hotbox can contain. "
                "When the row's maximum capacity is reached a new row will be started.This new row's maximum capacity will be incremented by the step size.")

    addToPreferences(knob, tooltip)

    #stepsize knob
    knob = nuke.Int_Knob('hotboxRowStepSize','Step size')
    knob.setValue(1)

    tooltip = ("The amount a buttons every new row's maximum capacity will be increased by. "
                "Having a number unequal to zero will result in a triangular shape when having multiple rows of buttons.")

    addToPreferences(knob, tooltip)

    #spawnmode knob
    knob = nuke.Boolean_Knob('hotboxButtonSpawnMode','Add new buttons to the sides')
    knob.setValue(True)
    knob.setFlag(nuke.STARTLINE)

    tooltip = "Add new buttons left and right of the row alternately, instead of to the right, in order to preserve muscle memory."

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