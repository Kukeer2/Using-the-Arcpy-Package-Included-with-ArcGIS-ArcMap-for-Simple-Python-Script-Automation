# coding=utf-8
import os

import numpy as np
from osgeo import gdal

def read_image(path):
    """读取影像"""

    dataset = gdal.Open(path)
    # 栅格矩阵的列数
    im_width = dataset.RasterXSize
    # 栅格矩阵的行数
    im_height = dataset.RasterYSize
    # 波段数
    im_bands = dataset.RasterCount
    im_geotrans = dataset.GetGeoTransform()  # 获取仿射矩阵信息
    im_proj = dataset.GetProjection()  # 获取投影信息
    arr = dataset.ReadAsArray()
    del dataset

    return im_width, im_height, im_geotrans, im_proj, arr

def writeTiff(im_data, im_width, im_height, im_bands, im_geotrans, im_proj, path):
    """将数组写成图像"""

    if len(im_data.shape) == 3:
        im_bands, im_height, im_width = im_data.shape
    elif len(im_data.shape) == 2:
        im_data = np.array([im_data])
    else:
        im_bands, (im_height, im_width) = 1, im_data.shape
        # 创建文件
    driver = gdal.GetDriverByName("GTiff")
    dataset = driver.Create(path, im_width, im_height, im_bands, gdal.GDT_Byte)
    if (dataset != None):
        dataset.SetGeoTransform(im_geotrans)  # 写入仿射变换参数
        dataset.SetProjection(im_proj)  # 写入投影
    for i in range(im_bands):
        dataset.GetRasterBand(i + 1).WriteArray(im_data[i])
    del dataset


if __name__ == '__main__':
    print('正在进行影像读取...')
    tif_path = 'Registration/Manual_registration/png.tif' #参考图像
    pngs_path = 'Registration/PNG'
    out_path = 'Run_time_folder/tif'

    dir = os.path.exists(out_path)
    if dir != True:
        os.makedirs(out_path)

    pngs = [i for i in os.listdir(pngs_path) if i.split('.')[-1] == 'png']
    for i in pngs:
        print(i)
        im_width, im_height, im_geotrans, im_proj, arr = read_image(tif_path)
        png_path = pngs_path + '\\' + i  # 配准图像
        input_dataset = gdal.Open(png_path)
        if input_dataset is not None:
            # 获取输入数据集的驱动程序
            input_driver = input_dataset.GetDriver()
            # 指定新文件名
            output_file = out_path + '\\' + i
            # 使用 CreateCopy 方法创建新的数据集副本
            output_dataset = input_driver.CreateCopy(output_file, input_dataset)
            if output_dataset is not None:
                output_dataset.SetGeoTransform(im_geotrans)
                output_dataset.SetProjection(im_proj)
                # 关闭数据集
                input_dataset = None
                output_dataset = None
                print("created successfully as {}.".format(output_file))
            else:
                print("Error: Unable to create copy.")
        else:
            print("Error: Unable to open {}.".format(png_path))
