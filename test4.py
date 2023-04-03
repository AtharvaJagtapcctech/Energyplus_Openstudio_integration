import openstudio as os
#import os.path

# Load the gbXML file
temp = os.gbxml.GbXMLReverseTranslator()
temp1 = temp.loadModel(path = "D:\\Gbxml\\ConferenceRoomStudy.xml")
if temp1.is_initialized():
    model = temp1.get()
model.save("D:\\Code_output\\Gbxml_to_osmoutput.osm", True)
model1 = os.model.Model.load("D:\\Code_output\\Gbxml_to_osmoutput.osm").get()
print(type(model1))

#Load EPW file
epw_path = os.path("D:\\Gbxml\\IND_Pune.430630_ISHRAE.epw")
epw = os.openstudioutilities.openstudioutilitiesfiletypes.EpwFile(epw_path)
weather = os.model.WeatherFile.setWeatherFile(model, epw)

city = weather.get().city()
dataSource = weather.get().dataSource()
stateProvinceRegion = weather.get().stateProvinceRegion()
country = weather.get().country()
wMONumber = weather.get().wMONumber()
latitude = weather.get().latitude()
longitude = weather.get().longitude()
timeZone = weather.get().timeZone()
elevation = weather.get().elevation()
url = weather.get().url()
path = weather.get().path()
isElevationDefaulted = weather.get().isElevationDefaulted()
startDateActualYear = weather.get().startDateActualYear()
startDayOfWeek = weather.get().startDayOfWeek()

site = model.getSite()
site.setElevation(elevation)
site.setLatitude(latitude)
site.setLongitude(longitude)
site.setTimeZone(timeZone)

#load ddy file
ddy_path ='D:\\Gbxml\\IND_Pune.430630_ISHRAE1M.ddy'
ddy_idf = os.IdfFile.load(os.toPath(str(ddy_path)), os.IddFileType('EnergyPlus')).get()
ddy_workspace = os.Workspace(ddy_idf)
rt = os.energyplus.ReverseTranslator()
ddy_model = rt.translateWorkspace(ddy_workspace)
desginDays = ddy_model.getDesignDays()
for desginDay in desginDays:
    model.addObject(desginDay.clone())



thermal_zones = model.getThermalZones()
#print("Thermal Zones are: ")
for thermal_zone in thermal_zones:
    zone_name = thermal_zone.name().get()
    #print(zone_name)

#get all surface details
surfaces = model.getSurfaces()
#print("Surfaces are ")
for surface in surfaces:
    surface_name = surface.name().get()
    #print("Surface name:",surface_name)

    surface_type = surface.surfaceType()
    #print("Surface type:", surface_type)
       
    construction_1 = surface.construction().get()
    new = surface_type
    construction_1.setName(new)
    construction_name = construction_1.name().get()
    #print("Construction Name:",construction_name)
   
    subsurfaces = surface.subSurfaces()
    for subsurface in subsurfaces:
        subsurface_name = subsurface.name().get()
        surface_type_2 = subsurface.subSurfaceType()
        construction_2 = subsurface.construction().get()
        new2= surface_type_2
        construction_2.setName(new2)
        construction_2_name = subsurface.construction().get().name().get()
        #print( construction_2_name,"\n")

    newname = f"{surface_name} - {surface_type}"
    surface.setName(newname)
#print("New Surfaces are ")
for surface in surfaces:
    surface_name = surface.name().get()
    #print("Surface name:",surface_name)

#add schedule set
default_schedule_set = os.model.DefaultScheduleSet(model)
default_schedule_set.setName('CCTech Conference Room Schedule')

#add schedule limits
schedule_limits_temperature_37 = os.model.ScheduleTypeLimits(model)
schedule_limits_temperature_37.setName("Temperature 37")   #error in this function it accesses unit type instead of name
schedule_limits_temperature_37.setUnitType("Temperature")
schedule_limits_temperature_37.setNumericType("Continuous")
schedule_limits_temperature_37.setLowerLimitValue(0.0)
schedule_limits_temperature_37.setUpperLimitValue(24.0)

