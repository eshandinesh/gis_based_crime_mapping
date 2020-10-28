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


'''def open_File(path):
    if path is None:
        filePath = str(input("file path"))
        print "Entered File Path is %s" % filePath
    else:
        filePath=path
    f = int(input("IF YOU LIKE TO READ FILE ENTER 0 AND IF YOU LIKE TO WRITE FILE ENTER 1"))
    datasource = ogr.Open(filePath,f)
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

def police():
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\POLICELOCATION\POLICELOCATION.shp")
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        print "feature number %d" % featureIndex
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.ExportToWkt(), geom.GetX(),geom.GetY(),layer

def crime():
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\CRIMELOCATION\CRIMELOCATION.shp")
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        print "feature number %d" % featureIndex
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.ExportToWkt(), geom.GetX(), geom.GetY(),layer

def check(wkt):
    featureforbuffer = ogr.CreateGeometryFromWkt(wkt)
    featurebuf = featureforbuffer.Buffer(0.01)
    featurebuffer = ogr.CreateGeometryFromWkt(featurebuf.ExportToWkt())
    print featurebuffer
    a,b,c,layer=crime()
    print b,c,layer
    print layer.SetSpatialFilter(featurebuffer)
    if feature in layer:
        return False
    else:
        return True

def buffer(a):
    geometry = ogr.CreateGeometryFromWkt(a)
    polygon = geometry.Buffer(0.01)
    return polygon


a=[]
g, c, d, policelayer = police()
print c,d
p, q, r, crimelayer = crime()
a.append(g)
route = {}
finalroute=[]
lengthend = {}
lengthstart={}
route_1 = {}
x=True
i=0
featureindex = 0
finalcord={}
while x:
    datasource = open_File(path="C:\Users\Hp\Desktop\ABSTRACT\SHASHANK\SHASHANK.shp")
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(buffer(a[i]))
    for feature in layer:
        featureindex += 1
        route[featureindex] = feature.GetGeometryRef().ExportToWkt()
        line1 = ogr.Geometry(ogr.wkbLineString)
        count1 = feature.GetGeometryRef().GetPointCount()
        line1.AddPoint(feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1])
        line1.AddPoint(q,r)
        end11=line1.Length()
        finalcord[end11]=feature.GetGeometryRef().GetPoint(0)
        line2 = ogr.Geometry(ogr.wkbLineString)
        line2.AddPoint(feature.GetGeometryRef().GetPoint(count1-1)[0], feature.GetGeometryRef().GetPoint(count1-1)[1])
        line2.AddPoint(q, r)
        end22 = line2.Length()
        finalcord[end22]=feature.GetGeometryRef().GetPoint(count1-1)
        lengthend[featureindex] = min(end11,end22)


        line3 = ogr.Geometry(ogr.wkbLineString)
        line3.AddPoint(feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1])
        line3.AddPoint(c,d)
        end13 = line3.Length()
        finalcord[end13] = feature.GetGeometryRef().GetPoint(0)
        line4 = ogr.Geometry(ogr.wkbLineString)
        line4.AddPoint(feature.GetGeometryRef().GetPoint(count1 - 1)[0], feature.GetGeometryRef().GetPoint(count1 - 1)[1])
        line4.AddPoint(c,d)
        end24 = line4.Length()
        finalcord[end24] = feature.GetGeometryRef().GetPoint(count1 - 1)
        lengthend[featureindex] = min(end13, end24)
    print route
    route_1[min(length.keys(), key=(lambda k: length[k]))] = length[min(length.keys(), key=(lambda k: length[k]))]
    print route_1
    final_route=ogr.CreateGeometryFromWkt(route[min(length.keys(), key=(lambda k: length[k]))])
    po= ogr.Geometry(ogr.wkbPoint)
    po.AddPoint(finalcord[length[min(length.keys(), key=(lambda k: length[k]))]][0],finalcord[length[min(length.keys(), key=(lambda k: length[k]))]][1])
    b=po.ExportToWkt()
    a.append(b)
    del layer
    route.clear()
    finalroute.append(final_route)
    length.clear()
    i+=1
    if i==3:
        break
spatialReference = osgeo.osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84")
count, list = number_of_available_drivers()
driverName = entered_driver_availiblity(count, list)
driver = osgeo.ogr.GetDriverByName("%s" % driverName)
folderLocation, folderName = creating_directory()
name = input("enter shape file name")
dstPath = os.path.join(folderLocation, "%s.shp" % name)
dstFile = driver.CreateDataSource("%s" % dstPath)
dstLayer = dstFile.CreateLayer("resulting layer")
out_row = ogr.Feature(dstLayer.GetLayerDefn())
multilinestring = ogr.Geometry(ogr.wkbMultiLineString)
for k in range(len(finalroute)):
    multilinestring.AddGeometry(finalroute[k])
poly={}
for i in range(len(finalroute)):
    poly[i]=multilinestring.GetGeometryRef(i)
line = {}
line[0]=poly[0]
for i in range(len(finalroute)-1):
    line[i + 1] = poly[i+1].Union(line[i])
out_row.SetGeometry(line[len(finalroute)-1])
dstLayer.CreateFeature(out_row)
dstFile.Destroy()

po= ogr.Geometry(ogr.wkbPoint)
po.AddPoint(78.21,26.23)
polygon = po.Buffer(0.005)
spatialReference = osgeo.osr.SpatialReference()
spatialReference.SetWellKnownGeogCS("WGS84")
count, list = number_of_available_drivers()
driverName = entered_driver_availiblity(count, list)
driver = osgeo.ogr.GetDriverByName("%s" % driverName)
folderLocation, folderName = creating_directory()
name = input("enter shape file name")
dstPath = os.path.join(folderLocation, "%s.shp" % name)
dstFile = driver.CreateDataSource("%s" % dstPath)
dstLayer = dstFile.CreateLayer("resulting layer")
out_row = ogr.Feature(dstLayer.GetLayerDefn())
out_row.SetGeometry(polygon)
dstLayer.CreateFeature(out_row)
dstFile.Destroy()'''




for i in range(31):
    print ("C:\Users\Hp\Desktop\pol\CRIMEDATA\crime%d.shp"%i)


