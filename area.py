import os
import datetime
import Calculate_tif

workspace = "Run_time_folder"
current_time = datetime.datetime.now()
folder_name = current_time.strftime("%Y%m%d_%H%M%S")
folder_path = os.path.join(workspace, folder_name)
if not os.path.exists(folder_path):
    os.makedirs(folder_path)
workspace_path = folder_path
path = "Run_time_folder/tif"

temperature_tif = None
for filename in os.listdir("temperature_tif"):
    if filename.endswith(".tif"):
        temperaturetif = os.path.join(folder_path, filename)
        break
rain_tif = None
for filename in os.listdir("rain_tif"):
    if filename.endswith(".tif"):
        temperaturetif = os.path.join(folder_path, filename)
        break
NPP_tif = None
for filename in os.listdir("NPP_tif"):
    if filename.endswith(".tif"):
        temperaturetif = os.path.join(folder_path, filename)
        break

Calculate_tif.process_and_calculate(workspace_path, path, temperature_tif, rain_tif, NPP_tif)