import arcpy, os


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "GeodienstToolbox"
        self.alias = "GeodienstToolbox"

        # List of tool classes associated with this toolbox
        self.tools = [FieldOptimizer, FieldResetter,QuickAlias, QuickPopup]

class Helper(object):
    def __init__(self):
        pass
    
    def getFields(self,mapname, layername, onlyVisible=False):
        p = arcpy.mp.ArcGISProject('current')
        m = p.listMaps(mapname)[0]
        lyrs = m.listLayers(layername)
        layer  = lyrs[0]
        cim_lyr = layer.getDefinition('V2')
        fields = []
        if len(cim_lyr.featureTable.fieldDescriptions) >0:
        for fd in cim_lyr.featureTable.fieldDescriptions:
            if not onlyVisible:
                fields.append(fd.fieldName)
            elif fd.visible:
                fields.append(fd.fieldName)
        else:
            arcpy.AddError("Field descriptions in CIM are default")
        return fields
        
    def getFieldsAndAliases(self,mapname, layername, onlyVisible=False):
        p = arcpy.mp.ArcGISProject('current')
        m = p.listMaps(mapname)[0]
        lyrs = m.listLayers(layername)
        layer  = lyrs[0]
        cim_lyr = layer.getDefinition('V2')
        fields = []
        for fd in cim_lyr.featureTable.fieldDescriptions:
            if not onlyVisible:
                fields.append([fd.fieldName, fd.alias])
            elif fd.visible:
                fields.append([fd.fieldName, fd.alias])
        return fields

class FieldOptimizer(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FieldOptimizer"
        self.description = "Turns off all fields which are not used in the online map to improve performance"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        inmap = arcpy.Parameter(
            displayName="Input Map",
            name="in_map",
            datatype="Map",
            parameterType="Required",
            direction="Input")
        layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="Layer",
            parameterType="Required",
            direction="Input")
        fields = arcpy.Parameter(
            displayName="Fields",
            name="fields",
            datatype="String",
            parameterType="Required",
            direction="Input")
        fields.filter.type = "ValueList"
        fields.filter.list = []
        fields.multiValue = True

        params = [inmap,layer,fields]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].valueAsText:
            if parameters[1].valueAsText:
                helper = Helper()
                fields = helper.getFields(parameters[0].valueAsText, parameters[1].valueAsText)
                parameters[2].filter.list = fields
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        p = arcpy.mp.ArcGISProject('current')
        m = p.listMaps(parameters[0].valueAsText)[0]
        lyrs = m.listLayers(parameters[1].valueAsText)
        layer  = lyrs[0]
        cim_lyr = layer.getDefinition('V2')
        fields = []
        if len(cim_lyr.featureTable.fieldDescriptions) == 0:
            arcpy.AddError("Field descriptions in CIM are default")
        for fd in cim_lyr.featureTable.fieldDescriptions:
            if fd.fieldName == cim_lyr.renderer.field:
                arcpy.AddMessage("{0} is visible".format(fd.fieldName))
                fd.visible = True
            elif fd.fieldName.upper() == "SHAPE":
                arcpy.AddMessage("{0} is visible".format(fd.fieldName))
                fd.visible = True
            elif fd.fieldName in parameters[2].values:
                arcpy.AddMessage("{0} is visible".format(fd.fieldName))
                fd.visible = True
            else:
                arcpy.AddMessage("{0} is invisible".format(fd.fieldName))
                fd.visible = False
        layer.setDefinition(cim_lyr)
        return

class FieldResetter(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "FieldResetter"
        self.description = "Turns on all fields in a layer"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""

        inmap = arcpy.Parameter(
            displayName="Input Map",
            name="in_map",
            datatype="Map",
            parameterType="Required",
            direction="Input")
        layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="Layer",
            parameterType="Required",
            direction="Input")

        params = [inmap,layer]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        p = arcpy.mp.ArcGISProject('current')
        m = p.listMaps(parameters[0].valueAsText)[0]
        lyrs = m.listLayers(parameters[1].valueAsText)
        layer  = lyrs[0]
        cim_lyr = layer.getDefinition('V2')
        fields = []
        for fd in cim_lyr.featureTable.fieldDescriptions:
            fd.visible = True
        layer.setDefinition(cim_lyr)
        return
        

