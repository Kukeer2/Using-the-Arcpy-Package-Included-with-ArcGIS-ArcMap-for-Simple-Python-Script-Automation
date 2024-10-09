# coding=utf-8
import time

import arcpy
import numpy as np
import os



def process_raster_data(workspace, input_tiff, input_raster):
    # # 设置工作空间
    arcpy.env.workspace = workspace
    # 新建文件夹
    tiff_filename = os.path.basename(input_tiff)
    filename = os.path.basename(input_raster)
    new_folder = "process_" + tiff_filename + "_" + filename
    folder_path = os.path.join(workspace, new_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 输出重分类后的栅格路径
    output_reclass = os.path.join(workspace, new_folder, "reclass1.tif")
    # 输出栅格转换为多边形的路径
    output_polygon = os.path.join(workspace, new_folder, "polygon1.shp")
    # 输出monthly_temperature栅格转换为点的路径
    output_point_feature = os.path.join(workspace, new_folder, "monthly_temperature_point.shp")
    # 输出IDW进行插值的栅格路径
    output_raster_idw = os.path.join(workspace, new_folder, "Idw_shp1")
    # 输出out_idw栅格转换为点文件路径
    output_point_feature_idw = os.path.join(workspace, new_folder, "idw_point.shp")
    # 输出连接结果路径
    output_join_result = os.path.join(workspace, new_folder, "Join_Output.shp")

    # 重分类
    reclass_values = arcpy.sa.RemapValue([[0, "NODATA"], [1, 254, 1], [255, "NODATA"]])
    out_reclass = arcpy.sa.Reclassify(input_tiff, "Value", reclass_values)
    out_reclass.save(output_reclass)
    # print("重分类完成，输出路径为: " + output_reclass)

    # 栅格转换为多边形
    arcpy.RasterToPolygon_conversion(output_reclass, output_polygon, "NO_SIMPLIFY")
    # print("栅格转换为多边形完成，输出路径为: " + output_polygon)

    # monthly_temperature栅格转换为点
    arcpy.conversion.RasterToPoint(input_raster, output_point_feature)
    # print("monthly_temperature栅格转换为点，转换完成。")

    # 使用 IDW 工具进行插值
    cell_size = 100
    original_coord_system = arcpy.env.outputCoordinateSystem
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4548)
    out_idw = arcpy.sa.Idw(output_point_feature, "grid_code", cell_size)
    out_idw.save(output_raster_idw)
    # # print("IDW插值完成，输出路径为: " + output_raster_idw)

    # # out_idw栅格转换为点
    arcpy.conversion.RasterToPoint(output_raster_idw, output_point_feature_idw)
    # # print("栅格转换为点完成，输出路径为: " + output_point_feature_idw)

    field_mappings = arcpy.FieldMappings()
    grid_code_field = arcpy.FieldMap()
    grid_code_field.addInputField(output_point_feature_idw, "grid_code")
    output_field = grid_code_field.outputField
    output_field.name = "gridcode"
    grid_code_field.outputField = output_field
    field_mappings.addFieldMap(grid_code_field)

    arcpy.analysis.SpatialJoin(
        target_features=output_polygon,
        join_features=output_point_feature_idw,
        out_feature_class=output_join_result,
        join_type="KEEP_ALL",
        field_mapping=field_mappings
    )
    area_field = "gridcode"
    cursor = arcpy.SearchCursor(output_join_result, [area_field])
    area = []
    for row in cursor:
        area.append(row.getValue(area_field))
    del cursor
    area_array = np.array(area)
    arcpy.ClearWorkspaceCache_management()
    arcpy.env.outputCoordinateSystem = original_coord_system
    return area_array


def process_raster_data1(workspace, input_tiff, input_raster):
    # 设置工作空间
    arcpy.env.workspace = workspace
    # 新建文件夹
    tiff_filename = os.path.basename(input_tiff)
    new_folder = "process_" + tiff_filename
    folder_path = os.path.join(workspace, new_folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # 输出重分类后的栅格路径
    output_reclass = os.path.join(workspace, new_folder, "reclass1.tif")
    # 输出栅格转换为多边形的路径
    output_polygon = os.path.join(workspace, new_folder, "polygon1.shp")
    # 输出monthly_temperature栅格转换为点的路径
    output_point_feature = os.path.join(workspace, new_folder, "monthly_temperature_point.shp")
    # 输出IDW进行插值的栅格路径
    output_raster_idw = os.path.join(workspace, new_folder, "Idw_shp1")
    # 输出out_idw栅格转换为点文件路径
    output_point_feature_idw = os.path.join(workspace, new_folder, "idw_point.shp")
    # 输出连接结果路径
    output_join_result = os.path.join(workspace, new_folder, "Join_Output.shp")
    # 输出要素类路径（投影后）
    output_feature_class = os.path.join(workspace, new_folder, "Join_Output_Projected.shp")

    # 重分类
    reclass_values = arcpy.sa.RemapValue([[0, "NODATA"], [1, 254, 1], [255, "NODATA"]])
    out_reclass = arcpy.sa.Reclassify(input_tiff, "Value", reclass_values)
    out_reclass.save(output_reclass)
    # print("重分类完成，输出路径为: " + output_reclass)

    # 栅格转换为多边形
    arcpy.RasterToPolygon_conversion(output_reclass, output_polygon, "NO_SIMPLIFY")
    # print("栅格转换为多边形完成，输出路径为: " + output_polygon)

    # monthly_temperature栅格转换为点
    arcpy.conversion.RasterToPoint(input_raster, output_point_feature)
    # print("monthly_temperature栅格转换为点，转换完成。")

    # 使用 IDW 工具进行插值
    cell_size = 100
    original_coord_system = arcpy.env.outputCoordinateSystem
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(4548)
    out_idw = arcpy.sa.Idw(output_point_feature, "grid_code", cell_size)
    out_idw.save(output_raster_idw)
    # print("IDW插值完成，输出路径为: " + output_raster_idw)

    # out_idw栅格转换为点
    arcpy.conversion.RasterToPoint(output_raster_idw, output_point_feature_idw)
    # print("栅格转换为点完成，输出路径为: " + output_point_feature_idw)

    field_mappings = arcpy.FieldMappings()
    grid_code_field = arcpy.FieldMap()
    grid_code_field.addInputField(output_point_feature_idw, "grid_code")
    output_field = grid_code_field.outputField
    output_field.name = "gridcode"
    grid_code_field.outputField = output_field
    field_mappings.addFieldMap(grid_code_field)

    arcpy.analysis.SpatialJoin(
        target_features=output_polygon,
        join_features=output_point_feature_idw,
        out_feature_class=output_join_result,
        join_type="KEEP_ALL",
        field_mapping=field_mappings
    )

    target_coordinate_system = arcpy.SpatialReference(4549)
    arcpy.management.DefineProjection(output_join_result, target_coordinate_system)
    arcpy.management.Project(output_join_result, output_feature_class, target_coordinate_system)
    area_field = "add"
    arcpy.management.AddField(output_feature_class, area_field, "DOUBLE")
    arcpy.management.CalculateField(output_feature_class, area_field, "!shape.geodesicarea@squaremeters!", "PYTHON_9.3")
    area_field = "Add"
    cursor = arcpy.SearchCursor(output_feature_class, [area_field])
    area = []
    for row in cursor:
        area.append(row.getValue(area_field))
    del cursor
    area_array = np.array(area)
    arcpy.ClearWorkspaceCache_management()
    arcpy.env.outputCoordinateSystem = original_coord_system
    return area_array
