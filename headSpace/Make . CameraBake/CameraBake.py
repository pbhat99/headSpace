import nuke
def cameraBake():
	#### by jaimex127@gmail.com ####
	
    #### get Script Name ####
    current_script = nuke.root().name()

	#### check if Script is Saved ####
		
    if  current_script == 'Root':
        nuke.message('You need to save the Script')
		
		
    else:    
        split_file_path = current_script.split('/')
        file_path_edited = split_file_path[:-1]
        join_file_path = ('/').join(file_path_edited)
		
		#### Build the FilePath where the Camera is Saved (Change this to save the Camera where you want)####
        tmpcam_filepath = join_file_path + '/camTMP.abc'
    
		#### Get the Script fps####
        current_script_fps = nuke.root().fps()
    
		#### Get all the info of the Selected Camera, Create a new one with the same values and paste the animation ####
		
        if nuke.selectedNodes('Camera2'):
            axiscamera = nuke.selectedNodes('Camera2')[0]
            axiscamera['selected'].setValue(0)
            camera = nuke.createNode('Camera2')
            camera['useMatrix'].setValue(1)
            camera['focal'].fromScript(axiscamera['focal'].toScript())
            camera['haperture'].fromScript(axiscamera['haperture'].toScript())
            camera['vaperture'].fromScript(axiscamera['vaperture'].toScript())
            camera['near'].fromScript(axiscamera['near'].toScript())
            camera['far'].fromScript(axiscamera['far'].toScript())
            
            for i in xrange(0,16):
                nuke.animation('%s.matrix.%s' % (camera['name'].value() , i), 'generate', (str(nuke.root()['first_frame'].value()), str(nuke.root()['last_frame'].value()), '1', 'y', 'parent.%s.world_matrix.%s' % (axiscamera['name'].value(),i) ))
        
		#### Create a Scene and things needed to Export the Camera ####   
		
            scene = nuke.createNode('Scene')
            wg = nuke.createNode('WriteGeo')
            wg['file'].setValue(tmpcam_filepath)
            wg['file_type'].setValue('abc')
            wg['writeGeometries'].setValue(0)
            wg['writePointClouds'].setValue(0)
            wg['writeCameras'].setValue(1)
            wg['writeAxes'].setValue(0)
            nuke.execute(wg)
    
            nuke.delete(camera)
            nuke.delete(scene)
            nuke.delete(wg)
          
         #### Import the Baked Camera exported (Creates a new Camera with the read from file option) ####   
            cleanCamera = nuke.createNode('Camera2', 'file {'+tmpcam_filepath+'} read_from_file True', inpanel = False)
            cleanCamera.knob('frame_rate').setValue(current_script_fps)
            cleanCamera.forceValidate()
            cleanCamera.knob('file').setValue('')
            cleanCamera.knob('read_from_file').setValue(0)
            
            
        else:
            nuke.message('Select a Camera')

#cameraBake()


			