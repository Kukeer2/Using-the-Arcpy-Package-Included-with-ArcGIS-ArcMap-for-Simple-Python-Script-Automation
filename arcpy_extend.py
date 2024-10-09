import os
import arcpy
from arcpy import conversion
import raster_processing


def RasterToPoint(workspace, input_raster, output_point_feature):
    arcpy.env.workspace = workspace
    arcpy.conversion.RasterToPoint(input_raster, output_point_feature)
    arcpy.ClearWorkspaceCache_management()


workspace = "E:/pythonProject2/Run_time_folder"
temperaturetif = "temperature.tif"
raintif = "rain.tif"
NPPtif = "NPP.tif"
tif_file = "WUHAN/tif/marsh.tif"
# tiff_filename = os.path.basename(temperaturetif)
# new_folder = "process_" + tiff_filename
# folder_path = os.path.join(workspace, new_folder)
# if not os.path.exists(folder_path):
#     os.makedirs(folder_path)
# output_point_feature = os.path.join(workspace, new_folder, "monthly_temperature_point.shp")
# RasterToPoint(workspace, temperaturetif, output_point_feature)
#
#
# tiff_filename = os.path.basename(raintif)
# new_folder = "process_" + tiff_filename
# folder_path = os.path.join(workspace, new_folder)
# if not os.path.exists(folder_path):
#     os.makedirs(folder_path)
# output_point_feature = os.path.join(workspace, new_folder, "monthly_temperature_point.shp")
# RasterToPoint(workspace, temperaturetif, output_point_feature)
raster_processing.process_raster_data(workspace, tif_file, temperaturetif)
# raster_processing.process_raster_data(workspace, tif_file, raintif)
