#coding:UTF-8
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
import operator

from math import radians, cos, sin, asin, sqrt, atan2, degrees
import glob



def creating_directoryj(name,path):
    folderName = ("%s"%name)
    folderPath = ("%s"%path)
    path = folderPath + '\\' + folderName
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)




def routej(li,path,name):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directoryj(name,path)
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)

    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    line=ogr.CreateGeometryFromWkt(li)
    feature.SetGeometry(line)
    dstLayer.CreateFeature(feature)
    feature.Destroy()
    dstFile.Destroy()



def wwkt(pointA, pointB):
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(pointA, pointB)
    return point.ExportToWkt()
'''li=wwkt(77.20751667535421,28.596286275178663)
routej(li,"C:/Users\Hp\Desktop\DATA","POLICELOCATION1")'''