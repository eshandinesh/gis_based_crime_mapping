import math
import glob
import math
import os
import os.path
import shutil
from osgeo import ogr
import gdal
import numpy as np
from gdalconst import *
from osgeo import gdal
# import mapnik
import pygeoprocessing as pg
from lsm import Landslide_Susceptibility as ls
import gc

_DEFAULT_GTIFF_CREATION_OPTIONS = ('TILED=YES', 'BIGTIFF=IF_SAFER')


def frange(start, stop, step):
    i = 0
    while (start + (i * step)) < stop:
        yield start + i * step
        i += 1

def open_File(path):
    if path is None:
        path = str(input("file path"))
    #print "Entered File Path is %s" % path
    datasource = gdal.Open(path,gdal.GA_Update)
    return datasource,path


def metadata(path):
    datasource,filepath = open_File(path)
    print (datasource.GetMetadata())

def creating_directory():
    print ("Please provide detail for developing new Directory")
    folderName = input("Enter Folder Name")
    folderPath = input("Where you want to save folder ")
    path = folderPath + '\\' + folderName
    #print path
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)



def raster_size(path):
    dataset,filePath = open_File(path)
    print("Size is {} x {} x {}".format(dataset.RasterXSize,
                                        dataset.RasterYSize,
                                        dataset.RasterCount))




def rater_band_count(path):
    datasource,filePath = open_File(path)
    print ("[ RASTER BAND COUNT ]: ", datasource.RasterCount)

def reading_raster(path):
    dataset,filepath=open_File(path)
    #print("Driver: {}/{}".format(dataset.GetDriver().ShortName,dataset.GetDriver().LongName))
    #print("Size is {} x {} x {}".format(dataset.RasterXSize,dataset.RasterYSize,dataset.RasterCount))
    #print("Projection is {}".format(dataset.GetProjection()))
    geotransform = dataset.GetGeoTransform()
    #if geotransform:
       #print("Origin = ({}, {})".format(geotransform[0], geotransform[3]))
        #print("Pixel Size = ({}, {})".format(geotransform[1], geotransform[5]))
    return [geotransform[1], geotransform[5]]

def reading_raster_band(raster_path):
    min, max = pg.geoprocessing.calculate_raster_stats(raster_path)
    print (min,max)
    a=((max-min)/(5))
    d = {}
    for i in range(min,int(min+(0.5)*a),1):
        d[i] = 1
    for i in range(int(min+(0.5)*a),int(min+(1.5*a)),1):
        d[i]=2
    for i in range(int(min+(1.5*a)), int(min+(3*a)), 1):
        d[i] = 3
    for i in range(int(min+(3*a)), max+1, 1):
        d[i] = 4
    print (d)
    return min,max,d


def rater_stats(path):
    raster_path=path
    min,max=pg.geoprocessing.calculate_raster_stats(raster_path)
    print min,max

def create_raster_dataset_as_per_other_dataset (path,datasource):
    gdal.AllRegister()
    if path is None and datasource is None:
        dataset,filepath = open_File(path)
    else:
        dataset=datasource
        filepath=path
    fileformat = dataset.GetDriver().ShortName
    #print fileformat
    folderLocation, folderName = creating_directory()
    print "Please Enter detail regarding new raster dataset"
    name = input("Enter Dataset Name")
    dstPath = os.path.join(folderLocation, "%s.tif" % name)
    driver=gdal.GetDriverByName(str(fileformat))
    #print driver
    dst_ds = driver.Create(dstPath , dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount, GDT_Float32)
    dst_ds.SetProjection(dataset.GetProjection())
    dst_ds.SetGeoTransform(dataset.GetGeoTransform())
    dst_ds=None
    return dstPath,dataset,filepath


