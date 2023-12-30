#v1.1 now it imports gizmo as group, autocolor was added

#this script gives you ability to create gizmos just by drop .gizmo files directly in Nuke's node graph

#installation guide:
#put this file into your home directory: 'C:\Users\user_name\.nuke'
#or you can create subdirectory and put file there: 'C:\Users\user_name\.nuke\python'
#for subdirectory working well you need to paste in init.py this line:
#nuke.pluginAddPath('./python')
#or full path:
#nuke.pluginAddPath('C:/Users/user_name/.nuke/python')
#then in your menu.py paste this line:
#import gizmoDropper

#created by Pushkarev Aleksandr
#you can contact me via pushkarevalecsandr@gmail.com

import nuke, nukescripts, os

def autocolor(name):
	preferences = nuke.toNode('preferences')
	if preferences.knob('autocolor').value():
		keywords = []
		colors = []
		for knName in list(preferences.knobs().keys()):
			if knName.startswith('NodeColourClass'):
				classes = preferences.knob(knName).value()
				if classes:
					keywords.append(classes.split())
					colors.append(preferences.knob(knName.replace('Class','')+'Color').value())
		for i, keys in enumerate(keywords):
			for key in keys:
				if name.lower().count(key.lower()):
					return 'tile_color 0x'+format(colors[i], '06x')+'\n'
	return ''


def gizmoDropper(mimeType, text):
	if mimeType=='text/plain' and text.endswith('.gizmo') and os.path.isfile(text):
		gizmo_line = 'Gizmo {\n'
		group_line = 'Group {\n'
		basename = os.path.basename(text)
		if basename=='.gizmo':
			name = 'untitled'
		else:
			name = os.path.splitext(basename)[0].replace(' ','_')

		#read gizmo file
		file = open(text)
		lines = []
		for line in file:
			lines.append(line)
		file.close()
		#change gizmo to group, and add name
		if lines.count(gizmo_line)==1:
			i = lines.index(gizmo_line)
			lines.pop(i)
			lines.insert(i,group_line)
			if name[-1].isdigit():
				lines.insert(i+1,'name '+name+'_1\n')
			else:
				lines.insert(i+1,'name '+name+'1\n')
			color = autocolor(name)
			if color:
				lines.insert(i+2,color)
		#load group
		groupText = ''
		for line in lines:
			groupText+=line
		nuke.scriptReadText(groupText)
		return True
	else:
		return False

nukescripts.addDropDataCallback(gizmoDropper)