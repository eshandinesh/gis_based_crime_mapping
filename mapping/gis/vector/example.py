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

from osgeo import ogr



def creating_directory():
    folderName = input("Enter Folder Name")
    folderPath = input("Where you want to save folder ")
    path = folderPath + '\\' + folderName
    print (path)
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)

def shp(l):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print ("Creating Directory For ShapeFile ")
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    fieldDef = osgeo.ogr.FieldDefn("P", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    point = ogr.Geometry(ogr.wkbPoint)
    a=l[1].mpoly[0][0]
    b=l[1].mpoly[0][1]
    point.AddPoint(float(a),float(b))
    feature.SetGeometry(point)
    feature.SetField("P", 1)
    dstLayer.CreateFeature(feature)
    feature.Destroy()

