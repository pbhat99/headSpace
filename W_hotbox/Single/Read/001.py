#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Shuffle Out
#
#----------------------------------------------------------------------------------------------------------

#for i in nuke.pluginPath():
#     print (i + '\n')

nodes = nuke.selectedNodes()
layers = []
crypto = []
for node in nodes:
   node['postage_stamp'].setValue(False)
   if node.Class() == 'Read':
    channels = node.channels()
    layers = list( set([channel.split('.')[0] for channel in channels]) )
    layers.sort()
    if 'rgba' in layers:
     layers.remove('rgba')
    for i in layers:
       if i.startswith('crypto'):
           print (i)
           crypto.append(i)

    layers = list(set(layers) - set(crypto))
    layers.sort()
    print (layers)


    for layer in layers:
       shuffleNode = nuke.nodes.Shuffle(label=layer,inputs=[node])
       shuffleNode['in'].setValue( layer )
#       shuffleNode['in2'].setValue('alpha')
#       shuffleNode['alpha'].setValue( 'red2' )
       shuffleNode['postage_stamp'].setValue(True)
    else:
      pass

    if not crypto == []:
       cryptomatte = nuke.nodes.Cryptomatte(inputs=[node])