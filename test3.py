import openstudio as os
#import os.path

# Load the gbXML file
temp = os.gbxml.GbXMLReverseTranslator()
temp1 = temp.loadModel(path = "D:\\Gbxml\\ConferenceRoomStudy.xml")
if temp1.is_initialized():
    model = temp1.get()
# translator = os.energyplus.ForwardTranslator()
# idf = translator.translateModel(model)
# idf.save("D:\\Code_output\\IDF_output.idf", True)
#Convert it to osm
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

ddy_path ='D:\\Gbxml\\IND_Pune.430630_ISHRAE1M.ddy'
ddy_idf = os.IdfFile.load(os.toPath(str(ddy_path)), os.IddFileType('EnergyPlus')).get()
ddy_workspace = os.Workspace(ddy_idf)
rt = os.energyplus.ReverseTranslator()
ddy_model = rt.translateWorkspace(ddy_workspace)
desginDays = ddy_model.getDesignDays()
for desginDay in desginDays:
    model.addObject(desginDay.clone())

# #Assign design day
# designDay = os.model.DesignDay(model)
# designDay.setName("My Design Day")
# designDay.setMonth(7)
# designDay.setDayOfMonth(21)
# #designDay.setDaylightSavingTimeIndicator("Yes")
# designDay.setMaximumDryBulbTemperature(30)
# designDay.setDailyDryBulbTemperatureRange(10)
# designDay.setHumidityIndicatingType("Wetbulb")
# designDay.setBarometricPressure(101325)
# #designDay.addToWorkspace()
# print(designDay)

#get thermal zones
thermal_zones = model.getThermalZones()
print("Thermal Zones are: ")
for thermal_zone in thermal_zones:
    zone_name = thermal_zone.name().get()
    print(zone_name)

#get all surface details
surfaces = model.getSurfaces()
print("Surfaces are ")
for surface in surfaces:
    surface_name = surface.name().get()
    print("Surface name:",surface_name)

    surface_type = surface.surfaceType()
    print("Surface type:", surface_type)
       
    construction_1 = surface.construction().get()
    new = surface_type
    construction_1.setName(new)
    construction_name = construction_1.name().get()
    print("Construction Name:",construction_name)
   
    subsurfaces = surface.subSurfaces()
    for subsurface in subsurfaces:
        subsurface_name = subsurface.name().get()
        surface_type_2 = subsurface.subSurfaceType()
        construction_2 = subsurface.construction().get()
        new2= surface_type_2
        construction_2.setName(new2)
        construction_2_name = subsurface.construction().get().name().get()
        print( construction_2_name,"\n")

    newname = f"{surface_name} - {surface_type}"
    surface.setName(newname)
print("New Surfaces are ")
for surface in surfaces:
    surface_name = surface.name().get()
    print("Surface name:",surface_name)

#add schedule set
default_schedule_set = os.model.DefaultScheduleSet(model)

#add schedule limits
schedule_limits = os.model.ScheduleTypeLimits(model)
schedule_limits.setName("Fractional")
#schedule_limits.setUnitType("Dimensionless")
schedule_limits.setLowerLimitValue(0.0)
schedule_limits.setUpperLimitValue(1.0)
schedule_limits2 = os.model.ScheduleTypeLimits(model)
schedule_limits2.setName("Temperature")
schedule_limits2.setUnitType("Temperature")
schedule_limits2.setLowerLimitValue(0.00)
schedule_limits2.setUpperLimitValue(23.50)

#add schedule to ruleset
schedule = os.model.ScheduleRuleset(model)
schedule.setName("New Schedule")
schedule.setScheduleTypeLimits(schedule_limits)
 
schedule1 = os.model.ScheduleRuleset(model)
schedule1.setName("New Schedule 2")
schedule1.setScheduleTypeLimits(schedule_limits2)

# Add ScheduleDay to ScheduleRuleset
schedule_day = os.model.ScheduleDay(model)
#schedule_day.setName("Schedule Day")
schedule_day.addValue(os.Time(0,8,0,0), 0.5)
schedule_day.addValue(os.Time(0,9,0,0), 1)
schedule_day.addValue(os.Time(0,10,0,0), 1)
schedule_day.addValue(os.Time(0,11,0,0), 1)
schedule_day.addValue(os.Time(0,12,0,0), 1)
schedule_day.addValue(os.Time(0,13,0,0), 1)
schedule_day.addValue(os.Time(0,14,0,0), 1)
schedule_day.addValue(os.Time(0,15,0,0), 1)
schedule_day.addValue(os.Time(0,16,0,0), 1)
schedule_day.setInterpolatetoTimestep(True)
#schedule_day.setScheduleTypeLimits(schedule_limits)
#schedule.setScheduleTypeLimits(os.model.ScheduleTypeLimits(model1))
schedule.setWinterDesignDaySchedule(schedule_day)
schedule.setSummerDesignDaySchedule(schedule_day)
schedule1.setWinterDesignDaySchedule(schedule_day)
schedule1.setSummerDesignDaySchedule(schedule_day)

