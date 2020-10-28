from __future__ import division
import ogr
import glob
import gdal
import osr
import osgeo
import numpy as np
import os, os.path, shutil
import osgeo.ogr
import osgeo.osr
from gdalconst import *
import csv
import xlrd
from osgeo import ogr
from TEST1.TASTE1.gis.vector.write import *

from math import radians, cos, sin, asin, sqrt, atan2, degrees,ceil

def get_extent(fn):
    ds = gdal.Open(fn)
    gt = ds.GetGeoTransform()
    return (gt[0], gt[3], gt[0] + gt[1] * ds.RasterXSize, gt[3] + gt[5] * ds.RasterYSize)


def mosiac(path):
    print ("Fetching all files from directory")
    file_path = str(path)
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
    rows = ceil((max_y-min_y)/-gt[5])
    col = ceil((max_x - min_x) / gt[1])
    folderLocation, folderName = creating_directory()
    print ("Please Provide Information Regarding New Dataset which will store all Final Information")
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

def xls (filePath):
    with open(filePath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        coord=[]
        for (row) in(spamreader):
            a = row[0].split(',') #as row is list containing all column element as single string eg: ['col,col2,co3,...,coln'], hence row[0] means first element of list.
            tuple=(a[1], a[2])
            coord.append(tuple)
        return coord

def open_File_1(path):
    if path is None:
        filePath = str(input("file path"))
    else:
        filePath=path
    datasource = ogr.Open(filePath,0)
    return datasource





def route(finalroute):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directory ()
    name = input("enter name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)
    out_row = ogr.Feature(dstLayer.GetLayerDefn())
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)
    for k in range(len(finalroute)):
        print (finalroute[k].GetGeometryRef())
        multipoint.AddGeometry(finalroute[k].GetGeometryRef())
    poly = {}
    for i in range(len(finalroute)):
        poly[i] = multipoint.GetGeometryRef(i)
    line = {}
    line[0] = poly[0]
    for i in range(len(finalroute) - 1):
        line[i + 1] = poly[i + 1].Union(line[i])
    out_row.SetGeometry(line[len(finalroute) - 1])
    dstLayer.CreateFeature(out_row)
    dstFile.Destroy()


def create_a_point(w,filePath) :
    coord=xls(filePath)
    long= (coord[w][0])
    lat=coord[w][1]
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(long),float(lat))
    return point.ExportToWkt()


def creating_directory():
    folderName = input("Enter Folder Name")
    folderPath = input("Where you want to save folder ")
    path = folderPath + '\\' + folderName
    print (path)
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)


def csvtoshp (filePath):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print ("Creating Directory For ShapeFile ")
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    numField = input("Enter the required number of fields\ attributes in a layer other than FieldID, Longitude, Latitude")
    fieldDef = osgeo.ogr.FieldDefn("FieldID", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("Longitude", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("Latitude", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("WEIGHT", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    list = {"Integer": 1, "IntegerList": 2, "Real": 3, "RealList": 4, "String": 5, "StringList": 6, "WideString": 7,
            "WideStringList": 8, "Binary": 9, "Date": 10, "Time": 11, "DateTime": 12, "Integer64": 13,
            "Integer64List": 14}
    print (list)
    fieldList = []
    for i in range(numField):
        ftype = input("please enter number corresponding to the type of field you want to make (integer value)")
        if ftype == 1:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTInteger)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 2:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTIntegerList)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 3:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTReal)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 4:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTRealList)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 5:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTString)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 6:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTStringList)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 7:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTWideString)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 8:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTWideStringList)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 9:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTBinary)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 10:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTDate)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 11:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTTime)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 12:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTDateTime)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 13:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTInteger64)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype == 14:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTInteger64List)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
    j = 0
    num = input("enter number of point")
    for  w in range(num+1):
        w+=1
        j = j + 1
        Q=create_a_point(w, filePath)
        point = ogr.CreateGeometryFromWkt(Q)
        print (w)
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField("FieldID", j)
        feature.SetField("Longitude", point.GetX())
        feature.SetField("Latitude", point.GetY())
        feature.SetField("WEIGHT", 1)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    dstFile.Destroy()




def haversine(pointA, pointB):

    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = pointA[1]
    lon1 = pointA[0]
    lat2 = pointB[1]
    lon2 = pointB[0]

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def open_File():
    filePath = str(input("file path"))
    print ("Entered File Path is %s" % filePath)
    datasource = ogr.Open(filePath)
    return datasource

def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    print ("the number of Layers in the file on the entered file path is %d" % numLayers)
    return numLayers



