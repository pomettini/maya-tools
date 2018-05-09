import maya.cmds as cmds

# TEST Reset the scene to the original state
def TestReset():
	cmds.select(all = True)
	cmds.delete()

# TEST Create a sphere and select an edge loop
def TestCreate():
	cmds.polySphere(n = 'Object001')
	cmds.polySelect('Object001', toggle=True, edgeLoop=180)

def FunctionalTest():
	TestReset()
	TestCreate()
	SelectEven()

def SelectEven():
	selection = cmds.ls(selection=True, flatten=True)
	# Deselect all the even items in the selection
	for i, item in enumerate(selection):
		if i % 2 == 0:
			cmds.select(item, deselect=True)

#FunctionalTest()
SelectEven()