def iterblocks_raster_claculator (path,raster_index_list=None, band_index_list=None, largest_block=2 ** 20, astype=np.float32, offset_only=False):

    print"creating target raster"
    datasource,path=open_File(path)
    dstPath, dataset, filepath=create_raster_dataset_as_per_other_dataset(path, datasource)
    print"opening target raster"
    target_raster = gdal.Open(dstPath, gdal.GA_Update)
    target_band = target_raster.GetRasterBand(1)
    print"opening source raster"
    if raster_index_list is None:
        raster_list = []
        number_of_raster = int(input("raster number"))
        for i in range(number_of_raster):
            dataset, filepath = open_File(path=None)
            raster_list.append(dataset)
        raster_index_list=raster_list

    if band_index_list is None:
        band_index_list = [raster.RasterCount for raster in raster_index_list]

    band_list = [
        raster.GetRasterBand(index) for index,raster in zip(band_index_list,raster_index_list)]

    block = band_list[0].GetBlockSize()
    cols_per_block = block[0]
    rows_per_block = block[1]

    n_cols = raster_index_list[0].RasterXSize
    n_rows = raster_index_list[0].RasterYSize

    block_area = cols_per_block * rows_per_block
    # try to make block wider
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

    # Initialize to None so a block array is created on the first iteration
    last_row_block_width = None
    last_col_block_width = None

    if astype is not None:
        block_type_list = [astype] * len(band_list)
    #else:
        #block_type_list = [_gdal_to_numpy_type(ds_band) for ds_band in band_index_list]

    for row_block_index in xrange(n_row_blocks):
        row_offset = row_block_index * rows_per_block
        row_block_width = n_rows - row_offset
        if row_block_width > rows_per_block:
            row_block_width = rows_per_block

        for col_block_index in xrange(n_col_blocks):
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

            offset_dict = {
                'xoff': col_offset,
                'yoff': row_offset,
                'win_xsize': col_block_width,
                'win_ysize': row_block_width,
            }
            result = offset_dict
            if not offset_only:
                dic={}
                i=0
                for i in range (number_of_raster):
                    band_list[i].ReadAsArray(buf_obj=raster_blocks[i], **offset_dict)
                    dic[i]=np.array(raster_blocks[i])
                result = (result,) + tuple(raster_blocks)
                target_block=np.add(dic[0].flatten(),dic[1].flatten())
                dic=None
                target_band.WriteArray(target_block.reshape(row_block_width, col_block_width), xoff=offset_dict['xoff'],yoff=offset_dict['yoff'])
    target_band.FlushCache()
    target_band = None
    target_raster = None


def slope(path):
    datasource, path = open_File(path)
    print "Creating New Dataset for Slope"
    dstPath,dataset,filepath=create_raster_dataset_as_per_other_dataset(path,datasource)
    dst_ds=gdal.DEMProcessing(dstPath,dataset,'slope',format = 'GTiff', alg='ZevenbergenThorne', scale=111120, zFactor=30)
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i=i+1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    min,max,d=reading_raster_band(dstPath)
    histogram(min, max, dst_ds)
    #zonal_statistics(dstPath, dst_ds)
    dst_ds.BuildOverviews('average',[2,4,8,16,32,64,128,256,512,1024,2048])
    dst_ds=None
    return dstPath

def aspect(path):
    datasource, path = open_File(path)
    print "Creating New Dataset for Aspect"
    dstPath, dataset, filepath = create_raster_dataset_as_per_other_dataset(path,datasource)
    dst_ds = gdal.DEMProcessing(dstPath, dataset, 'aspect',format = 'GTiff', alg='ZevenbergenThorne', scale=111120, zFactor=30)
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i = i + 1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    min, max, d = reading_raster_band(dstPath)
    histogram(min, max, dst_ds)
    dst_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    dst_ds = None
    return dstPath

def hillshade():
    dstPath, dataset = create_raster_dataset_as_per_other_dataset()
    dst_ds = gdal.DEMProcessing(dstPath, dataset, 'hillshade', format='GTiff', alg='ZevenbergenThorne', multiDirectional=True, computeEdges=True, scale=111120, zFactor=30)
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i = i + 1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    dst_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])

