mainMenu = menuMaker()

nuke.menu('Nuke').addCommand(mainMenu + 'Recent Files Browser', "import recent_files_browser ; recent_files_browser.open_recent_files_browser()", '', shortcutContext=2, icon='pbicon.png')