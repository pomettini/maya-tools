import maya.cmds as cmds

# TEST Reset the scene to the original state
def TestResetScene():
	cmds.select(all=True)
	cmds.delete()

# TEST Reset hypeshade to the original state
def TestResetHypershade():
	materials = cmds.ls(type='shadingDependNode')
	cmds.delete(materials)

def LoadFilePrompt():
	# Opens a prompt that ask user to select only images
	imgFilter = 'All Image files (*.jpg *.gif *.png);;'
	imgPath = cmds.fileDialog2(fileFilter=imgFilter, dialogStyle=1, fileMode=1)
	# If the Texture exists it returns it
	if imgPath is not None:
		return imgPath

def NewTextureMaterial():
	imgPath = LoadFilePrompt()
	# Creates a new lambert
	myMaterial = cmds.shadingNode('lambert', asShader=True)
	# Creates a shading node for the file
	myFile = cmds.shadingNode('file', asTexture=True)
	# Creates a shading group
	myShadingGroup = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
	# Sets the texture path
	cmds.setAttr(myFile+'.fileTextureName', imgPath[0], type='string')
	# Assigns the Texture File Name to the Shading Group Shader
	cmds.connectAttr(myMaterial+'.outColor', myShadingGroup+'.surfaceShader')
	# Assigns the Texture Color to the Material Color
	cmds.connectAttr(myFile+'.outColor', myMaterial+'.color')
	# Returns the material
	return myMaterial

def FunctionalTest1():
	# Resets everything
	TestResetScene()
	TestResetHypershade()
	# Creates a plane
	cmds.polyPlane(name='Object001', w=5, h=5, sx=True, sy=True)
	myMaterial = NewTextureMaterial()
	# Selects the object and applies the new material
	cmds.select('Object001')
	cmds.hyperShade(assign=myMaterial)

#FunctionalTest1()
NewTextureMaterial()