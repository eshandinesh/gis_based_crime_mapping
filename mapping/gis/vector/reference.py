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
import mapnik

def open_File():
    filePath = str(input("file path"))
    print "Entered File Path is %s" % filePath
    datasource = ogr.Open(filePath)
    return datasource


def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    print "the number of Layers in the file on the entered file path is %d" % numLayers
    return numLayers


def num_of_features_in_layer(source, Layers):
    datasource = source
    numLayers = Layers
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = layer.GetFeatureCount()
        print "Layer (%s) has %d features:" % (layerIndex, numFeatures)
        return numFeatures

def Transform():
    geographicCoordinateSystem = ["WGS84","WGS72", "NAD27", "NAD83", "EPSG:4326", "EPSG:4322" , "EPSG:4267", "EPSG:4269" ]
    projectionCordinateSystem = []
    x = 0
    y = 59
    while x <= y:
        x = x + 1
        projectionCordinateSystem.append(x)
    reply = input("whether want to see Geographic Coordinate System list answer in yes/no")
    if reply == "yes":
        print "\n".join(geographicCoordinateSystem)
    gcs = input("Enter Geographic Coordinate System's name:")
    srcProjection = osr.SpatialReference()
    srcProjection.SetWellKnownGeogCS("%s" % gcs)
    reply = input("whether want to see projection System list answer in yes/no")
    if reply == "yes":
        print projectionCordinateSystem
    pcs = input("Enter projection Coordinate System's zone number:")
    hemisphere= input("Enter type of  hemisphere north or south")

    dstProjection = osr.SpatialReference()
    if hemisphere=="north":
        dstProjection.SetUTM("%d" % (pcs),int(1))  # Lat/long.
    else:
        dstProjection.SetUTM("%d" % (pcs), int(0))
    transform = osr.CoordinateTransformation(srcProjection, dstProjection)
    return transform




def transformation_using_Ogr(source, Layers, Transformation):
    datasource = source
    numLayers = Layers
    transform = Transformation
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(source, Layers)
        for featureIndex in range(numFeatures):
            print "feature number %d" % featureIndex
            feature = layer.GetFeature(featureIndex)
            geometry = feature.GetGeometryRef()
            newGeometry = geometry.Clone()
            print "old geometry is %s" % newGeometry
            newGeometry.Transform(transform)
            print "new geometry is %s" % newGeometry

def open_File():
    filePath = str(input("file path"))
    print "Entered File Path is %s" % filePath
    datasource = ogr.Open(filePath)
    return datasource

def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    print "the number of Layers in the file on the entered file path is %d" % numLayers
    return numLayers

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


def creating_directory():
    folderName = input("Enter Folder Name")
    folderPath = input("Where you want to save folder ")
    path = folderPath + '\\' + folderName
    print path
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)

def number_of_available_drivers():
    cnt = ogr.GetDriverCount()
    formatsList = []  # Empty List
    for i in range(cnt):
        driver = ogr.GetDriver(i)
        driverName = driver.GetName()
        if not driverName in formatsList:
            formatsList.append(driverName)
    formatsList.sort()
    reply= input ("whether want to see driver list answer in yes/no")
    if reply =="yes":
        print "\n".join(formatsList)
    return (cnt,formatsList)


def entered_driver_availiblity(count,list):
    numberOfDriver=count
    driverList = list
    x = input("Enter driver name:")
    if x in driverList:
        print("ok")
        return x
    else:
        print("Value Error:%s is not in list" %x)

def dataSourceCreation():
    count, list = number_of_available_drivers()
    driverName = entered_driver_availiblity(count, list)
    driver = osgeo.ogr.GetDriverByName("%s" % driverName)
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    return dstFile

def reprojectLayer():

    transform=Transform()
    # get the input layer
    inDataSet = open_File()
    inLayer = inDataSet.GetLayer()

    # create the output layer
    outDataSet = dataSourceCreation()
    outLayer = outDataSet.CreateLayer("layer")

    # add fields
    inLayerDefn = inLayer.GetLayerDefn()
    for i in range(0, inLayerDefn.GetFieldCount()):
        fieldDefn = inLayerDefn.GetFieldDefn(i)
        outLayer.CreateField(fieldDefn)

    # get the output layer's feature definition
    outLayerDefn = outLayer.GetLayerDefn()

    # loop through the input features
    inFeature = inLayer.GetNextFeature()
    while inFeature:
        # get the input geometry
        geom = inFeature.GetGeometryRef()
        # reproject the geometry
        geom.Transform(transform)
        # create a new feature
        outFeature = ogr.Feature(outLayerDefn)
        # set the geometry and attribute
        outFeature.SetGeometry(geom)
        for i in range(0, outLayerDefn.GetFieldCount()):
            outFeature.SetField(outLayerDefn.GetFieldDefn(i).GetNameRef(), inFeature.GetField(i))
        # add the feature to the shapefile
        outLayer.CreateFeature(outFeature)
        # dereference the features and get the next input feature
        outFeature = None
        inFeature = inLayer.GetNextFeature()

    # Save and close the shapefiles
    inDataSet = None
    outDataSet = None

reprojectLayer()

def main():
    sourceFile = open_File()
    numberOfLayer=num_of_layers_in_file(sourceFile)














