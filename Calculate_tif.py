# coding=utf-8
import os
from tqdm import tqdm
import raster_processing
import pandas as pd
import numpy as np



def calculate(y, workspace_path, tif_file, temperaturetif, raintif, NPPtif):
    if y == 'river.tif':
        total_area_result = raster_processing.process_raster_data1(workspace_path, tif_file, "monthly_temperature.tif")
        Carbon_sink = total_area_result * ((0.6 + 0 + 3.8) * 3.6666 + 0.9 * 3.6666 * 0.1)
        serial_numbers = list(range(1, len(total_area_result) + 1))
        df = pd.DataFrame({
            '序号': serial_numbers,
            '面积': total_area_result,
            '碳汇量': Carbon_sink
        })
        df = df[['序号', '面积', '碳汇量']]
        excel_filename = "river.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Data saved to {}".format(excel_filename))

    elif y == 'lake.tif':
        total_area_result = raster_processing.process_raster_data1(workspace_path, tif_file, "monthly_temperature.tif")
        Carbon_sink = total_area_result * ((0.6 + 0 + 3.8) * 3.6666 + 0.9 * 3.6666 * 0.1)
        serial_numbers = list(range(1, len(total_area_result) + 1))
        df = pd.DataFrame({
            '序号': serial_numbers,
            '面积': total_area_result,
            '碳汇量': Carbon_sink
        })
        df = df[['序号', '面积', '碳汇量']]
        excel_filename = "lake.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Data saved to {}".format(excel_filename))

    elif y == 'canal.tif':
        total_area_result = raster_processing.process_raster_data1(workspace_path, tif_file, "monthly_temperature.tif")
        Carbon_sink = total_area_result * (0.6 + 0 + 0) * 3.6666
        serial_numbers = list(range(1, len(total_area_result) + 1))
        df = pd.DataFrame({
            '序号': serial_numbers,
            '面积': total_area_result,
            '碳汇量': Carbon_sink
        })
        df = df[['序号', '面积', '碳汇量']]
        excel_filename = "canal.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Data saved to {}".format(excel_filename))
    elif y == 'marsh.tif':
        total_area_result = raster_processing.process_raster_data1(workspace_path, tif_file, temperaturetif)
        temperature = modification(
            (raster_processing.process_raster_data(workspace_path, tif_file, temperaturetif))) - 273.1
        rain = modification(raster_processing.process_raster_data(workspace_path, tif_file, raintif)) * 100
        NPP = modification(raster_processing.process_raster_data(workspace_path, tif_file, NPPtif)) * 1000 * 0.08333
        Carbon_sink = calculation(total_area_result, temperature, rain, NPP)
        serial_numbers = list(range(1, len(total_area_result) + 1))
        df = pd.DataFrame({
            '序号': serial_numbers,
            '面积': total_area_result,
            '气温': temperature,
            '降水量': rain,
            'NPP': NPP,
            '碳汇量': Carbon_sink
        })
        df = df[['序号', '面积', '气温', '降水量', 'NPP', '碳汇量']]
        excel_filename = "marsh.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Data saved to {}".format(excel_filename))
    elif y == 'swamp.tif':
        total_area_result = raster_processing.process_raster_data1(workspace_path, tif_file, temperaturetif)
        temperature = modification(
            (raster_processing.process_raster_data(workspace_path, tif_file, temperaturetif))) - 273.1
        rain = modification(raster_processing.process_raster_data(workspace_path, tif_file, raintif)) * 100
        NPP = modification(raster_processing.process_raster_data(workspace_path, tif_file, NPPtif)) * 1000 * 0.08333
        Carbon_sink = calculation(total_area_result, temperature, rain, NPP)
        serial_numbers = list(range(1, len(total_area_result) + 1))
        df = pd.DataFrame({
            '序号': serial_numbers,
            '面积': total_area_result,
            '气温': temperature,
            '降水量': rain,
            'NPP': NPP,
            '碳汇量': Carbon_sink
        })
        df = df[['序号', '面积', '气温', '降水量', 'NPP', '碳汇量']]
        excel_filename = "swamp.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Data saved to {}".format(excel_filename))
    elif y == 'field.tif':
        total_area_result = raster_processing.process_raster_data1(workspace_path, tif_file, temperaturetif)
        temperature = modification(
            (raster_processing.process_raster_data(workspace_path, tif_file, temperaturetif))) - 273.1
        rain = modification(raster_processing.process_raster_data(workspace_path, tif_file, raintif)) * 100
        NPP = modification(raster_processing.process_raster_data(workspace_path, tif_file, NPPtif)) * 1000 * 0.08333
        Carbon_sink = calculation(total_area_result, temperature, rain, NPP)
        serial_numbers = list(range(1, len(total_area_result) + 1))
        df = pd.DataFrame({
            '序号': serial_numbers,
            '面积': total_area_result,
            '气温': temperature,
            '降水量': rain,
            'NPP': NPP,
            '碳汇量': Carbon_sink
        })
        df = df[['序号', '面积', '气温', '降水量', 'NPP', '碳汇量']]
        excel_filename = "field.xlsx"
        df.to_excel(excel_filename, index=False)
        print("Data saved to {}".format(excel_filename))

    else:
        return 0


def modification(num):
    average_num = np.mean(num[num != 0])
    zero_indices = np.where(num == 0)
    num[zero_indices] = average_num
    return num


def calculation(num, temperature, rain, NPP):
    formula_A = NPP - (np.exp(0.22) * (1.25 * np.exp(0.05452 * temperature) * rain / (4.259 + temperature)) ** 0.87)
    result = num * (0.6 + (formula_A * 0.01) + 3.8) * 3.6666
    return result


def process_and_calculate(workspace_path, path, temperaturetif, raintif, NPPtif):
    tif_files = [os.path.join(path, file) for file in os.listdir(path) if file.endswith(".tif")]
    for tif_file in tqdm(tif_files, desc="Processing"):
        y = os.path.basename(tif_file)
        calculate(y, workspace_path, tif_file, temperaturetif, raintif, NPPtif)


workspace_path = "E:/pythonProject2/WUHAN"
path = "E:/pythonProject2/WUHAN/tif"
temperaturetif = "temperature.tif"
raintif = "rain.tif"
NPPtif = "NPP.tif"

process_and_calculate(workspace_path, path, temperaturetif, raintif, NPPtif)
