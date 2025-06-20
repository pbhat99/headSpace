#############################################################
#################SPEEDY SCRIPT V1.0##########################
#################by Andrea Geremia###########################
###############www.andreageremia.it##########################
#############################################################

import os
import nuke, nukescripts
import webbrowser

#----------------------------------------------------------------------------------------
#IMPORT SCRIPT INTO GROUP
def importScriptFunction(filePath):
    
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
        nuke.showDag(groupNode)


#--------------------------------------------------------------------
#EXPORT GIZMO INTO GROUP
def exportScriptFunction():
    nodes = nuke.selectedNodes()    # GET SELECTED NODES
    amount = len( nodes )    # GET NUMBER OF SELECTED NODES
    
    
    if amount == 1:
        node = nuke.selectedNode()
        xPos = node.xpos()
        yPos = node.ypos()
    
        filePath = nuke.getFilename('Enter Path and save Gizmo', '*.nk *.gizmo')
        
        if filePath is not None:
            fileName = (os.path.basename(filePath))


            #if user doesn't put the extension
            if not (filePath.endswith(".nk") or filePath.endswith(".gizmo")):
                filePath = filePath + ".gizmo"
            
            
            
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
def findGroupFunction():
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