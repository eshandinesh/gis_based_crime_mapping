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
from django.contrib.gis.geos import geometry
from math import radians, cos, sin, asin, sqrt, atan2, degrees
import glob

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

def close(v,a):
    d={}
    l=[]
    for i in range(len(v)):
        roa = geometry.GEOSGeometry(v[i].mpoly)
        roa.wkt()
        pointA=(v[i].mpoly[0],v[i].mpoly[1])
        pointB=(a[len(a)-1].mpoly[0],a[len(a)-1].mpoly[1])
        dist=haversine(pointA,pointB)
        l.append(dist)
        d[dist]=pointA
    u=min(l)
    return d[u]


