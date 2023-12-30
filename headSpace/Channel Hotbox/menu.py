#Channel Hotbox
mainMenu = os.path.dirname(__file__).split('/')[-2]

nuke.menu("Nuke").addCommand(mainMenu + '/Channel HotBox', 'import channel_hotbox ; channel_hotbox.start()', 'alt+q', icon='pbicon.png')