def tpi():
    dstPath, dataset = create_raster_dataset_as_per_other_dataset()
    dst_ds = gdal.DEMProcessing(dstPath, dataset, 'tpi', format='GTiff')
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i = i + 1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    dst_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])

def tri():
    dstPath, dataset = create_raster_dataset_as_per_other_dataset()
    dst_ds = gdal.DEMProcessing(dstPath, dataset, 'tri', format='GTiff')
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i = i + 1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    dst_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])


def roughness ():
    dstPath, dataset = create_raster_dataset_as_per_other_dataset()
    dst_ds = gdal.DEMProcessing(dstPath, dataset, 'roughness', format='GTiff')
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i = i + 1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    dst_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])


def get_extent(fn):
    ds = gdal.Open(fn)
    gt = ds.GetGeoTransform()
    return (gt[0], gt[3], gt[0] + gt[1] * ds.RasterXSize, gt[3] + gt[5] * ds.RasterYSize)

def mosiac():
    print "Fetching all files from directory"
    file_path = str(input("Enter the path of directory where all files are stored"))
    os.chdir(file_path)
    file=glob.glob('*.tif')
    #print file
    min_x, max_y, max_x, min_y = get_extent(file[0])
    for fn in file[1:]:
        minx, maxy, maxx, miny = get_extent(fn)
        min_x = min(min_x,minx)
        max_y = max(max_y,maxy)
        max_x = max(max_x,maxx)
        min_y = min(min_y,miny)
    in_ds = gdal.Open(file[0])
    gt =  list(in_ds.GetGeoTransform())
    rows = math.ceil((max_y-min_y)/-gt[5])
    col = math.ceil((max_x - min_x) / gt[1])
    folderLocation, folderName = creating_directory()
    print "Please Provide Information Regarding New Dataset which will store all Final Information"
    name = input("Enter Dataset Name")
    dstPath = os.path.join(folderLocation, "%s.tif" % name)
    fileformat = in_ds.GetDriver().ShortName
    driver = gdal.GetDriverByName(str(fileformat))
    dst_ds = driver.Create(dstPath, int(col), int(rows), in_ds.RasterCount, GDT_Int16)
    dst_ds.SetProjection(in_ds.GetProjection())
    gt[0],gt[3]=min_x,max_y
    dst_ds.SetGeoTransform(gt)
    out_band=dst_ds.GetRasterBand(1)
    for fn in file:
        in_ds = gdal.Open(fn)
        trans=gdal.Transformer(in_ds,dst_ds,[])
        sucess,xyz=trans.TransformPoint(False,0,0)
        x,y,z = map(int,xyz)
        data = in_ds.GetRasterBand(1).ReadAsArray()
        out_band.WriteArray(data,x,y)
    dst_ds.FlushCache()
    for i in range(dst_ds.RasterCount):
        i = i + 1
        dst_ds.GetRasterBand(i).ComputeStatistics(False)
    dst_ds.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
    out_band.FlushCache()
    dst_ds = None
    dst_ds = None
    in_ds=None
    out_band=None
    return dstPath

mosiac()

def histogram(min,max,datasource):
    dst_ds=datasource
    for i in range(dst_ds.RasterCount):
        i=i+1
        band = dst_ds.GetRasterBand(i)
        bin=int(max-min)
        exact_hist = band.GetHistogram(min,max,bin,approx_ok=False)
        #print('Exact:', exact_hist[:],len(exact_hist[:]),sum(exact_hist))


