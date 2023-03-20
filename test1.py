import openstudio as os
# Load the gbXML file
temp = os.gbxml.GbXMLReverseTranslator()
temp1 = temp.loadModel(path = "/mnt/d/Gbxml/ConferenceRoomStudy.xml")
if temp1.is_initialized():
   
    model = temp1.get()
    surfaces = model.getSurfaces()
    thermal_zones = model.getThermalZones()
    print("Thermal Zones are ")

    for thermal_zone in thermal_zones:
        zone_name = thermal_zone.name().get()
        print(zone_name)

    print("Surfaces are ")
    for surface in surfaces:
        surface_name = surface.name().get()
        print("Surface name:",surface_name)
       
        construction = surface.construction().get()
        construction_name = construction.name().get()
        print("Construction Name:",construction_name)
       
        surface_type = surface.surfaceType()
        print("Surface type:", surface_type,"\n")

        newname = f"{surface_name} - {surface_type}"
        surface.setName(newname)

    print("New Surfaces are ")
    for surface in surfaces:
        surface_name = surface.name().get()
        print("Surface name:",surface_name)
        

    