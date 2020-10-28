import ogr
import glob
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
import xlrd
from osgeo import ogr
from vector.write import *
from math import radians, cos, sin, asin, sqrt, atan2, degrees,ceil

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
    print env
    return env

def main(env,gridHeight=0.005,gridWidth=0.005):
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
    print "Creating Directory For ShapeFile "
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    numField = input(
        "Enter the required number of fields\ attributes in a layer other than FieldID, Longitude, Latitude")
    fieldDef = osgeo.ogr.FieldDefn("FieldID", osgeo.ogr.OFTString)
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
            outFeature.SetField("FieldID", str((countcols,countrows)))
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
    return dictionary_1





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
        print finalroute[k].GetGeometryRef()
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
    print path
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)


def csvtoshp (filePath):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print "Creating Directory For ShapeFile "
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
    list = {"Integer": 1, "IntegerList": 2, "Real": 3, "RealList": 4, "String": 5, "StringList": 6, "WideString": 7,
            "WideStringList": 8, "Binary": 9, "Date": 10, "Time": 11, "DateTime": 12, "Integer64": 13,
            "Integer64List": 14}
    print list
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
        print w
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField("FieldID", j)
        feature.SetField("Longitude", point.GetX())
        feature.SetField("Latitude", point.GetY())
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
    print "Entered File Path is %s" % filePath
    datasource = ogr.Open(filePath)
    return datasource

def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    print "the number of Layers in the file on the entered file path is %d" % numLayers
    return numLayers


def creating_an_empty_shape_file(geom):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print "Creating Directory For ShapeFile "
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
    print "point geometry"
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
    print "Creating Directory For ShapeFile "
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    numField = input("Enter the required number of fields\ attributes in a layer other than FieldID, Longitude, Latitude")
    fieldDef = osgeo.ogr.FieldDefn("FieldID", osgeo.ogr.OFTString)
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
    print "point geometry"
    for i in range(len(q)):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(centroid[q[i]][0],centroid[q[i]][1])
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        feature.SetField("FieldID", str(q[i]))
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
                print "feature number %d" % featureIndex
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
            print "feature number %d" % featureIndex
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
            print "feature number %d" % featureIndex
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
    print "CRIMEPOINT"
    crimepointlist=point_list(crimefilepath)
    print "MEAN CRIME POINT"
    meanpointlist=point_list(meanfilepath)
    print "done"
    for i in range(len(crimepointlist)):
        pointA=crimepointlist[i]
        E=haversine(pointA,meanpointlist[0])
        print E
        d.append(E**2)
        print d
    for i in range(len(d)):
        total=total+d[i]
    print total
    avgsquareroot=sqrt(total)/len(d)
    print avgsquareroot
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(meanpointlist[0][0],meanpointlist[0][1])
    poly = point.Buffer(avgsquareroot/100)
    l.append(poly.ExportToWkt())
    creating_an_empty_shape_file(l)

def poly_in_fish():
    poly={}
    datasource = ogr.Open("C:\Users\Hp\Desktop\pol\HOTSPOTTEST\FISHNET\FISHNET.shp")
    for layer in datasource:
        for feature in layer:
            poly[feature.GetField("FieldID")] = feature
    return poly


def crimecount(dic,poly,path):
    centroid={}
    count={}
    a=0
    crimepointdatasource = open_File_1(path)
    crimepointlayer = crimepointdatasource.GetLayerByIndex(0)
    for key,value in dic.iteritems():
        centroid[key]=((dic[key][0]+dic[key][1])/2,(dic[key][2]+dic[key][3])/2)
    for key,value in poly.iteritems():
        crimepointlayer.SetSpatialFilter(poly[key].GetGeometryRef())
        count[key]=crimepointlayer.GetFeatureCount()
    return count

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
    for key,value in count.iteritems():
        a=a+count[key]
    mean=a/len(count)
    return mean

def std_getis_ord():
    a = 0
    b = 0
    i = 0
    datasource = ogr.Open("C:\Users\Hp\Desktop\pol\HOTSPOTTEST\ZSDFGHJ\SDFGHJ.shp")
    for layer in datasource:
        for feature in layer:
            a = a + feature.GetField("COUNT")
            b = b + (feature.GetField("COUNT")) ** 2
            i += 1
    c=sqrt((b/i)-(a/i)**2)
    return c,a/i

def count_dic():
    a={}
    datasource = ogr.Open("C:\Users\Hp\Desktop\pol\HOTSPOTTEST\ZSDFGHJ\SDFGHJ.shp")
    for layer in datasource:
        for feature in layer:
            a[feature.GetField("FieldID")]=feature.GetField("COUNT")
    return a

def abcd(w):
    a=0
    b=0
    for key, value in w.iteritems():
        a = a + w[key] ** 2
        b = b + w[key]
    d=sqrt((len(w)*a-b**2)/(len(w)-1))
    print d,b
    return d,b

def Getisord(count,mean,d,b,c,w):
    e=0
    q=[]
    for key, value in w.iteritems():
        q.append(key)
    for i in range(len(q)):
        e = e + (count[q[i]] * w[q[i]])
    f=mean*b
    g=(e-f)/(d*c)
    print g

def Gi_statistics():
    gi_star={}
    y=[]
    env = envelop(filepath="C:\Users\Hp\Desktop\pol\ONEFEATLIST\ONEFEATLIST.shp")
    dictionary_1= main(env, gridHeight=0.005, gridWidth=0.005)
    centroid=centroid_1(dictionary_1)
    poly=poly_in_fish()
    count=crimecount(dictionary_1, poly, path="C:\Users\Hp\Desktop\pol\LESSCRIMEFEAT\CRIMEFEAT.shp")
    creating_test_shape_file(centroid, count)
    '''dist=lag_distance(centroid)
    for key, value in centroid.iteritems():
        y.append(key)
    for i in range(len(y)):
        w=spatial_weight_matrix(centroid, dist, (y[i][0],y[i][1]))
        c,mean = std_getis_ord()
        d, b = abcd(w)
        g=Getisord(count, mean, d, b, c, w)
        gi_star[y[i]]=g
    print gi_star'''
#C:\Users\Hp\Desktop\pol\HOTSPOTTEST
import time
from time import mktime
a='AsDfSdFg'
b='aSdfSdfG'
if a.lower() == b.lower():
    print "yes"