class QuickAlias(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "1 QuickAlias"
        self.description = "Create Field aliases on the visible fields"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        inmap = arcpy.Parameter(
            displayName="Input Map",
            name="in_map",
            datatype="Map",
            parameterType="Required",
            direction="Input")
        layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="Layer",
            parameterType="Required",
            direction="Input")
        fields = arcpy.Parameter(
            displayName="Fields (Empty Alias input will be ignored",
            name="fields",
            datatype="GPValueTable",
            parameterType="Required",
            direction="Input")
        fields.columns = [['GPString', 'Field'], ['GPString', 'Alias']]
        fields.enabled = False
        params = [inmap,layer,fields]
        
        
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        if parameters[0].valueAsText:
            if parameters[1].valueAsText:
                parameters[2].enabled = True
                helper = Helper()
                fields = helper.getFieldsAndAliases(parameters[0].valueAsText, parameters[1].valueAsText, onlyVisible=True)
                #values = []
                #for field in fields:
                #    values.append([field,''])
                if parameters[2].values is None:
                    parameters[2].values = fields
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        p = arcpy.mp.ArcGISProject('current')
        m = p.listMaps(parameters[0].valueAsText)[0]
        lyrs = m.listLayers(parameters[1].valueAsText)
        layer  = lyrs[0]
        cim_lyr = layer.getDefinition('V2')
        fields = []
        for fd in cim_lyr.featureTable.fieldDescriptions:
            for value in parameters[2].values:
                if value[0] == fd.fieldName and value[1] != "":
                    fd.alias = value[1]
                    arcpy.AddMessage("{0} alias: {1}".format(fd.fieldName, fd.alias))
        layer.setDefinition(cim_lyr)
        return
        
class QuickPopup(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "QuickPopup"
        self.description = "Creates a popup for all fields with Alias and formats the renderfield to Dutch number formatting"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        
        inmap = arcpy.Parameter(
            displayName="Input Map",
            name="in_map",
            datatype="Map",
            parameterType="Required",
            direction="Input")
        layer = arcpy.Parameter(
            displayName="Input Layer",
            name="in_layer",
            datatype="Layer",
            parameterType="Required",
            direction="Input")
        decimals = arcpy.Parameter(
            displayName="Number of decimals",
            name="decimals",
            datatype="GPLong",
            parameterType="Required",
            direction="Input")
        decimals.value = 0
        nodata = arcpy.Parameter(
            displayName="No data value",
            name="nodata",
            datatype="GPString",
            parameterType="Required",
            direction="Input")
        nodata.value= "Data nog niet bekend"
        params = [ inmap, layer, decimals, nodata]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        p = arcpy.mp.ArcGISProject('current')
        m = p.listMaps(parameters[0].valueAsText)[0]
        lyrs = m.listLayers(parameters[1].valueAsText)
        layer  = lyrs[0]
        cim_lyr = layer.getDefinition('V2')
        fields = []
        nodata = parameters[3].value
        decimals = "0"* parameters[2].value
        hasdecimals = "." if parameters[2].value >0 else ""
        pi = cim_lyr.popupInfo
        fields = [] 
        for fd in cim_lyr.featureTable.fieldDescriptions:
            if fd.fieldName == cim_lyr.renderer.field:
                exinfo = arcpy.cim.CIMSymbolizers.CIMExpressionInfo()
                exinfo.name =  'FormattedNumber'
                exinfo.title = fd.alias if fd.alias is not None and fd.alias !="" else fd.fieldName
                exinfo.returnType = 'String'
                expression = 'if ($feature.' + fd.fieldName + ' == 999999999){\nreturn "'+ nodata +'"}\nelse{\nreturn  Replace(Replace(Replace(Text($feature.' + fd.fieldName + ', "###,###,###'+ hasdecimals + decimals +'"),".","*"),",","."),"*",",")\n}'
                arcpy.AddMessage("field expression = " + expression)
                exinfo.expression = expression
                pi.expressionInfos.clear()
                pi.expressionInfos.append(exinfo)
                fields.append(r'expression/' + exinfo.name )
                layer.setDefinition(cim_lyr)
            else:
                if fd.visible:
                    fields.append(fd.fieldName)
                    arcpy.AddMessage("field visible in popup = " + fd.fieldName)
            
        tablemediainfo = pi.mediaInfos[0]
        tablemediainfo.fields = fields
        layer.setDefinition(cim_lyr)
        return