#==========================================================================================
# Script : deleteGroupViewers.py
#------------------------------------------------------------------------------------------
# Written by Fynn Laue
# to delete viewers located inside group nodes.
#==========================================================================================

import nuke
def delViewers():
# Deletes all viewers inside groups
	#variables for result logging
	class log:
		groups = 0
		viewers = 0
		deletedViewers = 0
	self = log
	nodes = nuke.allNodes()
	def nextlevel(self,node):
		self.groups+=1 #increments groups because this function only gets called when a group is found
		# 1) loop through all nodes and delete viewers.
		# 2) loop through all nodes again and go inside groups this time.
		for n in node.nodes():
			if n.Class() == "Viewer":
				nuke.delete(n)
				self.deletedViewers+=1
		for m in node.nodes():
			if m.Class() =="Group":
				nextlevel(self,m) #makes this function reference itself to go into the current group node

	###   S T A R T   H E R E   ###
	# 1) Go through all nodes and inside groups
	# 2) Go through all nodes and count viewers
	for node in nodes:
		if node.Class() == "Group":
			nextlevel(self,node)
		elif node.Class() == "Viewer":
			self.viewers+=1

	# Show Results
	def decode(list):
		output = '\r'
		for item in list:
			output = output+'\n'+str(''.join(str(e) for e in item))
		return output

	msg1 =  "Deleted ",self.deletedViewers," viewer(s) in ",self.groups," group(s)."
	msg2 =  self.viewers, ' viewer(s) remaining in main comp window.'
	messages = [msg1,msg2]
	nuke.message(decode(messages))
	print (decode(messages))

