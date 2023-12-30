#############################################################
#################SPEEDY SCRIPT V1.0##########################
#################by Andrea Geremia###########################
###############www.andreageremia.it##########################
#############################################################

import os
import nuke, nukescripts
import webbrowser

try:
  from PySide.QtGui import QApplication
except:
  from PySide2.QtWidgets import QApplication


#------------------------------------------------------------------------------------
#READ RECENT SCRIPTS

with open(os.path.expanduser('~/.nuke/recent_files'), 'r') as _fileHandle:
    my_file_contents = _fileHandle.read()
    li = list(my_file_contents.split("\n"))
    li = [item.replace('"', '') for item in li]
    #print li


#------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------

class SpeedyScriptPanel(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__(self, 'Speedy Script', 'com.ohufx.SpeedyScript')
        

        # CREATE KNOBS in the Panel
        
        # IMPORT
        self.ImportTab = nuke.Tab_Knob('importTab', 'Import')
        self.textImport = nuke.Text_Knob("textImport", "", "<i>Import a script into a Group.<br/> Below there are 4 different ways to select the file")
        self.openGroup = nuke.Boolean_Knob("openGroup", "Open Group automatically when imported")
        self.openGroup.setFlag(nuke.STARTLINE)
        self.localizationPause = nuke.Boolean_Knob("localizationPause", "Pause Localization")
        self.localizationPause.setFlag(nuke.STARTLINE)
        
        self.textFileBrowser = nuke.Text_Knob("File_Browser","<font color='lime'>File Browser:")
        self.importScript = nuke.PyScript_Knob('importScript', "<b><font color='lime'>Import Script/Gizmo in Group")
        #self.importScript.setFlag(nuke.STARTLINE)
        #self.openScript = nuke.PyScript_Knob('openScript', 'Open Script/Gizmo')
        
        
        self.divider = nuke.Text_Knob("divider","")
        self.textFilePath = nuke.Text_Knob("File Path", "<font color='deeppink'>File Path:")
        self.importStr = nuke.String_Knob('importStr', '')
        self.importStr.setValue("Insert here the path like      example/example/file.nk")
        self.ImportFrom = nuke.PyScript_Knob('importFrom', "<b><font color='deeppink'>Import from Path in Group")


        self.divider2 = nuke.Text_Knob("divider2","")
        self.textFileRecent = nuke.Text_Knob("Recent Files", "<font color='gold'>Recent Files:")
        self.recentComp = nuke.Enumeration_Knob('recent', "", li)
        self.importRecent = nuke.PyScript_Knob('importRecent', "<b><font color='gold'>Import Recent Script in Group")


        self.divider4 = nuke.Text_Knob("divider4","")
        self.textOtherVersion = nuke.Text_Knob("Other Version","<font color='deepSkyBlue'>Other Version:")
        self.importOtherVers = nuke.PyScript_Knob('importOtherVers', "<b><font color='deepSkyBlue'>Import another version of this script in Group")

        self.divider5 = nuke.Text_Knob("divider5","")
        self.findGroup = nuke.PyScript_Knob('findGroup', "Find Group")

        # EXPORT
        self.ExportTab = nuke.Tab_Knob('exportTab', "Export")
        self.textExport = nuke.Text_Knob("textExport", "", "<i><font color='lightcyan'>Select a gizmo/node and export it")
        self.divider3 = nuke.Text_Knob("divider3","")
        self.nodesChoice = nuke.Enumeration_Knob('nodes', '<font color="cyan">Output format', ['Group .gizmo', 'Nuke File .nk'])
        self.exportScript = nuke.PyScript_Knob('exportScript', "<b><font color='cyan'>Export Gizmo")
        #self.exportScript.setFlag(nuke.STARTLINE)
        
        
        
        # OTHER
        self.OtherTab = nuke.Tab_Knob('otherTab', "...bonus Feature")
        self.textOther = nuke.Text_Knob("textOther", "", "<i>Import the Nuke script which created the relative Read node")
        self.infoOther = nuke.PyScript_Knob('infoOther', "<i>?")
        self.infoOther.setFlag(nuke.STARTLINE)
        self.exampleOther = nuke.PyScript_Knob('exampleOther', "<i>Import example")
        self.divider6 = nuke.Text_Knob("divider6","")
        self.textMetadata = nuke.Text_Knob("textMetadata","<font color='indianRed'>Create Metadata:")
        self.createMetadata = nuke.PyScript_Knob('createMetadata', "<b><font color='indianRed'>Create Metadata node")
        self.divider7 = nuke.Text_Knob("divider7","")
        self.textReadNodes = nuke.Text_Knob("textReadNodes","<font color='crimson'>Create Button in every Read Node :")
        self.createReadNodes = nuke.PyScript_Knob('createReadNodes', "<b><font color='crimson'>Create button in Read Node")
        
        SS_path = os.path.dirname(__file__) + "/icon/SpeedyScript_text.png"
        
        self.credits = nuke.Text_Knob("credits", "", '<img src="'+ SS_path + '" width=120>' "<b><font size='2' color='red'>v1.1</font></b><br><font size='0.5' color='white'><i>by Andrea Geremia</i><br><br>andrea.geremia89@gmail.com<br>www.andreageremia.it</font>")
        #self.credits = nuke.Text_Knob("credits", "", '<img src="/Users/gere/.nuke/SpeedyScript/icon/SpeedyScript_text.png" width=120>' "<b><font size='2' color='red'>v1.0</font></b><br><font size='0.5' color='white'><i>by Andrea Geremia</i><br><br>andrea.geremia89@gmail.com<br>www.andreageremia.it</font>")
        #self.credits = nuke.Text_Knob("credits", "", '<img src="/Users/gere/.nuke/SpeedyScript/icon/SpeedyScript_text.png" width=100>' "<b><font size='2' color='red'>Speedy Script for Nuke v1.0</font></b><br><font size='0.5' color='white'><i>by Andrea Geremia</i><br><br>andrea.geremia89@gmail.com<br>www.andreageremia.it</font>")
        self.info = nuke.PyScript_Knob('info', "<i>?")
        self.www = nuke.PyScript_Knob('www', "<i>www")

 
        
        # ADD KNOBS
        self.addKnob(nuke.BeginTabGroup_Knob())

        #IMPORT
        self.addKnob(self.ImportTab)
        
        self.addKnob(self.textImport)
        
        self.openGroup.setValue(True)
        self.addKnob(self.openGroup)
        self.openGroup.setTooltip("Open group automatically when it's imported in the script. Otherwise you can open it manually")
        
        self.localizationPause.setValue(False)
        self.addKnob(self.localizationPause)
        self.localizationPause.setTooltip("When group is imported, put Localization on Pause if this is checked")
        
        self.addKnob(self.textFileBrowser)
        self.addKnob(self.importScript)
        
        self.addKnob(self.divider4)
        self.addKnob(self.textOtherVersion)
        self.addKnob(self.importOtherVers)
        
        #self.addKnob(self.openScript)
        self.addKnob(self.divider)
        self.addKnob(self.textFilePath)
        self.addKnob(self.importStr)
        self.addKnob(self.ImportFrom)
        self.addKnob(self.divider2)

        self.addKnob(self.textFileRecent)
        self.addKnob(self.recentComp)
        self.addKnob(self.importRecent)
        
        self.importScript.setTooltip("Import a file .nk or gizmo into a Group. Select it from a pop-up window")
        self.importOtherVers.setTooltip("Import another version of this script. It will pop-up automatically folder script")
        self.ImportFrom.setTooltip("Import the script from the inserted path")
        self.importRecent.setTooltip("Select a script from the list of the 'Recent projects'")

        self.addKnob(self.divider5)
        self.addKnob(self.findGroup)
        self.findGroup.setTooltip("Check if in the script you have a Group")
        
        
        
		#EXPORT
        self.addKnob(self.ExportTab)
        self.ExportTab.setTooltip("Select a node/group in the Node Graph, choose the format of export and click on this button. It will export the node without all the annoying strings from Nuke")
        
        self.addKnob(self.textExport)
        self.addKnob(self.divider3)
        self.addKnob(self.nodesChoice)
        self.addKnob(self.exportScript)
        
        self.nodesChoice.setTooltip("Select the format: gizmo or nk")
        self.exportScript.setTooltip("Export a Gizmo in the cleaner way: it will delete automatically the first lines, convert Gizmo into Group and rename the node")
        
        
        #OTHER
        self.addKnob(self.OtherTab)
        self.addKnob(self.textOther)
        self.addKnob(self.infoOther)
        self.addKnob(self.exampleOther)
        self.addKnob(self.divider6)
        self.addKnob(self.textMetadata)
        self.addKnob(self.createMetadata)
        self.addKnob(self.divider7)
        self.addKnob(self.textReadNodes)
        self.addKnob(self.createReadNodes)
        
        self.exampleOther.setTooltip("Import an example of this feature. You will see how it works with the Write and Read nodes")
        self.createMetadata.setTooltip("Create the Metadata node, so you can put it directly above the Write node")
        self.createReadNodes.setTooltip("If your Read Nodes have the correct metadata, you will find a new Tab 'Import Script' where you can import the relative script directly from the Read Node")

        self.addKnob(nuke.EndTabGroup_Knob())



        #INFO
        self.addKnob(self.credits)
        self.addKnob(self.info)
        self.addKnob(self.www)
        self.www.setTooltip("Check tutorial on the net")

#################################################################################
#################################################################################

    #if something is clicked
    def knobChanged(self, knob):
        if knob is self.importScript:
            filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo')
            if filePath is not None:
                self.importScriptFunction(filePath)


        if knob is self.ImportFrom:
        	if self.importStr.value() != "":
	            filePath = os.path.normpath(str(self.importStr.value()))
	            
	            #check if file exists
	            if os.path.isfile(filePath):
	            	self.importScriptFunction(filePath)
	            else:
		        	#If file has not been found, ask to look for it
		            if nuke.ask('Impossible to find the script in the original position: ' + filePath + '\nDo you want to look for the file?'):
		                filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo')
		                #If user select a file
		                if filePath is not None:
		                    self.importScriptFunction(filePath)
        	else:
	            nuke.message("Insert a valid path")


        if knob is self.importRecent:
            filePath = os.path.normpath(str(self.recentComp.value()))
            
            #check if file exists
            if os.path.isfile(filePath):
            	self.importScriptFunction(filePath)
            else:
				#If file has not been found, ask to look for it
	            if nuke.ask('Impossible to find the script in the original position: ' + filePath + '\nDo you want to look for the file?'):
	                filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo')
	                #If user select a file
	                if filePath is not None:
	                    self.importScriptFunction(filePath)

            
        if knob is self.importOtherVers:
            file = nuke.root().knob('name').value()
            if file != "":
                current_directory = os.path.normpath(os.path.split(file)[0]).replace("\\", "/") + "/"
            else:
                current_directory = ""
                nuke.message("If you want to select another version of the current script, you have to save it before!")

            filePath = nuke.getFilename('Get a Nuke File', '*.nk *.gizmo', current_directory)
            if filePath is not None:
                self.importScriptFunction(filePath)   

        if knob is self.exportScript:
            self.exportScriptFunction()
            
            
            
            
            
            
        if knob is self.infoOther:    
            nuke.message("<b>In this Tab you can render in the Metadata of your EXR files the path of the script which created that footage.\nIn this way you can have a Button directly in each Read node in order to import directly the relative script\n\n\n- METADATA: Add this metadata before your write node. It will work only with EXR format and remember to render out 'ALL METADATA' \n\n\n-BUTTON: this button will check all the Read Nodes in your script and if they have the right Metadata, it will add the Button to import the script directly from the node")
        
        if knob is self.exampleOther:
            self.exampleOtherFunction()
        
        if knob is self.createReadNodes:
            self.createReadNodesFunction()
        
        if knob is self.createMetadata:
            self.createMetadataFunction()
            
            
            
            
        if knob is self.findGroup:
            self.findGroupFunction()    
        
        if knob is self.info:
            nuke.message("<b>- IMPORT: import an entire script inside a Group node. You will save RAM because you don't need to open a new istance of Nuke and your script it is gonna be more clean \n\n\n-EXPORT: export your gizmo directly in .gizmo or .nuke files, replacing the Gizmo with Group and deleting 'set cut_paste_input', 'version' and 'push $cut_paste_input'")

        if knob is self.www:
            webbrowser.open('http://www.andreageremia.it/tutorial_importexport.html') 

    #----------------------------------------------------------------------------------------
    #IMPORT SCRIPT INTO GROUP
    def importScriptFunction(self, filePath):
        
        fileName = (os.path.basename(filePath))
        size = os.path.getsize(filePath)
        sizeMB = size/(1024*1024)
        
        import_ok = True
        
        #if file is bigger than 8MB, give a message
        if size > 8000000:
            import_ok = False
            if nuke.ask("File is quite BIG, " + str(sizeMB) + "MB and importing could take some seconds. \nDo you want to continue? \nIn case, don't close Nuke or move anything"):
                import_ok = True
            
        if import_ok == True:

            #LOCALIZATION PAUSE
            if (self.localizationPause.getValue() == True):
                nuke.localization.pauseLocalization()
        
            #CREATE GROUP
            group = nuke.createNode("Group")
            
            #CUSTOMIZE NODE
            fileName = fileName.replace('.nk','')
            fileName = fileName.replace(' ','_')
            
            group.knob('name').setValue("SCRIPT_IMPORTED_" + fileName)
            #group.knob('label').setValue(fileName + '\n' + filePath)
            group.knob('label').setValue(filePath)
            group.knob('note_font_size').setValue(20)
            group.knob('tile_color').setValue(0x99000000)
            group.knob('note_font_color').setValue(4294967041)
            group.knob('note_font').setValue("bold")

            groupNode = nuke.toNode(group.name())
            groupNode.begin()
            nuke.nodePaste(filePath)
            groupNode.end()
            
            #OPEN GROUP
            if (self.openGroup.getValue() == True):
                nuke.showDag(groupNode)


    #--------------------------------------------------------------------
    #EXPORT GIZMO INTO GROUP
    def exportScriptFunction(self):
        nodes = nuke.selectedNodes()    # GET SELECTED NODES
        amount = len( nodes )    # GET NUMBER OF SELECTED NODES
        
        
        if amount == 1:
            node = nuke.selectedNode()
            xPos = node.xpos()
            yPos = node.ypos()
        
            filePath = nuke.getFilename('Enter Path and save Gizmo', '*.nk *.gizmo')
            
            if filePath is not None:
                fileName = (os.path.basename(filePath))
                
                #check format
                if (self.nodesChoice.value() == "Group .gizmo"):
                    formato = ".gizmo"
                else:
                    formato = ".nk"


                #if user doesn't put the extension
                if not (filePath.endswith(".nk") or filePath.endswith(".gizmo")):
                    filePath = filePath + formato
                
                
                
                #SAVE FILE
                nuke.nodeCopy(filePath)
                #nuke.nodeCopy("%clipboard%")
                
                
                data = ""
                with open(filePath, "r") as f:
                    data = f.read()
                
                #check name
                try:
                    nodeName = str(node['name'].getValue())
                    nodeName = nodeName.replace(" ", "_")   #remove spaces with underscore
                    head, tail = os.path.split(filePath)
                    fileName, extension = os.path.splitext(tail)
                    fileName = fileName.replace(" ", "_")    #remove spaces with underscore
                    if fileName != nodeName:
                        if nuke.ask("FileName and NodeName are different. Do you want to change the NodeName as '" + fileName + "' ?"):
                            data = data.replace("name " + nodeName + "\n", "name " + fileName + "\n", 1)
                except:
                    print("Error with the Name during the export")
                    
                
                #check if I have to delete 2 or 3 lines
                if "push $cut_paste_input" in data:
                    data = data.split("\n",3)[3]
                else:
                    data = data.split("\n",2)[2]
    
                #replace gizmo with group
                #data = data.replace("Gizmo { \n", "Group { \n", 1)
                data = data.replace("Gizmo", "Group", 1)
    
                #delete just the first line who contains "xpos" and "ypos"
                data = data.replace(" xpos " + str(xPos) + "\n", "", 1)
                data = data.replace(" ypos " + str(yPos) + "\n", "", 1)
        
                with open(filePath, "w") as f:
                    f.write(data)
        
        else:
            nuke.message("Select only one node")

#--------------------------------------------------------------------
    #FIND GROUP IN MY SCRIPT
    def findGroupFunction(self):
        found = False

        #deselect all Nodes
        nuke.selectAll()
        nuke.invertSelection()

        #look for Groups start with "SCRIPT_IMPORTED"
        for node in nuke.allNodes():
            nodeClass = node.Class()
            nodeName =  str(node['name'].getValue())
            print(nodeName)

            if nodeClass == "Group" and nodeName.startswith("SCRIPT_IMPORTED"):
                node.setSelected(True)
                nuke.zoom( 2, [ node.xpos(), node.ypos() ])
                found = True
                break

        if found == False:
            nuke.message("No Imported Script into Group has been found!")

#--------------------------------------------------------------------
    #IMPORT EXAMPLE
    def exampleOtherFunction(self):
    
        # var that points to the folder that this init file lives in
        SS_path = os.path.dirname(__file__)
    
        nuke.nodePaste(os.path.join(SS_path + "/example/SpeedyScript_test.nk"))


#--------------------------------------------------------------------
    #CREATE METADATA NODE
    def createMetadataFunction(self):
        
        # var that points to the folder that this init file lives in
        SS_path = os.path.dirname(__file__)
        
        nuke.nodePaste(os.path.join(SS_path + "/elements/metadataSpeedyScript.nk"))
        
        nuke.message("Put the metadata node just before your write node.\nIt works only with EXR format and remember to render our 'all metadata'")

#--------------------------------------------------------------------

    #CREATE BUTTON IN THE READ NODES
    def createReadNodesFunction(self):
        
        #import ReadNodes_ImportScript
        
        metad = 'exr/nuke/script/script' #'exr/nuke/script/script'
        
        
        #CREATE KNOBS
        tabKnob = nuke.Tab_Knob('Import Script')
        importKnob = nuke.PyScript_Knob("Import Script into Group","<font color='red'>Import Script into Group","import ReadNodes_ImportScript \nReadNodes_ImportScript.getScriptPath()")
        openKnob= nuke.PyScript_Knob("Open Script","<font color='deepskyblue'>Open Script","import ReadNodes_ImportScript \nReadNodes_ImportScript.OpenScript()")
        dividerKnob = nuke.Text_Knob("divider","")
        
        
        nodes = nuke.allNodes()
	 
        for n in nodes:
            if n.Class() == "Read":
                #ADD KNOBS ONLY IF METADATA EXISTS
                if n.metadata(metad) != None:
                    n.addKnob(tabKnob)

                    #since metadata exists, I create the String_Knob with the path
                    stringKnob = nuke.String_Knob('pathScript', 'Path Script:', n.metadata(metad))
                    n.addKnob(stringKnob)
                    n.addKnob(dividerKnob)
                    n.addKnob(importKnob)
                    n.addKnob(openKnob)

                    #add Tooltip for the buttons
                    n.knob("Import Script").setTooltip("Import relative script where this sequence has been created")
                    n.knob("Open Script").setTooltip("Open in a new Nuke instance, the script where this sequence has been created")
                    
        nuke.message("Check your Read Node. If they have the right metadata, you will find the new tab 'Import Script'")

#################################################################
def addSSPanel():
    global ssPanel
    ssPanel = SpeedyScriptPanel()
    return ssPanel.addToPane()
