import maya.cmds as cmds
import pymel.core as pm

# faces = list of pm.MeshFace
def __get_average_center(faces):
	average = pm.datatypes.Vector()
	for curr_face in faces:
		points = curr_face.getPoints(space='world')
		average += reduce(lambda x, y: x+y, points) / len(points)
	return average / len(faces)

# faces = list of pm.MeshFace
def __get_average_normal(faces):
	average = pm.datatypes.Vector()
	for curr_face in faces:
		average += curr_face.getNormal(space='world')
	return average.normal()

def look_at_selected_faces():
	# get the active camera
	active_panel = pm.getPanel(wf=True)
	if 'scriptEditorPanel1' == active_panel:
		cmds.error("Please don't call me from the script editor!")
	active_camera_xform = pm.modelEditor(active_panel, camera=True, q=True)
	if None == active_camera_xform:
		cmds.error("Failed to find active panel's camera.")
	active_camera = pm.listRelatives(active_camera_xform)[0]

	# get all selected faces
	selected_faces = filter(lambda x: isinstance(x, pm.MeshFace), pm.selected())
	selected_faces = [x for sublist in selected_faces for x in sublist]
	if not len(selected_faces):
		cmds.error("Please select at least one face.")

	# compute average normal
	average_normal = __get_average_normal(selected_faces)
	# compute average position
	average_position = __get_average_center(selected_faces)

	# distance from camera's current position to average position
	initial_distance = (average_position - active_camera_xform.getTranslation(space='world')).length()
	# new position from average along normal by the initial camera's distance
	new_position = (average_position + average_normal * initial_distance)
	# https://help.autodesk.com/cloudhelp/2016/ENU/Maya-Tech-Docs/CommandsPython/viewPlace.html
	cmds.viewPlace(str(active_camera), an=True, eye=new_position, la=average_position, up=[0.0, 1.0, 0.0])

look_at_selected_faces()
