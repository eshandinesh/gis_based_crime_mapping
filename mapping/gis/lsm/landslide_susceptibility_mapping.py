from basic_function import *

import Landslide_Susceptibility as ls

def factor_maps():
    #Path_of_joined_dataset=mosiac()
    reply = str(input("Do You already have Dataset yes/no"))
    if reply=="yes":
        target_rasterPath=str(input("Enter Path of the Dataset for Reclassify slope"))
    else:
        target_rasterPath=None
        Path_of_joined_dataset = str(input("Enter Path of the Dataset"))
    Path_of_Reclassified_Elevation_dataset = reclassify_raster(Path_of_joined_dataset, target_rasterPath)
    Path_of_slope_dataset=slope(Path_of_joined_dataset)
    reply=str(input("Do You already have Dataset yes/no"))
    if reply=="yes":
        target_rasterPath=str(input("Enter Path of the Dataset for Reclassify slope"))
    else:
        target_rasterPath=None
    Path_of_Reclassified_slope_dataset=reclassify_raster(Path_of_slope_dataset, target_rasterPath)
    Path_of_Aspect_dataset=aspect(Path_of_joined_dataset)
    if reply=="yes":
        target_rasterPath=str(input("Enter Path of the Dataset for Reclassify Aspect"))
    else:
        target_rasterPath=None
    Path_of_Reclassified_Aspect_dataset=reclassify_raster(Path_of_Aspect_dataset, target_rasterPath)
    
    #iterblocks_raster_claculator(Path_of_joined_dataset, raster_index_list=None, band_index_list=None, largest_block=2 ** 20, astype=np.float32, offset_only=False)






def open_File(path):
    if path is None:
        path = str(input("file path"))
    #print "Entered File Path is %s" % path
    datasource = gdal.Open(path,gdal.GA_Update)
    return datasource,path

def tuple_generator(band_index_list,raster_index_list,path):
    reply = str(input("DO YOU HAVE RASTER DATASET YES/NO"))
    if reply=="NO":
        print"for creating target raster provide base raster path"
        datasource, path = open_File(path)
        dstPath, dataset, filepath = create_raster_dataset_as_per_other_dataset(path, datasource)
    else:
        dstPath=str(input("enter path of raster dataset"))
    print"opening target raster"
    target_raster = gdal.Open(dstPath, gdal.GA_Update)
    target_band = target_raster.GetRasterBand(1)
    textfile = open("C:\Users\Hp\Desktop\Textfile\Tuplelist\Text2.txt", 'w')
    q=0
    astype = np.float32
    largest_block = 2 ** 20
    raster_list = []
    if raster_index_list is None:
        number_of_raster = int(input("raster number"))
        for i in range(number_of_raster):
            dataset, filepath = open_File(path=None)
            raster_list.append(dataset)
        raster_index_list=raster_list
    else:
        for m in range(len(raster_index_list)):
            dataset, filepath = open_File(raster_index_list[m])
            raster_list.append(dataset)
        raster_index_list = raster_list
        number_of_raster = len(raster_index_list)
    if band_index_list is None:
        band_index_list = [raster.RasterCount for raster in raster_index_list]
    band_list = [
        raster.GetRasterBand(index) for index,raster in zip(band_index_list, raster_index_list)]
    block = band_list[0].GetBlockSize()
    cols_per_block = block[0]
    rows_per_block = block[1]
    print cols_per_block,rows_per_block
    n_cols = raster_index_list[0].RasterXSize
    n_rows = raster_index_list[0].RasterYSize
    block_area = cols_per_block * rows_per_block
    if largest_block / block_area > 0:
        width_factor = largest_block / block_area
        cols_per_block *= width_factor
        if cols_per_block > n_cols:
            cols_per_block = n_cols
        block_area = cols_per_block * rows_per_block
    # try to make block taller
    if largest_block / block_area > 0:
        height_factor = largest_block / block_area
        rows_per_block *= height_factor
        if rows_per_block > n_rows:
            rows_per_block = n_rows

    n_col_blocks = int(math.ceil(n_cols / float(cols_per_block)))
    n_row_blocks = int(math.ceil(n_rows / float(rows_per_block)))
    last_row_block_width = None
    last_col_block_width = None
    if astype is not None:
        block_type_list = [astype] * len(band_list)
    for row_block_index in range(n_row_blocks):
        row_offset = row_block_index * rows_per_block
        row_block_width = n_rows - row_offset
        if row_block_width > rows_per_block:
            row_block_width = rows_per_block

        for col_block_index in range(n_col_blocks):
            col_offset = col_block_index * cols_per_block
            col_block_width = n_cols - col_offset
            if col_block_width > cols_per_block:
                col_block_width = cols_per_block

            # resize the raster block cache if necessary
            if (last_row_block_width != row_block_width or
                    last_col_block_width != col_block_width):
                raster_blocks = [
                    np.zeros(
                        (row_block_width, col_block_width),
                        dtype=block_type) for block_type in
                    block_type_list]
                output_raster_blocks = np.zeros((row_block_width, col_block_width), dtype=astype)

            offset_dict = {
                'xoff': col_offset,
                'yoff': row_offset,
                'win_xsize': col_block_width,
                'win_ysize': row_block_width,
            }
            result = offset_dict
            dic = {}
            for i in range(number_of_raster):
                band_list[i].ReadAsArray(buf_obj=raster_blocks[i], **offset_dict)
                dic[i] = np.array(raster_blocks[i])
            for s,a,e,u in zip(dic[0].flatten(),dic[1].flatten(),dic[2].flatten(),range(len(dic[0].flatten()))):
                k=(s,a,e)
                print k
                if s<0 or a<0:
                    o=-1
                else:
                    fc = ls.FuzzyController()
                    o=fc.controller(s,a,e)
                    oarray=output_raster_blocks.flatten()
                    result=np.put(oarray,[u],o)
            target_band.WriteArray(result.reshape(row_block_width, col_block_width), xoff=offset_dict['xoff'],yoff=offset_dict['yoff'])
            print "over"
    target_band.FlushCache()






tuple_generator(band_index_list=None,raster_index_list=["I:\Data\data\LSMDATASET\RECLASSSLOPE\RECLASSSLOPE.tif","I:\Data\data\LSMDATASET\RECLASSASPECT\RECLASSASPECT.tif","I:\Data\data\LSMDATASET\MOSIAC\ELEVATIONRECLASS\ELEVATIONRECLASS.tif"],path="I:\Data\data\LSMDATASET\MOSIAC\MOSIAC.tif")