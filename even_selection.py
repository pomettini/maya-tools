import maya.cmds as cmds

# TEST Reset the scene to the original state
def ES_TestReset():
	cmds.select(all = True)
	cmds.delete()

# TEST Create a sphere and select an edge loop
def ES_TestCreate():
	cmds.polySphere(n = 'Object001')
	cmds.polySelect('Object001', toggle=True, edgeLoop=180)

def ES_FunctionalTest():
	ES_TestReset()
	ES_TestCreate()
	ES_SelectEven()

def ES_SelectEven():
	selection = cmds.ls(selection=True, flatten=True)
	# Deselect all the even items in the selection
	for i, item in enumerate(selection):
		if i % 2 == 0:
			cmds.select(item, deselect=True)

#ES_FunctionalTest()
ES_SelectEven()