def reclassify():
    directory_path= str(input('enter diectory path'))
    os.chdir(directory_path)
    fileName = str(input("file name"))
    datasource = gdal.Open(fileName)
    fileformat = datasource.GetDriver().ShortName
    driver = gdal.GetDriverByName(str(fileformat))
    ds = driver.Create('dem_class4.tif', datasource.RasterXSize, datasource.RasterYSize, 1, gdal.GDT_Byte)
    band=ds.GetRasterBand(1)
    colors=gdal.ColorTable()
    Number_of_class = int(input("enter number of class for classification"))
    for i in range(Number_of_class):
        color_tuple=[]
        Number_of_class = int(input("enter number of color to be entered"))
        for j in range (Number_of_class):
            color = int(input("enter color number"))
            color_tuple.append(color)
        colors.SetColorEntry(i,tuple(color_tuple))
    band.SetRasterColorTable(colors)
    band.SetRasterColorInterpretation(gdal.GCI_PaletteIndex)
    del band, ds

def create_RAT():
    dst_ds = open_File()
    for i in range(dst_ds.RasterCount):
        i=i+1
        band = dst_ds.GetRasterBand(i)
        band.SetNoDataValue(-1)
        rat=gdal.RasterAttributeTable()
        rat.CreateColumn('Value',gdal.GFT_Integer,gdal.GFU_Name)
        rat.CreateColumn('Value', gdal.GFT_Integer, gdal.GFU_Generic)
        rat.CreateColumn('Value', gdal.GFT_String, gdal.GFU_Generic)
        rat.SetRowCount(6)
        rat.WriteArray(range(6),0)
        rat.SetValueAsInt(0, 1, 1)
        rat.SetValueAsInt(1,1,4)
        rat.SetValueAsInt(2, 1, 3)
        rat.SetValueAsInt(3, 1, 7)
        rat.SetValueAsInt(4, 1, 2)
        rat.SetValueAsInt(5, 1, 6)
        rat.SetValueAsString(0, 2, '0-1000')
        rat.SetValueAsString(1, 2,'1000-2000' )
        rat.SetValueAsString(2, 2, '2000-3000')
        rat.SetValueAsString(3, 2, '3000-4000')
        rat.SetValueAsString(4, 2, '4000-5000')
        rat.SetValueAsString(5, 2, '5000-6000')
        band.SetDefaultRAT(rat)
        rat.DumpReadable()
        band.SetNoDataValue(0)
        print rat
        del band,dst_ds


def reclassify_raster(path,target_rasterPath):
    print("Opening dataset to reclassify it")
    slope_datasource, slope_filePath=open_File(path)
    if target_rasterPath is None:
        target_raster_p,target_raster_dataset,filePath = create_raster_dataset_as_per_other_dataset (slope_filePath,  slope_datasource)
    else:
        target_raster_p=target_rasterPath
    filePath=slope_filePath
    datasource=slope_datasource
    min,max,d=reading_raster_band(filePath)
    #target_raster_path, datasource = create_raster_dataset_as_per_other_dataset()
    target_no_data=-1
    for i in range(datasource.RasterCount):
        i = i + 1
        band = datasource.GetRasterBand(i)
        base_raster_path_band=(filePath,i)
        #a = np.arange(-1024, 6608, 1)
        #list = np.arange(6608)
        pg.geoprocessing.reclassify_raster(base_raster_path_band,value_map=d,target_raster_path=target_raster_p,target_datatype=gdal.GDT_Float32, target_nodata=target_no_data,values_required=True)
        datasource, path=open_File(target_raster_p)
        datasource.BuildOverviews('average', [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048])
        reclass=None
        return target_raster_p

#reclassify_raster(path="I:\Data\shashankdata\HAMIRPURRASTER\MOSIAC\MOSIAC.tif",target_rasterPath=None)

