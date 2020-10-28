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

def open_File(path):
    if path is None:
        filePath = str(input("file path"))
    else:
        filePath=path
    datasource = ogr.Open(filePath,0)
    return datasource
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
def nearest_policia():
    path="C:/Users\Hp\Desktop\DATA\POLICELOCATION\POLICELOCATION.shp"
    crimepath="C:/Users\Hp\Desktop\DATA\CRIMELOCATION\CRIMELOCATION.shp"
    d={}
    patht={}
    l=[]
    crimedatasource = open_File(crimepath)
    clayer = crimedatasource.GetLayerByIndex(0)
    cfeat = clayer.GetFeature(0)
    datasource = open_File(path)
    layer = datasource.GetLayerByIndex(0)
    for feat in layer:
        pointA=(feat.GetGeometryRef().GetX(),feat.GetGeometryRef().GetY())
        pointB=(cfeat.GetGeometryRef().GetX(),cfeat.GetGeometryRef().GetY())
        length=haversine(pointA,pointB)
        patht[length]=feat.GetField("name")
        d[length]=feat
        l.append(length)
    print (patht[min(l)])
    return d[min(l)].GetGeometryRef().GetX(),d[min(l)].GetGeometryRef().GetY()