schedule_limits_temperature_36 = os.model.ScheduleTypeLimits(model)
schedule_limits_temperature_36.setName("Temperature 36") #error in this function it accesses unit type instead of name
schedule_limits_temperature_36.setUnitType("Temperature")
schedule_limits_temperature_36.setNumericType("Continuous")
schedule_limits_temperature_36.setLowerLimitValue(0.0)
schedule_limits_temperature_36.setUpperLimitValue(20.0)

schedule_limits_Activity = os.model.ScheduleTypeLimits(model)
schedule_limits_Activity.setName("ActivityLevel") #error in this function it accesses unit type instead of name
schedule_limits_Activity.setUnitType("ActivityLevel")
schedule_limits_Activity.setNumericType("Continuous")
schedule_limits_Activity.setLowerLimitValue(0.0)
schedule_limits_Activity.setUpperLimitValue(132.0)

schedule_limits_fraction = os.model.ScheduleTypeLimits(model)
schedule_limits_fraction.setName("Fraction") #error in this function it accesses unit type instead of name
schedule_limits_fraction.setUnitType("Fraction")
schedule_limits_fraction.setNumericType("Continuous")
schedule_limits_fraction.setLowerLimitValue(0.0)
schedule_limits_fraction.setUpperLimitValue(1.0)

#add schedule to ruleset
schedule = os.model.ScheduleRuleset(model)
schedule.defaultDaySchedule()
schedule.setName("Clg Thermostat Schedule")
schedule.setScheduleTypeLimits(schedule_limits_temperature_37)

schedule1 = os.model.ScheduleRuleset(model)
schedule1.setName("Htg Thermostat Schedule")
schedule1.setScheduleTypeLimits(schedule_limits_temperature_36)
 
schedule2 = os.model.ScheduleRuleset(model)
schedule2.setName("Office Activity")
schedule2.setScheduleTypeLimits(schedule_limits_Activity)

schedule3 = os.model.ScheduleRuleset(model)
schedule3.setName("Office Bldg Equip")
schedule3.setScheduleTypeLimits(schedule_limits_fraction)

schedule4 = os.model.ScheduleRuleset(model)
schedule4.setName("Office Bldg Light")
schedule4.setScheduleTypeLimits(schedule_limits_fraction)

schedule5 = os.model.ScheduleRuleset(model)
schedule5.setName("Office Infil Quarter On")
schedule5.setScheduleTypeLimits(schedule_limits_fraction)

schedule6 = os.model.ScheduleRuleset(model)
schedule6.setName("Office Work Occ")
schedule6.setScheduleTypeLimits(schedule_limits_fraction)

#add dayschedule
schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Medium Office ClgSetp Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 24)
schedule_day.addValue(os.Time(0,24,0,0),24)
schedule_day.setInterpolatetoTimestep(True)
schedule.setWinterDesignDaySchedule(schedule_day)
schedule.setSummerDesignDaySchedule(schedule_day)

schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Medium Office HtgSetp Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 20)
schedule_day.addValue(os.Time(0,24,0,0),20)
schedule_day.setInterpolatetoTimestep(True)
schedule1.setWinterDesignDaySchedule(schedule_day)
schedule1.setSummerDesignDaySchedule(schedule_day)

schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Office Activity Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 99)
schedule_day.addValue(os.Time(0,24,0,0),99)
schedule_day.setInterpolatetoTimestep(True)
schedule2.setWinterDesignDaySchedule(schedule_day)
schedule2.setSummerDesignDaySchedule(schedule_day)

schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Office Bldg Equip Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 1)
schedule_day.addValue(os.Time(0,24,0,0),1)
schedule_day.setInterpolatetoTimestep(True)
schedule3.setWinterDesignDaySchedule(schedule_day)
schedule3.setSummerDesignDaySchedule(schedule_day)

schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Office Bldg Light Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 1)
schedule_day.addValue(os.Time(0,24,0,0),1)
schedule_day.setInterpolatetoTimestep(True)
schedule4.setWinterDesignDaySchedule(schedule_day)
schedule4.setSummerDesignDaySchedule(schedule_day)

schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Office Infil Quarter On Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 1)
schedule_day.addValue(os.Time(0,24,0,0),1)
schedule_day.setInterpolatetoTimestep(True)
schedule5.setWinterDesignDaySchedule(schedule_day)
schedule5.setSummerDesignDaySchedule(schedule_day)