def zonal_statistics(path="G:\Data\shashankdata\pointshp/New.tif",source="G:\Data\shashankdata\LSMDATASET\Roadbuffer\Roadbuffer.shp"):
    vector_dataset=source = ogr.Open(source)
    raster_datasource,raster_path=open_File(path)
    for i in range(raster_datasource.RasterCount):
        i = i + 1
        base_raster_path_band = (raster_path, i)
        layer = vector_dataset.GetLayer()
        schema = {}
        ldefn = layer.GetLayerDefn()
        for n in range(ldefn.GetFieldCount()):
            fdefn = ldefn.GetFieldDefn(n)
            schema[n] = fdefn.name
        print schema
        index = int(input("Enter index number corresponding to field"))

        aggregate_vector_path="I:\Data\shashankdata\LSMDATASET\CHAMBASHP\CHAMBASHP.shp"
        dic=pg.geoprocessing.zonal_statistics(base_raster_path_band, aggregate_vector_path, aggregate_field_name="%s"%schema[index], aggregate_layer_name=None, ignore_nodata=True, all_touched=False, polygons_might_overlap=True)
        print dic

#zonal_statistics(path="I:\Data\shashankdata\Roadbuffer\ROADBUFFER\INVENTORYClip.tif",source="I:\Data\shashankdata\LSMDATASET\CHAMBASHP\CHAMBASHP.shp")


def vec2rast(rasterpath,vectorpath):
    schema = {}
    if rasterpath is None:
        rasterpath = str(input("Enter path of raster"))
    if vectorpath is None:
        filepath = str(input("Enter vector path"))
    source = ogr.Open(filepath)
    numLayers = num_of_layers_in_file(source)
    for layerIndex in range(numLayers):
        layer = source.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(source, numLayers)
        for featureIndex in range(numFeatures):
            print "feature number %d" % featureIndex
            feature = layer.GetFeature(featureIndex)
    ldefn = layer.GetLayerDefn()
    for n in range(ldefn.GetFieldCount()):
        fdefn = ldefn.GetFieldDefn(n)
        schema[n] = fdefn.name
    print schema
    index = int(input("Enter index number corresponding to field"))
    print ldefn.GetFieldBy("%s" % schema[index])
    pg.geoprocessing.rasterize(filepath,rasterpath, burn_values=[255], option_list=["ATTRIBUTE= %s" % schema[index]], layer_index=0)

#vec2rast(rasterpath=None,vectorpath=None)





def raster_calculator():
    raster_list=[]
    number_of_raster = int(input("raster number"))
    for i in range(number_of_raster):
        dataset, filepath = open_File()
        band_number = int(input("band number"))
        band = dataset.GetRasterBand(band_number)
        value = band.ReadAsArray()
        raster_list.append (value)
    a = 0 * (len(raster_list[0]))
    for i in range(len(raster_list)):
        a = np.add(raster_list[i], a)
    print a


