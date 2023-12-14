mainMenu = menuMaker()
nuke.menu("Nuke").addCommand( menuMaker() + 'New Ref Frame', 'import new_ref_frame' , icon = 'ParticleSpeedLimit.png')