schedule_day = os.model.ScheduleDay(model)
schedule_day.setName("Office Bldg Occ Default Schedule")
schedule_day.addValue(os.Time(0,0,0,0), 1)
schedule_day.addValue(os.Time(0,24,0,0),1)
schedule_day.setInterpolatetoTimestep(True)
schedule6.setWinterDesignDaySchedule(schedule_day)
schedule6.setSummerDesignDaySchedule(schedule_day)

#addschedule to scheduleset
default_schedule_set.setNumberofPeopleSchedule(schedule6)
default_schedule_set.setPeopleActivityLevelSchedule(schedule2)
default_schedule_set. setLightingSchedule(schedule4)
default_schedule_set.setElectricEquipmentSchedule(schedule3)
default_schedule_set. setInfiltrationSchedule(schedule5)

construction_set = os.model.DefaultConstructionSet(model)
construction_set.setName('CCTech Conference Room')
construction23 = model.getConstructionByName("Wall")
construction24 = model.getConstructionByName("Floor")
construction25 = model.getConstructionByName("RoofCeiling")
construction26 = model.getConstructionByName("OperableWindow")
construction27 = model.getConstructionByName("Door")
temp1 = os.model.DefaultSurfaceConstructions(model)
temp1.setWallConstruction(construction23.get())
temp1.setFloorConstruction(construction24.get())
temp1.setRoofCeilingConstruction(construction25.get())
construction_set.setDefaultExteriorSurfaceConstructions(temp1)
construction_set.setDefaultInteriorSurfaceConstructions(temp1)
construction_set.setDefaultGroundContactSurfaceConstructions(temp1)
temp2 = os.model.DefaultSubSurfaceConstructions(model)
temp2.setFixedWindowConstruction(construction26.get())
temp2.setOperableWindowConstruction(construction26.get())
temp2.setDoorConstruction(construction27.get())
construction_set.setDefaultExteriorSubSurfaceConstructions(temp2)
construction_set.setDefaultInteriorSubSurfaceConstructions(temp2)

#add load 
peopleDefinition = os.model.PeopleDefinition(model)
peopleDefinition.setNumberofPeople(12)
peopleDefinition.setFractionRadiant(0.3)
peopleDefinition.setName("CCTech Conference Room People Load")
lightsDefinition = os.model.LightsDefinition(model)
lightsDefinition.setName("CCTech Conference Room Light Load")
lightsDefinition.setLightingLevel(210)

#add space type
space_type = os.model.SpaceType(model)
space_type.setName("Conference Room 1")
space_type.setDefaultConstructionSet(construction_set)
space_type.setDefaultScheduleSet(default_schedule_set)
DesignSpecificationOutdoorAir = os.model.DesignSpecificationOutdoorAir(model)
DesignSpecificationOutdoorAir.setName("189.1-2009 - Office - Conference - CZ1-3 Ventilation")
DesignSpecificationOutdoorAir.setOutdoorAirMethod('Sum')
ventilation_rate = 0.002359737216
DesignSpecificationOutdoorAir.setOutdoorAirFlowperPerson(ventilation_rate)
ventilation_rate = 0.0003048 
DesignSpecificationOutdoorAir.setOutdoorAirFlowperFloorArea(ventilation_rate)
DesignSpecificationOutdoorAir.setOutdoorAirFlowRateFractionSchedule(schedule6)
space_type.setDesignSpecificationOutdoorAir(DesignSpecificationOutdoorAir)
spa=os.model.SpaceInfiltrationDesignFlowRate(model)
spa.setName("189.1-2009 - Office - Conference - CZ1-3 Infiltration")
## No object present in space type class for assign space infiltration design flow rate

#add building settings
building = model.getBuilding()
building.setName("CCTech Building") 
floor_to_Ceiling_height =3 # meters
building.setNominalFloortoCeilingHeight(floor_to_Ceiling_height)
floor_to_floor_height =2.499360 # meters
building.setNominalFloortoFloorHeight(floor_to_floor_height)
north_axis=270.0
building.setNorthAxis(north_axis)
stories=4
building.setStandardsNumberOfStories(stories)
building.setSpaceType(space_type)
building.setDefaultConstructionSet(construction_set)
building.setDefaultScheduleSet(default_schedule_set)