def create_raster_from_vector(path):
    reply = str(input("WANT TO MAKE RASTER FOR ALL FEATURE OR INDIVIDUAL FEATURE ALL/INDIVIDUAL"))
    if reply=="ALL":
        target_pixel_size=reading_raster(path)
        base_vector_path = str(input("base vector path"))
        vector = ogr.Open(base_vector_path)
        shp_extent = None
        for layer in vector:
            for feature in layer:
                feature_extent = feature.GetGeometryRef().GetEnvelope()
                if shp_extent is None:
                    shp_extent = list(feature_extent)
                else:
                # expand bounds of current bounding box to include that
                # of the newest feature
                    shp_extent = [
                        f(shp_extent[index], feature_extent[index])
                        for index, f in enumerate([min, max, min, max])]

        # round up on the rows and cols so that the target raster encloses the
        # base vector
        n_cols = int(np.ceil(
            abs((shp_extent[1] - shp_extent[0]) / target_pixel_size[0])))
        n_rows = int(np.ceil(
            abs((shp_extent[3] - shp_extent[2]) / target_pixel_size[1])))

        driver = gdal.GetDriverByName('GTiff')
        n_bands = 1
        folderLocation, folderName = creating_directory()
        print "Please Enter detail regarding new raster dataset"
        name = input("Enter Dataset Name")
        dstPath = os.path.join(folderLocation, "%s.tif" % name)
        raster = driver.Create(dstPath, n_cols, n_rows, n_bands,GDT_Float32)
        target_nodata=int(-10)
        raster.GetRasterBand(1).SetNoDataValue(target_nodata)

        # Set the transform based on the upper left corner and given pixel
        # dimensions
        if target_pixel_size[0] < 0:
            x_source = shp_extent[1]
        else:
            x_source = shp_extent[0]
        if target_pixel_size[1] < 0:
            y_source = shp_extent[3]
        else:
            y_source = shp_extent[2]
        raster_transform = [
            x_source, target_pixel_size[0], 0.0,
            y_source, 0.0, target_pixel_size[1]]
        raster.SetGeoTransform(raster_transform)

        # Use the same projection on the raster as the shapefile
        raster.SetProjection(vector.GetLayer(0).GetSpatialRef().ExportToWkt())
        fill_value=1
        # Initialize everything to nodata
        if fill_value is not None:
            band = raster.GetRasterBand(1)
            band.Fill(fill_value)
            band.FlushCache()
            band = None
        raster = None
    else:
        folderLocation, folderName = creating_directory()
        target_pixel_size = reading_raster(path)
        base_vector_path = str(input("base vector path"))
        vector = ogr.Open(base_vector_path)
        shp_extent = None
        for layer in vector:
            for feature in layer:
                feature_extent = feature.GetGeometryRef().GetEnvelope()
                n_cols = int(np.ceil(
                    abs((feature_extent[1] - feature_extent[0]) / target_pixel_size[0])))
                n_rows = int(np.ceil(
                    abs((feature_extent[3] - feature_extent[2]) / target_pixel_size[1])))

                driver = gdal.GetDriverByName('GTiff')
                n_bands = 1
                print "Please Enter detail regarding new raster dataset"
                name = input("Enter Dataset Name")
                dstPath = os.path.join(folderLocation, "%s.tif" % name)
                raster = driver.Create(dstPath, n_cols, n_rows, n_bands, GDT_Float32)
                target_nodata = int(-10)
                raster.GetRasterBand(1).SetNoDataValue(target_nodata)

                # Set the transform based on the upper left corner and given pixel
                # dimensions
                if target_pixel_size[0] < 0:
                    x_source = feature_extent[1]
                else:
                    x_source = feature_extent[0]
                if target_pixel_size[1] < 0:
                    y_source = feature_extent[3]
                else:
                    y_source = feature_extent[2]
                raster_transform = [
                    x_source, target_pixel_size[0], 0.0,
                    y_source, 0.0, target_pixel_size[1]]
                raster.SetGeoTransform(raster_transform)

                # Use the same projection on the raster as the shapefile
                raster.SetProjection(vector.GetLayer(0).GetSpatialRef().ExportToWkt())
                fill_value = 1
                # Initialize everything to nodata
                if fill_value is not None:
                    band = raster.GetRasterBand(1)
                    band.Fill(fill_value)
                    band.FlushCache()
                    band = None
                raster = None
#create_raster_from_vector(path="I:\Data\shashankdata\LSMDATASET\MOSIAC\MOSIAC.tif")

def raster_info():
    r=str(input("want information for group yes\No"))
    if r=="yes":
        print "Fetching all files from directory"
        file_path = str(input("Enter the path of directory where all files are stored"))
        os.chdir(file_path)
        file = glob.glob('*.tif')
        for i in range(len(file)):
            rasterinfo = pg.geoprocessing.get_raster_info(file[i])
            print rasterinfo,file[i]
    else:
        raster_path=str(input("enter raster path for getting its info"))
        rasterinfo=pg.geoprocessing.get_raster_info(raster_path)
        print rasterinfo

#raster_info()

def vector_info():
    vector_path=str(input("enter vector path for getting its info"))
    vectorinfo=pg.geoprocessing.get_vector_info(vector_path,layer_index=0)
    print vectorinfo



