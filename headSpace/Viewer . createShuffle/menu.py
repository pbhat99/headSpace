
nuke.menu('Viewer').addCommand( 'Shuffle This', 'import createShuffle ; createShuffle.createShuffleAndReset()', 'v', icon='Shuffle.png')
nuke.menu('Nodes').addCommand( "Channel/Shuffle", 'import createShuffle ; createShuffle.createShuffle()', 'v', icon='Shuffle.png')