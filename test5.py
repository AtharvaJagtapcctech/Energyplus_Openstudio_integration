import openstudio as os

#import os.path

# Load the gbXML file
temp = os.gbxml.GbXMLReverseTranslator()
temp1 = temp.loadModel(path = "/mnt/d/Gbxml/ConferenceRoomStudy.xml")
if temp1.is_initialized():
    model = temp1.get()

# Convert it to osm
model.save("/mnt/d/Gbxml/output.osm", True)
model1 = os.model.Model.load("/mnt/d/Gbxml/output.osm").get()

#Load EPW file
epw_path = os.path("/mnt/d/Gbxml/IND_Pune.430630_ISHRAE.epw")
epw = os.openstudioutilities.openstudioutilitiesfiletypes.EpwFile(epw_path)
weather = os.model.WeatherFile.setWeatherFile(model, epw)

#print(type(weather))
city = weather.get().city()

#Assign design day
designDay = os.model.DesignDay(model1)
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

default_schedule_set = os.model.DefaultScheduleSet(model1)
hours_of_operation_schedule = default_schedule_set.hoursofOperationSchedule()

#add schedule limits
schedule_limits = os.model.ScheduleTypeLimits(model1)
schedule_limits.setName("Fractional")
#schedule_limits.setUnitType("Dimensionless")
schedule_limits.setLowerLimitValue(0.0)
schedule_limits.setUpperLimitValue(10.0)

schedule = os.model.ScheduleRuleset(model1)
schedule.setName("Summer")
schedule.setScheduleTypeLimits(schedule_limits)

# Add ScheduleDay to ScheduleRuleset
schedule_day = os.model.ScheduleDay(model1)
schedule_day.setName("Schedule Day")
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
#schedule.setScheduleTypeLimits(os.model.ScheduleTypeLimits(model1))
schedule.setWinterDesignDaySchedule(schedule_day)
schedule.setSummerDesignDaySchedule(schedule_day)
#schedule.defaultDaySchedule(schedule_day)

default_schedule_set.setNumberofPeopleSchedule(schedule)

model1.save("/mnt/d/Gbxml/output4.osm", True)