def creating_an_empty_shape_file(geom):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print ("Creating Directory For ShapeFile ")
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    numField = input(
        "Enter the required number of fields\ attributes in a layer other than FieldID, Longitude, Latitude")
    fieldDef = osgeo.ogr.FieldDefn("FieldID", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    print ("point geometry")
    for i in range(len(geom)):
        point = ogr.CreateGeometryFromWkt(geom[i])
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField("FieldID", i)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    dstFile.Destroy()
    return dstPath

def creating_test_shape_file(centroid,count):
    q=[]
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print ("Creating Directory For ShapeFile ")
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    numField = input("Enter the required number of fields\ attributes in a layer other than FieldID, Longitude, Latitude")
    fieldDef = osgeo.ogr.FieldDefn("ROW", osgeo.ogr.OFTInteger64)
    fieldDef.SetWidth(50)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("COLUMN", osgeo.ogr.OFTInteger64)
    fieldDef.SetWidth(50)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("COUNT", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(50)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("CENTROID", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    for key, value in centroid.iteritems():
        q.append(key)
    print ("point geometry")
    for i in range(len(q)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(centroid[q[i]][0],centroid[q[i]][1])
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField("COLUMN", q[i][0])
        feature.SetField("ROW", q[i][1])
        feature.SetField("COUNT", count[q[i]])
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    dstFile.Destroy()
    return dstPath

def making_one_from_all(file_path):
    list=[]
    os.chdir(file_path)
    file = glob.glob('*.shp')
    for i in range(len(file)):
        datasource = open_File_1(file[i])
        numLayers = num_of_layers_in_file(datasource)
        for layerIndex in range(numLayers):
            layer = datasource.GetLayerByIndex(layerIndex)
            numFeatures = num_of_features_in_layer(datasource, numLayers)
            for featureIndex in range(numFeatures):
                print ("feature number %d" % featureIndex)
                feature = layer.GetFeature(featureIndex)
                geometry = feature.GetGeometryRef().ExportToWkt()
                list.append(geometry)
    path=creating_an_empty_shape_file(list)
    return path,list

def mean(filepath):
    x=[]
    l=[]
    y=[]
    xtotal=0
    ytotal=0
    datasource = open_File_1(filepath)
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            geomX = feature.GetGeometryRef().GetX()
            geomY = feature.GetGeometryRef().GetY()
            x.append(geomX)
            y.append(geomY)
    for i in range(len(x)):
        xtotal = xtotal + x[i]
    for i in range(len(x)):
        ytotal = ytotal + y[i]
    xmean=xtotal/ len(x)
    ymean=ytotal/len(y)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(xmean, ymean)
    l.append(point.ExportToWkt())
    path=creating_an_empty_shape_file(l)
    return path,(xmean,ymean)

def point_list(filepath):
    x=[]
    datasource = open_File_1(filepath)
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            geomX = feature.GetGeometryRef().GetX()
            geomY = feature.GetGeometryRef().GetY()
            a=(geomX,geomY)
            x.append(a)
    return x



def std(crimefilepath,meanfilepath):
    d=[]
    total=0
    l=[]
    print ("CRIMEPOINT")
    crimepointlist=point_list(crimefilepath)
    print ("MEAN CRIME POINT")
    meanpointlist=point_list(meanfilepath)
    print ("done")
    for i in range(len(crimepointlist)):
        pointA=crimepointlist[i]
        E=haversine(pointA,meanpointlist[0])
        print (E)
        d.append(E**2)
        print (d)
    for i in range(len(d)):
        total=total+d[i]
    print (total)
    avgsquareroot=sqrt(total)/len(d)
    print (avgsquareroot)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(meanpointlist[0][0],meanpointlist[0][1])
    poly = point.Buffer(avgsquareroot/100)
    l.append(poly.ExportToWkt())
    creating_an_empty_shape_file(l)

def featurelist (filepath):
    x=[]
    datasource = open_File_1(filepath)
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        for feature in layer:
            x.append(feature)
    return x


def envelop(filepath):
    x=featurelist(filepath)
    env=x[0].GetGeometryRef().GetEnvelope()
    print (env)
    return env


def fish_net(env,gridHeight=0.005,gridWidth=0.005):
    dictionary_1={}

    # convert sys.argv to float
    xmin = float(env[0])
    xmax = float(env[1])
    ymin = float(env[2])
    ymax = float(env[3])
    gridWidth = float(gridWidth)
    gridHeight = float(gridHeight)

    # get rows
    rows = ceil((ymax-ymin)/gridHeight)
    # get columns
    cols = ceil((xmax-xmin)/gridWidth)

    # start grid cell envelope
    ringXleftOrigin = xmin
    ringXrightOrigin = xmin + gridWidth
    ringYtopOrigin = ymax
    ringYbottomOrigin = ymax-gridHeight

    # create output file
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print ("Creating Directory For ShapeFile ")
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    numField = input(
        "Enter the required number of fields\ attributes in a layer other than FieldID, Longitude, Latitude")
    fieldDef = osgeo.ogr.FieldDefn("ROW", osgeo.ogr.OFTInteger64)
    fieldDef.SetWidth(50)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("COLUMN", osgeo.ogr.OFTInteger64)
    fieldDef.SetWidth(50)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("COUNT", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(50)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("CENTROID", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    featureDefn = dstLayer.GetLayerDefn()

    # create grid cells
    countcols = 0
    while countcols < cols:
        countcols += 1
        # reset envelope for rows
        ringYtop = ringYtopOrigin
        ringYbottom =ringYbottomOrigin
        countrows = 0
        while countrows < rows:
            countrows += 1
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYtop)
            ring.AddPoint(ringXrightOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYbottom)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            dictionary_1[(countcols,countrows)]=(ringXleftOrigin,ringXrightOrigin,ringYtop,ringYbottom)
            # add new geom to layer
            outFeature = ogr.Feature(featureDefn)
            outFeature.SetGeometry(poly)
            outFeature.SetField("COLUMN", countcols)
            outFeature.SetField("ROW", countrows)
            dstLayer.CreateFeature(outFeature)
            outFeature.Destroy()
            # new envelope for next poly
            ringYtop = ringYtop - gridHeight
            ringYbottom = ringYbottom - gridHeight
        # new envelope for next poly
        ringXleftOrigin = ringXleftOrigin + gridWidth
        ringXrightOrigin = ringXrightOrigin + gridWidth
    # Save and close DataSources
    dstFile.Destroy()
    for key,value in dictionary_1.iteritems():
        target_ds = gdal.GetDriverByName('GTiff').Create("C:/Users\Hp\Desktop\pol\RASTER\%d%d.tif"%(key[0],key[1]), 1,1,1, GDT_Float32)
        target_ds.SetGeoTransform((dictionary_1[key][0], 0.005, 0,dictionary_1[key][2], 0, -0.005))
        band = target_ds.GetRasterBand(1)
        band.SetNoDataValue(100000000)
    return dictionary_1




def poly_in_fish():
    i=0
    poly={}
    datasource = ogr.Open("C:/Users\Hp\Desktop\pol\HOTSPOTTEST\FISHNET\FISHNET.shp")
    for layer in datasource:
        for feature in layer:
            a=feature.GetField("COLUMN")
            b=feature.GetField("ROW")
            poly[(a,b)] = feature.GetGeometryRef().ExportToWkt()
    return poly


def crimecount(poly,path):
    count={}
    crimepointdatasource = open_File_1(path)
    crimepointlayer = crimepointdatasource.GetLayerByIndex(0)
    for key,value in poly.iteritems():
        a=ogr.CreateGeometryFromWkt(poly)
        crimepointlayer.SetSpatialFilter(a)
        count[key]=crimepointlayer.GetFeatureCount()
    return count



def crime_count_for_raster(env,cell_width,cell_height,crimeshp_path):
    count={}
    xmin = env[0]
    xmax = env[1]
    ymin = env[2]
    ymax = env[3]
    cols = int(ceil((xmax - xmin) / cell_width))
    rows = int(ceil((ymax - ymin) /cell_height))
    index=indentity(env,cell_width,cell_height)
    for i in range(rows):
        for j in range(cols):
            ringXleftOrigin, ringYtop=index[(i+1,j+1)]
            ring = ogr.Geometry(ogr.wkbLinearRing)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            ring.AddPoint(ringXleftOrigin+cell_width, ringYtop)
            ring.AddPoint(ringXleftOrigin+cell_width, ringYtop-cell_height)
            ring.AddPoint(ringXleftOrigin, ringYtop-cell_height)
            ring.AddPoint(ringXleftOrigin, ringYtop)
            poly = ogr.Geometry(ogr.wkbPolygon)
            poly.AddGeometry(ring)
            crimepointdatasource = open_File_1(crimeshp_path)
            crimepointlayer = crimepointdatasource.GetLayerByIndex(0)
            crimepointlayer.SetSpatialFilter(poly)
            count[(ringXleftOrigin, ringYtop)]=crimepointlayer.GetFeatureCount()
    print (len(count))
    return count,rows,cols,index

def numpy_array(count,rows,cols,index):
    print (len(index))
    l_outside=[]
    for i in range(rows):
        l_inside = []
        for j in range(cols):
            a=index[(i+1,j+1)]
            c=count[(a)]
            l_inside.append(c)
        l_outside.append(l_inside)
        del l_inside
    array=np.matrix(l_outside)
    print ("array shape",array.shape,"array size",array.size,"array length",len(array.flatten()))
    return array

def gi_star_array(rows,cols,gi_star_dics):
    l_outside = []
    for i in range(rows):
        l_inside = []
        for j in range(cols):
            a = gi_star_dics[(i + 1, j + 1)]
            l_inside.append(a)
        l_outside.append(l_inside)
        del l_inside
    array = np.matrix(l_outside)
    print ("array shape", array.shape, "array size", array.size, "array length", len(array.flatten()))
    return array


def raster(env,rows,cols,array,gridHeight=-0.005, gridWidth=0.005):
    xmin = env[0]
    ymax = env[3]
    path=str(input("ENTER PATH"))
    target_ds = gdal.GetDriverByName('GTiff').Create(path, cols,rows,1,GDT_Float32)
    target_ds.SetGeoTransform((xmin, gridWidth, 0, ymax, 0, gridHeight))
    band = target_ds.GetRasterBand(1)
    band.WriteArray(array)
    band.SetNoDataValue(100000000)
    del target_ds


def indentity(env,xwidth,yheight):
    index={}
    xmin=env[0]
    xmax=env[1]
    ymin=env[2]
    ymax=env[3]
    cols=int(ceil((xmax-xmin)/xwidth))
    rows=int(ceil((ymax-ymin)/yheight))
    for i in range(rows):
        for j in range(cols):
            a=(xmin+(j*xwidth))
            b=(ymax-(i*yheight))
            index[(i+1,j+1)]=(a,b)
    return index

def donknow(row,col,rowmax,colmax):
    r=[]
    c=[]
    cell_list=[]
    #lag=input(("PLEASE ENTER LAG DISTANCE"))
    lag=1
    for k in range(lag+1):
        if (row-k)>0:
            r.append(row-k)
        if (row+k)<rowmax or (row+k)==rowmax :
            r.append(row+k)
    for k in range(lag+1):
        if (col-k)>0:
            c.append(col-k)
        if (col+k)<colmax or (col+k)==colmax :
            c.append(col+k)
    for i in range(len(r)):
        for j in range(len(c)):
            cell_list.append((r[i],c[j]))
    final_list=set(cell_list)
    return list(final_list)




def centroid_1(dic):
    centroid = {}
    for key,value in dic.iteritems():
        centroid[key]=((dic[key][0]+dic[key][1])/2,(dic[key][2]+dic[key][3])/2)
    return centroid

def lag_distance(centroid):
    i=input("enter number of lag")
    pointA=centroid[(1,1)]
    pointB=centroid[(i+1,i+1)]
    dist=haversine(pointA,pointB)
    return dist

def spatial_weight_matrix(centroid,dist,(c,r)):
    w={}
    pointA = centroid[(c,r)]
    for key,value in centroid.iteritems():
        pointB=centroid[key]
        d=haversine(pointA,pointB)
        if d<dist or d==dist:
            w[key]=1
        else:
            w[key]=0
    return w


def mean_count(count):
    a=0
    b=len(count)
    for key,value in count.iteritems():
        a=a+count[key]
    mean=a/b
    print ("mean",mean,"Total Count",a)
    return mean

def std_getis_ord(count,mean):
    a = 0
    for key, value in count.iteritems():
        a = a + count[key]**2
    print ("total count square",a)
    c=sqrt((a/len(count))-(mean)**2)
    print ("sqrt of total count square minus mean square",c)
    return c



def abcd(row,col,rowmax,colmax,count,index):
    sum = 0
    l=[]
    l = donknow(row, col, rowmax, colmax)
    for o in range(len(l)):
        sum = sum + count[index[l[o]]]
    d=sqrt((len(count)*len(l)-len(l)**2)/(len(count)-1))
    print (d,"length of count",len(count))
    return d,l,sum

def Getisord(d,l,count,mean,sum):
    c=std_getis_ord(count, mean)
    f=mean*len(l)
    g=(sum-f)/(d*c)
    return g

def Gi____statistics(rowmax,colmax,index,count):
    gi_star_dics={}
    for row in range(rowmax):
        for col in range(colmax):
            d,l,sum=abcd(row+1,col+1,rowmax, colmax, count, index)
            mean=mean_count(count)
            gi_star=Getisord(d, l, count, mean, sum)
            gi_star_dics[(row+1,col+1)]=gi_star
    array=gi_star_array(rowmax, colmax, gi_star_dics)
    return array


def Gi_statistics():
    env = envelop(filepath="C:/Users\Hp\Desktop\pol\ONEFEATLIST\ONEFEATLIST.shp")
    count, rows, cols, index=crime_count_for_raster(env, 0.005, 0.005, crimeshp_path="C:/Users\Hp\Desktop\pol\LESSCRIMEFEAT\CRIMEFEAT.shp")
    array=numpy_array(count,rows,cols,index)
    raster(env, rows, cols, array, gridHeight=-0.005, gridWidth=0.005)
    array_1=Gi____statistics(rows, cols, index, count)
    raster(env, rows, cols, array_1, gridHeight=-0.005, gridWidth=0.005)


Gi_statistics()




