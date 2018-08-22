import maya.cmds as mc

class SceneVrayObjID():
	sceneAssets = []
	sceneMatteNodes = {}
	sceneObjNumbers = []
	sceneGeos = {}
	
	def __init__(self):
		self.mattes = {}
		self.objIDs = {}
		self.geos = {}

	def sceneRefAssets():
		# list all reference nodes in scene
		ref = mc.ls(references=True)
		# list comprehension to get the namespaces from ref nodes
		namespaces = [mc.referenceQuery(r, namespace=True) for r in ref]
		# return only namespaces that are assets
		return [ns for ns in namespaces if mc.objExists('{0}:ASSET'.format(ns))]

	# get rgb ID's and channel name from VRayRenderElement Node
	def getMatteID(self,matte):
		if mc.attributeQuery('vray_redid_multimatte', node=matte, exists=True):
			r = mc.getAttr('{0}.vray_redid_multimatte'format(matte))
			g = mc.getAttr('{0}.vray_greenid_multimatte'format(matte))
			b = mc.getAttr('{0}.vray_blueid_multimatte'format(matte))
			chan = mc.getAttr('{0}.vray_name_multimatte'format(matte))
			return [r, g, b, chan]
	
	# get vrayObjectID from geo node
	def getGeoID(self,geo):
		if mc.attributeQuery('vrayObjectID', node=geo, exists=True):
			return mc.getAttr('{0}.vrayObjectID'format(geo))
		else:
			return 'Not Assigned'	 


class Asset(SceneVrayObjID):
	
	def __init__(self, asset):
		self.asset = asset

	def getMattes():
	    # find VRayRenderElement nodes with Asset namespace
	    res = mc.ls('{0}:*'.format(asset),exactType='VRayRenderElement')
	    
	    # find multiMatteEements - has to have vray_redid_multimatte attribute
	    mme = [re for re in res if mc.attributeQuery('vray_redid_multimatte', node=r, exists=True)]
	    
	    for each in mme:
	    	# get id numbers and channel name
	    	r = mc.getAttr('{0}.vray_redid_multimatte'format(each))
	    	g = mc.getAttr('{0}.vray_greenid_multimatte'format(each))
	    	b = mc.getAttr('{0}.vray_blueid_multimatte'format(each))
	    	chan = mc.getAttr('{0}.vray_name_multimatte'format(each))
	    	# add to dict mattes
	    	self.mattes[each] = [r, g, b, chan]

	def getIDnumbers(self):
		pass
	
	def getGeos(self):
		geos = mc.ls('{0}:*_geoShape'.format(asset),)
