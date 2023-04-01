import openstudio as os
# import openstudio.model as model
# import openstudio.runmanager as runmanager
# import openstudio.simulation as simulation

# Create an OpenStudio model
m = os.model.Model()

# Add a building story to the model
s = os.model.BuildingStory(m)

# Add a thermal zone to the building story
z = os.model.ThermalZone(m)
z.setVolume(1000)
s.addThermalZone(z)

# Set up the simulation parameters
params = os.simulation.SimulationParameters()
params.setRunSimulationforSizingPeriods(False)
params.setUseIdealAirLoads(True)

# Run the simulation
result = os.runmanager.runModel(m, params)

# Print the simulation results
print("Simulation completed successfully!")
print("Total electric energy used (J):", result.totalSiteEnergy())