def offset_info(P):
    a=[]
    b=[]
    c=["I:\Data\shashankdata\LSMDATASET\MOSIAC\MOSIAC.tif",P]
    for i in range(2):
        #raster_path=str(input("enter raster path for getting its info"))
        rasterinfo=pg.geoprocessing.get_raster_info(c[i])
        print rasterinfo
        a.append(rasterinfo['geotransform'][0])
        a.append(rasterinfo['geotransform'][3])
        b.append(rasterinfo['geotransform'][1])
        b.append(rasterinfo['geotransform'][5])
        print a,b

    x=((a[2]-a[0])/b[0])
    y=((a[3]-a[1])/b[1])
    #print math.ceil(x),math.floor(y)
    return int(math.ceil(x)),int(math.floor(y))


#offset_info()


def small_raster(path):
    b_box_feat = None
    target_pixel_size = reading_raster(path)
    vector = ogr.Open("I:\Data\shashankdata\HAMIRPUR\HAMIRPUR.shp")
    for layer in vector:
        b_box_feat = [feature.GetGeometryRef().GetEnvelope() for feature in layer]
    block = [100, 100]
    n_cols = block[0]
    n_rows = block[1]
    m=0
    for l in range(len(b_box_feat)):
        folderLocation, folderName = creating_directory()
        k=0
        m+=1
        while 1:
            x_source = b_box_feat[l][0] + (target_pixel_size[0] * n_cols * k)
            j=0
            while 1:
                driver = gdal.GetDriverByName('GTiff')
                n_bands = 1
                print "Please Enter detail regarding new raster dataset"
                name = "A%dB%dC%d" % (m,k,j)
                dstPath = os.path.join(folderLocation, "%s.tif" % name)
                raster = driver.Create(dstPath, n_cols, n_rows, n_bands, GDT_Float32)
                y_source = b_box_feat[l][2] - (target_pixel_size[1] * n_rows * j)
                raster_transform = [x_source, target_pixel_size[0], 0.0,y_source, 0.0, target_pixel_size[1]]
                raster.SetGeoTransform(raster_transform)
                # Use the same projection on the raster as the shapefile
                raster.SetProjection(vector.GetLayer(0).GetSpatialRef().ExportToWkt())
                fill_value = 1
                # Initialize everything to nodata
                if fill_value is not None:
                    band = raster.GetRasterBand(1)
                    band.Fill(fill_value)
                    band.FlushCache()
                    band = None
                if  y_source < b_box_feat[0][3]:
                    j += 1
                    print j
                    pass
                else:
                    print "***********************************************************************************************************\
                    *******************************************************************************************************"

                    break
            if x_source < b_box_feat[0][1]:
                k += 1
                print k
                raster=None
                pass
            else:
                break
        '''r=str(input("want to do it for next feature yes\no"))
        if r=="yes":
            pass
        else:
            break'''



#small_raster(path="I:\Data\shashankdata\LSMDATASET\MOSIAC\MOSIAC.tif")