#add story
story = model.getBuildingStoryByName("aim0015").get() #Not able to get it dynamically or reset
story.setName("Conference Room 4th Level")
story.setNominalZCoordinate(22)
story.setNominalFloortoCeilingHeight(2.499360)
story.setNominalFloortoFloorHeight(3)
story.setDefaultConstructionSet(construction_set)
story.setDefaultScheduleSet(default_schedule_set)

# Set the SpaceType for the Space
space_name=model.getSpaceByName("aim0030").get()
space_name.setName("Conference Room")
space_name.setDefaultConstructionSet(construction_set)
space_name.setDefaultScheduleSet(default_schedule_set)

#add thermal zones
thermal_zone = model.getThermalZoneByName("aim0024").get()
thermostat = os.model.ThermostatSetpointDualSetpoint(model)
thermostat.setName("My Thermostat")
thermostat.setCoolingSetpointTemperatureSchedule(schedule)
thermostat.setHeatingSetpointTemperatureSchedule(schedule1)
thermal_zone.setThermostatSetpointDualSetpoint(thermostat)

#add imulation settings
runPeriod = os.model.getRunPeriod(model)
runPeriod.setBeginMonth(1)
runPeriod.setBeginDayOfMonth(1)
runPeriod.setEndMonth(12)
runPeriod.setEndDayOfMonth(31)
sizingParameters = os.model.getSizingParameters(model)
sizingParameters.setHeatingSizingFactor(1.25)
sizingParameters.setCoolingSizingFactor(1.15)
timestep = os.model.getTimestep(model)
timestep.setNumberOfTimestepsPerHour(60)
simulationControl = os.model.getSimulationControl(model)
simulationControl.setRunSimulationforSizingPeriods(True)
simulationControl.setRunSimulationforWeatherFileRunPeriods(True)
simulationControl.setMaximumNumberofWarmupDays(25)
simulationControl.setMinimumNumberofWarmupDays(1)
simulationControl.setTemperatureConvergenceToleranceValue(0.4)
simulationControl.setLoadsConvergenceToleranceValue(0.04)
simulationControl.setSolarDistribution("MinimalShadowing")
simulationControl.setMaximumNumberofHVACSizingSimulationPasses(1)
shadowCalculation = os.model.getShadowCalculation(model)
shadowCalculation.setShadingCalculationUpdateFrequency(20)
shadowCalculation.setMaximumFiguresInShadowOverlapCalculations(1500)
shadowCalculation.setPolygonClippingAlgorithm("SutherlandHodgman")
shadowCalculation.setSkyDiffuseModelingAlgorithm("SimpleSkyDiffuseModeling")
insideSurfaceConvectionAlgorithm = os.model.getInsideSurfaceConvectionAlgorithm(model)
insideSurfaceConvectionAlgorithm.setAlgorithm("AdaptiveConvectionAlgorithm")
outsideSurfaceConvectionAlgorithm = os.model.getOutsideSurfaceConvectionAlgorithm(model)
outsideSurfaceConvectionAlgorithm.setAlgorithm("AdaptiveConvectionAlgorithm")
heatBalanceAlgorithm = os.model.getHeatBalanceAlgorithm(model)
heatBalanceAlgorithm.setAlgorithm("ConductionTransferFunction")
heatBalanceAlgorithm.setSurfaceTemperatureUpperLimit(200)
heatBalanceAlgorithm.setMinimumSurfaceConvectionHeatTransferCoefficientValue(0.1)
heatBalanceAlgorithm.setMaximumSurfaceConvectionHeatTransferCoefficientValue(1000)
zoneAirHeatBalanceAlgorithm = os.model.getZoneAirHeatBalanceAlgorithm(model)
zoneAirHeatBalanceAlgorithm.setAlgorithm("ThirdOrderBackwardDifference")

model.save("D:\\Code_output\\Conference_room_copy.osm", True)
translator = os.energyplus.ForwardTranslator()
idf = translator.translateModel(model)
idf.save("D:\\Code_output\\Conference_room_copy.idf", True)