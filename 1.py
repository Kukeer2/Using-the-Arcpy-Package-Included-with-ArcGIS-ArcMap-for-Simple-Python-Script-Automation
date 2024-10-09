# coding=utf-8
import arcpy
from arcpy import management

# 指定输入和输出路径
input_png = 'Registration/PNG/all.png'  # PNG 文件路径
output_tif = 'Registration/PNG/all.tif'  # TIFF 文件路径

# 转换 PNG 到 TIFF
arcpy.management.CopyRaster(input_png, output_tif)

# 为输出的 TIFF 文件创建金字塔层级
arcpy.management.BuildPyramids(output_tif)