#addschedule to scheduleset
default_schedule_set.setNumberofPeopleSchedule(schedule)

#add load 
peopleDefinition = os.model.PeopleDefinition(model)
peopleDefinition.setNumberofPeople(12)
peopleDefinition.setFractionRadiant(0.3)
peopleDefinition.setName("CCTech Conference Room People Load")
# peopleDefinition.disableASHRAE55ComfortWarnings()lightsDefinition = openstudio.model.LightsDefinition(model)
lightsDefinition = os.model.LightsDefinition(model)
lightsDefinition.setName("CCTech Conference Room Light Load")
lightsDefinition.setLightingLevel(210)

#add default Constructionset
construction_set = os.model.DefaultConstructionSet(model)
construction_set.setName('My Construction Set')
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


#new_wall_construction = model.getConstructionByName("Wall")
# surface_constructions = model.getDefaultSurfaceConstructions("Wall")
#construction_set.setDefaultExteriorSurfaceConstructions(surface_constructions)
#add space type
space_type = os.model.SpaceType(model)
space_type.setName("Conference_space")
space_type.setStandardsBuildingType("Office")
space_type.setDefaultConstructionSet(construction_set)
space_type.setDefaultScheduleSet(default_schedule_set)
dsoa = os.model.DesignSpecificationOutdoorAir(model)
dsoa.setName("MyDesignSpecificationOutdoorAir")
ventilation_rate = 0.2 # m^3/s per m^2
dsoa.setOutdoorAirFlowperFloorArea(ventilation_rate)
space_type.setDesignSpecificationOutdoorAir(dsoa)
spa=os.model.SpaceInfiltrationDesignFlowRate(model)
spa.setName("newairflowrate")
flow_rate=spa.airChangesperHour()
#print(type(flow_rate))
#spa.setAirChangesperHour(flow_rate)
#space_type.setSpaceInfiltrationDesignFlowRate(spa)

#add building settings
building = model.getBuilding()
building.setName("MyBuilding")
floor_to_floor_height = 3.0 # meters
building.setNominalFloortoFloorHeight(floor_to_floor_height)
north_axis=20.0
building.setNorthAxis(north_axis)
#story_name=model.getBuildingStoryByName("aim0015")
#story_name.setnominalZCoordinate(22)
story = model.getBuildingStoryByName("aim0015").get()
#story.setName("MyStory")
story.setNominalZCoordinate(22)
story.setNominalFloortoCeilingHeight(3)
story.setNominalFloortoFloorHeight(3)


# Set the SpaceType for the Space
space_name=model.getSpaceByName("aim0030").get()
space_name.setSpaceType(space_type)
space_name.setBuildingStory(story)
space_name.setDefaultConstructionSet(construction_set)
space_name.setDefaultScheduleSet(default_schedule_set)
#space.setThermalZone("aim0024")
thermal_zoned = model.getThermalZoneByName("aim0024")
if thermal_zoned.is_initialized():
    thermal_zoness = thermal_zoned.get()
    #thermal_zoness.setCoolingSetpointTemperatureSchedule(schedule1) 
    space_name.setThermalZone(thermal_zoness)
else:
    print("Thermal zone not found.")

# dual_setpoint_thermostat = os.model.ThermostatSetpointDualSetpoint(model)
# dual_setpoint_thermostat.setCoolingSchedule(schedule1)
thermal_zone = model.getThermalZoneByName("aim0024").get()
#thermal_zone.setName("aim0024")

thermostat = os.model.ThermostatSetpointDualSetpoint(model)
thermostat.setName("My Thermostat")
thermostat.setCoolingSetpointTemperatureSchedule(schedule1)
thermostat.setHeatingSetpointTemperatureSchedule(schedule1)
thermal_zone.setThermostatSetpointDualSetpoint(thermostat)
#thermal_zone.setCoolingThermostatSetpointTemperatureSchedule(schedule1)

#run_period = os.model.Timestep(model)

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

#model.runSimulationforSizingPeriods()
#workflow=os.
model.save("D:\\Code_output\\Final_output.osm", True)
translator = os.energyplus.ForwardTranslator()
idf = translator.translateModel(model)
idf.save("D:\\Code_output\\IDF_output.idf", True)