def tuple_generator(raster_ind_list,path):
    oarray = None
    dstPath=None
    output_raster_blocks=None
    fc = ls.FuzzyController()
    #file_path = str(input("Enter the path of directory where all files are stored"))
    astype = np.float32
    raster_index_list = []
    if raster_ind_list is None:
        number_of_raster = int(input("raster number"))
        for i in range(number_of_raster):
            dataset, filepath = open_File(path=None)
            raster_index_list.append(dataset)
    else:
        for m in range(len(raster_ind_list)):
            dataset, filepath = open_File(str(raster_ind_list[m]))
            raster_index_list.append(dataset)
        number_of_raster = len(raster_index_list)
    band_index_list=None
    if band_index_list is None:
        band_index_list = [raster.RasterCount for raster in raster_index_list]
    band_list = [raster.GetRasterBand(index) for index, raster in zip(band_index_list, raster_index_list)]
    file_path ="I:\Data\shashankdata\HAMIRPURRASTER\U"
    os.chdir(file_path)
    print file_path
    file = glob.glob('*.tif')
    for g in range(len(file)):
        print "Give iteration information"
        x, y = offset_info(file[g])
        '''reply = str(input("DO YOU HAVE RASTER DATASET YES/NO"))
        if reply == "NO":
            print"for creating target raster provide base raster path"
            datasource, path = open_File(path)
            dstPath, dataset, filepath = create_raster_dataset_as_per_other_dataset(path, datasource)
        else:
            # dstPath=str(input("enter path of raster dataset"))'''
        dstPath = str(file[g])
        print"opening target raster"
        target_raster = gdal.Open(dstPath, gdal.GA_Update)
        target_band = target_raster.GetRasterBand(1)
        block = [100,100]
        cols_per_block = block[0]
        rows_per_block = block[1]
        n_cols = target_band.XSize+x
        n_rows = target_band.YSize+y
        n_col_blocks = int(math.ceil(n_cols / float(cols_per_block)))
        n_row_blocks = int(math.ceil(n_rows / float(rows_per_block)))
        last_row_block_width = None
        last_col_block_width = None
        tie=[]
        if astype is not None:
            block_type_list = [astype] * len(band_list)
        for row_block_index in xrange(n_row_blocks):
            row_offset = (row_block_index * rows_per_block)+ y
            #row_offset = (row_block_index * rows_per_block) + y
            row_block_width = n_rows - row_offset
            if row_block_width > rows_per_block:
                row_block_width = rows_per_block
            elif row_block_width==0:
                break

            for col_block_index in xrange(n_col_blocks):
                col_offset = (col_block_index * cols_per_block)+ x
                #col_offset = (col_block_index * cols_per_block) + x
                col_block_width = n_cols - col_offset
                if col_block_width > cols_per_block:
                    col_block_width = cols_per_block
                elif col_block_width==0:
                    break

                # resize the raster block cache if necessary
                if (last_row_block_width != row_block_width or
                        last_col_block_width != col_block_width):
                    raster_blocks = [np.zeros((row_block_width, col_block_width), dtype=block_type) for block_type in block_type_list]


                offset_dict_read = {
                    'xoff': col_offset,
                    'yoff': row_offset,
                    'win_xsize': col_block_width,
                    'win_ysize': row_block_width,
                }
                offset_dict_write = {
                    'xoff': col_offset-x,
                    'yoff': row_offset-y,
                    'win_xsize': col_block_width,
                    'win_ysize': row_block_width,
                }

                dic = {}
                for i in range(number_of_raster):
                    band_list[i].ReadAsArray(buf_obj=raster_blocks[i], **offset_dict_read)
                    dic[i] = np.array(raster_blocks[i])
                o=None
                for s,a,e,u in zip(dic[0].flatten(),dic[1].flatten(),dic[2].flatten(),range(len(dic[0].flatten()))):
                    k=(s,a,e)
                    #print k
                    if s<0 or a<0:
                        o=-1
                    else:
                        o = fc.controller(s,a,e)
                    tie.append(o)
                oarray=np.asarray(tie,dtype=astype)
                target_band.WriteArray(oarray.reshape(row_block_width, col_block_width), xoff=offset_dict_write['xoff'],yoff=offset_dict_write['yoff'])
                print "*********************************************************************************************block over****************************************************************************************************************************"
                target_band.FlushCache()
    gc.collect()

#tuple_generator(raster_ind_list=["I:\Data\shashankdata\LSMDATASET\RECLASSSLOPE\RECLASSSLOPE.tif","I:\Data\shashankdata\LSMDATASET\RECLASSASPECT\RECLASSASPECT.tif","I:\Data\shashankdata\LSMDATASET\MOSIAC\ELEVATIONRECLASS\ELEVATIONRECLASS.tif"],path="I:\Data\shashankdata\LSMDATASET\MOSIAC\MOSIAC.tif")























