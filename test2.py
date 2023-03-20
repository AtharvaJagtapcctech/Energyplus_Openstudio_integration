import openstudio as os
#import os.path

# Load the gbXML file
temp = os.gbxml.GbXMLReverseTranslator()
temp1 = temp.loadModel(path = "D:\\Gbxml\\ConferenceRoomStudy.xml")
if temp1.is_initialized():
    model = temp1.get()

# Convert it to osm hello
#model.save("D:\\Code_output\\Gbxml_to_osmoutput.osm", True)
#model1 = os.model.Model.load("D:\\Code_output\\Gbxml_to_osmoutput.osm").get()
#print(type(model1))


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

#Assign design day
designDay = os.model.DesignDay(model)
designDay.setName("My Design Day")
designDay.setMonth(7)
designDay.setDayOfMonth(21)
#designDay.setDaylightSavingTimeIndicator("Yes")
designDay.setMaximumDryBulbTemperature(30)
designDay.setDailyDryBulbTemperatureRange(10)
designDay.setHumidityIndicatingType("Wetbulb")
designDay.setBarometricPressure(101325)
#designDay.addToWorkspace()
print(designDay)

#add schedule set
default_schedule_set = os.model.DefaultScheduleSet(model)

#add schedule limits
schedule_limits = os.model.ScheduleTypeLimits(model)
schedule_limits.setName("Fractional")
#schedule_limits.setUnitType("Dimensionless")
schedule_limits.setLowerLimitValue(0.0)
schedule_limits.setUpperLimitValue(1.0)

#add schedule to ruleset
schedule = os.model.ScheduleRuleset(model)
schedule.setName("New Schedule")
schedule.setScheduleTypeLimits(schedule_limits)
 
schedule1 = os.model.ScheduleRuleset(model)
schedule1.setName("New Schedule 2")
schedule1.setScheduleTypeLimits(schedule_limits)

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

model.save("D:\\Code_output\\Final_output.osm", True)
# translator = os.energyplus.ForwardTranslator()
# idf = translator.translateModel(model)
# idf.save("/mnt/d/Code_output/IDFoutput.idf", True)