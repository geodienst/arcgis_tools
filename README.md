# arcgis_tools
This repository contains handy arcgis toolboxes
The tools are developed to publish a large dataset with many attribute columns optimized for ArcGIS Online. 

# FieldOptimizer
This tool disables all fields except the shape field, the field used for symbology and selected fields. The layer should use data from a FileGeodatabase.


# FieldResetter
This tool enables all fields in the selected layer

# QuickAlias
This tool has a simplified UI to set field Aliases for the Visible fields.

# QuickPopup
This tool creates a simple tabular popup for the visible fields. The field used for symbology gets an Arcade expression to force numeric values into Dutch number formatting and a no data value will be converted to a text message

# Remarks
* The Fields and popup info in the CIM are seem to be only accessible when they are not default. Modify the popup and fields one time manually in the ArcGIS Pro Project to force them to custom properties and then run the Tools


