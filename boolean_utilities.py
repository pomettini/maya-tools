import maya.cmds as cmds
from pymel.all import Callback

# TEST Reset the scene to the original state
def BU_TestReset():
	cmds.select(all = True)
	cmds.delete()

# TEST Create two objects that will work with booleans
def BU_TestCreate():
	cmds.polyCube(n = 'Object001')
	cmds.polyCube(n = 'Object002')
	cmds.move(0, 0, 0, 'Object001')
	cmds.move(0.5, 0.5, 0.5, 'Object002')

def BU_DiffIntersection():
	selection = cmds.ls(sl=True)

	# If you don't have exactly two meshes selected it ends the function
	if len(selection) > 2 or len(selection) < 2:
		print "You have to select two elements"
		return

	firstObj = selection[0]
	secondObj = selection[1]

	# I duplicate the objects to use it again
	firstObjCopy = cmds.duplicate(firstObj)
	secondObjCopy = cmds.duplicate(secondObj)

	# First I do the difference between the first and the second object
	cmds.polyCBoolOp(firstObj, secondObj, op=2)
	# Then I do the intersection
	cmds.polyCBoolOp(firstObjCopy, secondObjCopy, op=3)

def BU_IntersectionPreserveMeshes():
	selection = cmds.ls(sl=True)

	# If you don't have exactly two meshes selected it ends the function
	if len(selection) > 2 or len(selection) < 2:
		print "You have to select two elements"
		return

	firstObj = selection[0]
	secondObj = selection[1]

	# I duplicate the objects to use it again
	firstObjCopy = cmds.duplicate(firstObj)
	secondObjCopy = cmds.duplicate(secondObj)

	# This will be used later as well
	secondObjCopy2 = cmds.duplicate(secondObj)

	# First I do the difference between the first and the second object
	cmds.polyCBoolOp(firstObj, secondObj, op=2)
	# Then I do the intersection
	intersObj = cmds.polyCBoolOp(firstObjCopy, secondObjCopy, op=3)

	# This will get preserve all the meshes used for the intersection
	intersObjCopy = cmds.duplicate(intersObj)
	cmds.polyCBoolOp(secondObjCopy2, intersObjCopy, op=2)

def BU_FunctionalTest1():
	BU_TestReset()
	BU_TestCreate()
	cmds.select('Object001')
	cmds.select('Object002', add=True)
	BU_DiffIntersection()

def BU_FunctionalTest2():
	BU_TestReset()
	BU_TestCreate()
	cmds.select('Object002')
	cmds.select('Object001', add=True)
	BU_DiffIntersection()

def BU_FunctionalTest3():
	BU_TestReset()
	BU_TestCreate()
	cmds.select('Object001')
	cmds.select('Object002', add=True)
	BU_IntersectionPreserveMeshes()

def BU_FunctionalTest4():
	BU_TestReset()
	BU_TestCreate()
	cmds.select('Object002')
	cmds.select('Object001', add=True)
	BU_IntersectionPreserveMeshes()

def BU_InitUI():
	win_name = 'diff_intersection'

	if cmds.window(win_name, q=True, ex=True):
		cmds.deleteUI(win_name)

	cmds.window(win_name, t='Boolean Utilities')
	cmds.window(win_name, e=True, height=100, width=300, sizeable=False)
	cmds.columnLayout(adj=True)
	cmds.button(l='Difference + Intersection', height=50, c=Callback(BU_DiffIntersection))
	cmds.button(l='Intersection (Preserve Meshes)', height=50, c=Callback(BU_IntersectionPreserveMeshes))
	cmds.setParent('..')
	cmds.showWindow(win_name)

BU_InitUI()