import ogr
import gdal
import osr
import osgeo
import os, os.path, shutil
import osgeo.ogr
import osgeo.osr
from osgeo import osr
import osgeo.ogr as ogr
import osgeo.osr as osr
from gdalconst import *
import csv








def open_File():
    filePath = str(input("file path"))
    print ("Entered File Path is %s" % filePath)
    datasource = ogr.Open(filePath)
    return datasource

def open_File_1(path):
    if path==None:
        filePath = str(input("file path"))
    else:
        filePath=path
    print ("Entered File Path is %s" % filePath)
    datasource = ogr.Open(filePath,True)
    return datasource

def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    print ("the number of Layers in the file on the entered file path is %d" % numLayers)
    return numLayers


def num_of_features_in_layer(source, Layers):
    datasource = source
    numLayers = Layers
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = layer.GetFeatureCount()
        print ("Layer (%s) has %d features:" % (layerIndex, numFeatures))
        return numFeatures

def analyzeGeometry(geometry, indent=0):
    s = []
    s.append(" " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    print ("number of geometry element %d" % geometry.GetGeometryCount())
    if geometry.GetGeometryCount() > 0:
        s.append("containing:")
    print ("".join(s))
    for i in range(geometry.GetGeometryCount()):
        analyzeGeometry(geometry.GetGeometryRef(i), indent + 1)

def get_geometry():
    datasource = open_File()
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            print (feature)
            geometry = feature.GetGeometryRef()
            name = geometry.GetGeometryName()
        return datasource,layer

def frange(start, stop, step):
    i = 0
    while (start + (i * step)) < stop:
        yield start + i * step
        i += 1

def createBuffer():
    bufferDist = []
    num = int(input("number of buffer"))
    rep = str(input('like to enter manually yes/No'))
    dist = 0
    datasource = open_File()
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        folderLocation, folderName = creating_directory()
        dstPath = os.path.join(folderLocation, "%s.shp" % folderName)
        shpdriver = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.exists(dstPath):
            shpdriver.DeleteDataSource(dstPath)
        outputBufferds = shpdriver.CreateDataSource(dstPath)
        bufferlyr = outputBufferds.CreateLayer(dstPath, layer.GetSpatialRef(), geom_type=ogr.wkbPolygon)
        out_row = ogr.Feature(bufferlyr.GetLayerDefn())
        fieldDef = osgeo.ogr.FieldDefn("distance", osgeo.ogr.OFTReal)
        fieldDef.SetWidth(32)
        bufferlyr.CreateField(fieldDef)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            print (feature)
            geometry = feature.GetGeometryRef()
            for j in range(num):
                if rep == 'yes':
                    dist = float(input("buffer distance"))
                    bufferDist.append(dist)
                else:
                    dist +=0.00001
                    bufferDist.append(dist)
            li=[]
            for i in range(len(bufferDist)):
                poly = geometry.Buffer(bufferDist[i])
                out_row.SetGeometry(poly)
                li.append(i+1)
                out_row.SetField("distance",li[i])
                bufferlyr.CreateFeature(out_row)
                print (i+1)
    datasource=None






def union():
    datasource = open_File()
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        count, list = number_of_available_drivers()
        driverName = entered_driver_availiblity(count, list)
        driver = osgeo.ogr.GetDriverByName("%s" % driverName)
        folderLocation, folderName = creating_directory()
        name = input("enter shape file name")
        dstPath = os.path.join(folderLocation, "%s.shp" % name)
        dstFile = driver.CreateDataSource("%s" % dstPath)
        dstLayer = dstFile.CreateLayer("resulting layer", layer.GetSpatialRef(), ogr.wkbLineString)
        out_row = ogr.Feature(dstLayer.GetLayerDefn())
        multilinestring = ogr.Geometry(ogr.wkbMultiLineString)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print "feature number %d" % featureIndex
            feature = layer.GetFeature(featureIndex)
            print feature
            geometry = feature.GetGeometryRef().Clone()
            name = geometry.GetGeometryName()
            multilinestring.AddGeometry(geometry)
        poly={}
        for i in range(numFeatures):
            poly[i]=multilinestring.GetGeometryRef(i)

        line = {}
        line[0]=poly[0]
        for i in range(numFeatures-1):
            a = poly[i+1].Union(line[i])
            line[i+1]=a
        out_row.SetGeometry(line[numFeatures-1])
        dstLayer.CreateFeature(out_row)


#union()
#createBuffer()


"G:\Data\shashankdata\Factorlayer\Road.shp,ESRI Shapefile"



def Geometry_Analysis ():
    geometry =get_geometry()
    analyzeGeometry(geometry, indent=0)


def get_Area():
    geometry = get_geometry()
    print "Area = %d" % geometry.GetArea()

def envelop():
    geometry = get_geometry()
    env = geometry.GetEnvelope()
    print "minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3])

def Length ():
    geometry = get_geometry()
    print "Length = %d" % geometry.Length()

def intersection_of_geometry():
    poly1= get_geometry()
    poly2= get_geometry()
    intersection = poly1.Intersection(poly2)
    return intersection

'''def union():
    poly1 = get_geometry()
    poly2 = get_geometry()
    union = poly1.Union(poly2)
    return union()'''


def get_spatial_reference():
    source = open_File()
    numLayers=num_of_layers_in_file(source)
    for layerNum in range(numLayers):
        layer = source.GetLayer(layerNum)
        spatialRef = layer.GetSpatialRef()
        spatialRef_1 = layer.GetSpatialRef().ExportToProj4()
        print "Layer %d has spatial reference %s" % (layerNum, spatialRef)
        print "Layer %d has proj spatial reference %s" % (layerNum, spatialRef_1)
        return (spatialRef,spatialRef_1)



