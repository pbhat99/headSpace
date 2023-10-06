# dot create and align tool
nuke.menu('Nuke').addCommand('-{ pb }-/NodeGraph/Align Dots', "import AlignDots ; AlignDots.AlignDots()", 'Shift+.', shortcutContext=2, icon='pbicon.png')