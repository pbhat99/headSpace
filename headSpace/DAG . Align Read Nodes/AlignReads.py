# ------------------------------
# sbnAlignReadNodes_2020 v1.13
# ------------------------------
# AUTHOR:
#    Sebastian Faber (2020), Hamburg, Senior Nuke-Compositor & 3D-Artist   
#    sebastian.cg.faber@gmx.de
# 
# DESCRIPTION:
#   - this script aligns selected read nodes in the node graph editor of the foundry's nuke. 
#   - read nodes are sorted by name and aligned in horizontal, zig zag or in vertical direction
#
# MENU.PY:
# # e.g.
# global glToggleRS; glToggleRS
# m=nuke.menu('Nodes').addMenu("sbn")
# m.addCommand( ".Align Read Nodes  "            , "nuke.load('sbnAlignReadNodes_2020.py'), sbnAlignNodes('default')", "L", shortcutContext=2)
# m.addCommand( ".Align Read Nodes (vertical)"   , "nuke.load('sbnAlignReadNodes_2020.py'), sbnAlignNodes('vertical')", "shift+L", shortcutContext=2)
# m.addCommand( ".Align Read Nodes (horizontal)" , "nuke.load('sbnAlignReadNodes_2020.py'), sbnAlignNodes('horizontal')", "", shortcutContext=2)
# m.addCommand( ".Align Read Nodes (wave)"       , "nuke.load('sbnAlignReadNodes_2020.py'), sbnAlignNodes('wave')", "", shortcutContext=2)
# m.addCommand( ".Align Read Nodes (zigzag)"     , "nuke.load('sbnAlignReadNodes_2020.py'), sbnAlignNodes('zigzag')", "", shortcutContext=2)
# 
# USAGE:
#   Select your read nodes then 
#     press "L"            for horizontal and zig zag alignement (remember 'L' is a toggle)
#     press "L"+ shift     for vertical alignment
#
# COMMENT:
#   Performance version
# 
# SPECIAL THANKS:
#   Thanks to Johan Van Huyssteen for his suggestions and bugreporting
#
# VERSIONS:
#   Tested on Nuke 11.x and Nuke 12.x (Windows 10)
#
# DATE: 
#   17.02.2020 -- fixing Issue: 'L' shortcut do not overwrite 'L'- in the viewer playback (Thanks to Johan for this hint)
#   22.12.2019 -- fixing minor issues
#   12.12.2019 -- Changing installation
# ------------------------------------------------------------------------------------------------

import nuke
#global glToggleRS; glToggleRS
glToggleRS = 0


def getBaseName(sFullFileName):
   aSplit=sFullFileName.split("/")[-1:]   
   return(aSplit[0])
   
def sbnAlignNodes(sMode):
   from operator import itemgetter
   global glToggleRS
   aList=[]  
   i=0; xpos=0; ypos=0    
   oNodesReader = nuke.selectedNodes("Read")
   oNodes = nuke.selectedNodes()
   
   if len(oNodes)==0:      
      return()

   if len(oNodesReader)!=len(oNodes):     
      for oNode in oNodes:              
         oNode.autoplace()
      return()
      
   for oNode in oNodes:
      if oNode.Class() == "Read":             
         sNodeName=oNode.name()         
         sFile=oNode['file'].getValue()
         sBaseName=getBaseName(sFile)         
         xpos = oNode.xpos()   
         ypos = oNode.ypos()    

         #-------------0,----1----,----2-----,---3--,--4--,--5,--
         aList.append([i,sBaseName, sNodeName, sFile, xpos, ypos])
         i=i+1
   
   # do sort
   aListSortedBasename=sorted(aList, key=itemgetter(1))
   aListSortedXPos=sorted(aList, key=itemgetter(4))
   aListSortedYPos=sorted(aList, key=itemgetter(4,5))
   
   xpos=aListSortedXPos[0][4]
   ypos=aListSortedYPos[0][5]
   yposStart=ypos
   
   # default - toggle mode
   if sMode=="default": 
      if (glToggleRS==0):
         sMode="horizontal"
         
      if (glToggleRS==1):            
         sMode="zigzag"      
         glToggleRS=-1         
            
      if (glToggleRS==2):            
         sMode="vertical"
         glToggleRS=-1
      glToggleRS=glToggleRS+1     

   for oItem in aListSortedBasename:      
      oNode = nuke.toNode( oItem[2] )
      oNode.knob('selected').setValue(True)
      oNode.setXYpos(xpos, ypos)

      # horizontal
      if sMode=="horizontal": xpos=xpos+100   

      # vertical
      if sMode=="vertical":   ypos=ypos+100

      # vertical zigzag 
      if sMode=="zigzag":   
         xpos=xpos+100  
         ypos=ypos-50
         if ypos < (yposStart-50): ypos=yposStart
      
      # vertical wave
      if sMode=="wave":   
         import math
         iOffset=int((math.sin(xpos))*100)         
         xpos=xpos+100  
         ypos=ypos+iOffset
