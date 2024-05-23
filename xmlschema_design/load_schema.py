import xmlschema
import os






def Load():
    path= os.path.join("/Users/darshankumar/Documents/Python AI/simulation_preparation","xmlschema_design")
    os.chdir(path)
    my_schmea= xmlschema.XMLSchema('substation_template.scd')
    network_schema=my_schmea.to_dict('substation_template.xml')
    return network_schema