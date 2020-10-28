'''adfdfdfdfdf = input("enter code")
    if adfdfdfdfdf == 1:
        pass'''

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


def open_File(path):
    if path is None:
        filePath = str(input("file path"))
    else:
        filePath = path
    datasource = ogr.Open(filePath, 0)
    return datasource




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
    fieldDef = osgeo.ogr.FieldDefn("name", osgeo.ogr.OFTString)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    k=0
    for i in li:
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        line=ogr.CreateGeometryFromWkt(i)
        feature.SetGeometry(line)
        feature.SetField("name", str(k))
        dstLayer.CreateFeature(feature)
        feature.Destroy()
        k=k+1
    dstFile.Destroy()
li=[]
os.chdir("C:/Users\Hp\Desktop\PATH\MODEL\POINT")
file=glob.glob('*.shp')
for f in file:
    data=open_File(f)
    for layer in data:
    #ne=0
        for feta in layer:
            li.append(feta.GetGeometryRef().ExportToWkt())
routej(li, "C:/Users\Hp\Desktop\DATA", "COMBINEPOINT")
# routej(li, "C:/Users\Hp\Desktop\DATA", "TESTINDIA%s"%ne)
li.clear()




'''fi = ogr.Open("C:/Users\Hp\Desktop\DATA\COMBINE\COMBINE.shp", 1)
for la in fi:
    for feta in la:
        if feta.GetGeometryRef().GetPointCount() == 1:
            print(feta.GetGeometryRef().GetPointCount(), feta.GetField("name"),feta.GetFID())
            la.DeleteFeature(feta.GetFID())
            a = input("enter code")
            if a == 1:
                pass'''




'''
    if feta.GetGeometryRef().GetPointCount()==1:
       print(feta.GetGeometryRef().GetPointCount(), feta.GetField("name"))
        a = input("enter code")
        if a == 1:
            pass'''


'''ne=ne+1'''
'''print(feta.GetGeometryRef())
        a = input("enter code")
        if a == 1:
            pass
        if ne==10:
            break
        li.append(feta.GetGeometryRef().ExportToWkt())
    routej(li, "C:/Users\Hp\Desktop\DATA", "BHOPALLINES")
    #routej(li, "C:/Users\Hp\Desktop\DATA", "TESTINDIA%s"%ne)
    li.clear()'''




'''

print(feta.GetGeometryRef().GetPointCount(), feta.GetField("name"))'''


'''w=4
name="shashank"

print("%s%s.shp" % (name,w))'''

