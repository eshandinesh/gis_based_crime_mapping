# -*- coding: utf-8 -*-
from sklearn.neighbors.kde import KernelDensity
from django.shortcuts import render
from osgeo import ogr
import json,xlsxwriter
import xlrd,math,scipy
from collections import OrderedDict,Counter
from scipy import stats
from scipy.stats import norm
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import statistics,glob,os,osgeo,shutil

def area(maxlat,minlat,minlon,maxlon):
    l= haversine(maxlat, minlon,maxlat,maxlon)
    w= haversine(maxlat, maxlon,minlat,maxlon)
    return (l*w)

def NND(lat,lon):
    llat = 0.00
    llon = 0.00

    count = 0.00
    j = 0
    for a in zip(lat,lon):
        llat += a[0]
        llon += a[1]
        j = j + 1
    print("llat is preperaded")
    cc=[]
    kw=0
    ar=area(max(lat), min(lat), min(lon), max(lon))
    r=0.5*math.sqrt(ar/j)
    se=math.sqrt(abs(((4-math.pi)*ar)/(4*math.pi*math.pow(j,2))))
    return r,se


def haversine(lat1, lon1, lat2, lon2):#returns distance in kilometers

    # convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r #returns distance in kilometers

def uffe(lat,lon,d):
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(lat,lon)
    poly = point.Buffer(d)
    return poly


def cluster(llat,llon,Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance):
    f_cluster,ui=[],0
    for a in zip(llat,llon):
        ui+=1
        cluster_lat,cluster_lon=[],[]
        for h in zip(llat,llon):
            dist=haversine(a[0],a[1],h[0],h[1])
            if dist <=Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance:
                cluster_lat.append(h[0])
                cluster_lon.append(h[1])
        poly =uffe(a[0],a[1],Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance)
        shp([poly],ui,"C:/Users\Hp\Desktop\TEST")
        f_cluster.append([cluster_lat,cluster_lon])
    return f_cluster

def maxcluster(f_cluster,w):
    lat,lon,mealat,mealon=[],[],[],[]
    for ad in f_cluster:
        for q in ad:
            lat.append(q[0])
            lon.append(q[1])
        print(lat,lon)
        w[scipy.mean(lat), scipy.mean(lon)]=ad
    for key, value in w.items():
        mealat.append(key[0])
        mealon.append(key[1])
    return w,mealat,mealon


def ope_file(path):
    lat, lon, result, frequency,rferee = [], [], [], [],OrderedDict()
    for i in glob.glob(os.path.join(path, "*")):
        print(i)
        book = xlrd.open_workbook(i)
        for i in range(book.nsheets):
            sheet=book.sheet_by_index(i)
            for ro in range (sheet.nrows-1):
                ro+=1
                alat=sheet.cell_value(rowx=ro,colx=5)
                lat.append(alat)
                alon = sheet.cell_value(rowx=ro, colx=4)
                lon.append(alon)
                print(alat,alon)
    for a,b in zip(lat,lon):
        j=0
        for c,d in zip(lat,lon):
            if c==a and d==b:
                j+=1
        frequency.append(j)
        result.append([a,b])
        #rferee[[a,b]]=j
    #print(result,frequency,len(result))
    return result,frequency,lat,lon


def creating_directory():
    folderName = "TEST"#input("Enter Folder Name")
    #folderPath = input("Where you want to save folder ")
    path = "C:/Users\Hp\Desktop" + '\\' + "TEST"
    #print (path)
    '''if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)'''
    #os.mkdir("%s" % path)
    "C:/Users\Hp\Desktop\TEST"
    "C:/Users\Hp\Desktop\Folder"
    return (path, folderName)


def shp(ring,name,folderLocation):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    # count, list = number_of_available_drivers()
    # driverName = entered_driver_availiblity(count, list)
    # driver = osgeo.ogr.GetDriverByName("%s" % driverName)#ESRI Shapefile
    driver = ogr.GetDriverByName("ESRI Shapefile")
    print("Creating Directory For ShapeFile")
    #folderLocation, folderName = creating_directory()
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("layer", spatialReference)
    fieldDef = osgeo.ogr.FieldDefn("FieldID", osgeo.ogr.OFTInteger)
    fieldDef.SetWidth(10)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("Longitude", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("Latitude", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
    if len(ring)==1:
        feature.SetGeometry(ring[0])
        feature.SetField("FieldID", 1)
        feature.SetField("Longitude", 1)
        feature.SetField("Latitude", 1)
        dstLayer.CreateFeature(feature)
    else:
        for i in range(len(ring)):
            feature.SetGeometry(ring[i])
            feature.SetField("FieldID", 1)
            feature.SetField("Longitude", 1)
            feature.SetField("Latitude", 1)
            dstLayer.CreateFeature(feature)
    feature.Destroy()

def create_a_polygon(ge):
    #Create ring
    tryAgain = "yes"
    poly = ogr.Geometry(ogr.wkbPolygon)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    for i in ge:
        ring.AddPoint(i[0],i[1])
    poly.AddGeometry(ring)
    return poly

def cr_shp(llat,llon):
    ri=[]
    for l in zip(llat, llon):
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(float(l[0]), float(l[1]))
        ri.append(point)
    #shp(ri)
    return ri


def covex_hull(poi):
    poi.append(poi[0])
    convex_hull=[]
    points = np.array(poi)
    hull = ConvexHull(points)
    for t in hull.vertices:
        convex_hull.append(list(points[t]))
    poly =create_a_polygon(convex_hull)
    return convex_hull,poly


def nnh():
    result, frequency, lat, lon = ope_file(path="C:/Users\Hp\Desktop\TEST_DATA")
    #shp(cr_shp(lat, lon),"TEST","C:/Users\Hp\Desktop\TEST_DATA")
    if input():
        pass
    convex_hull_f = []
    g=0
    w = OrderedDict()
    f_cluster_i=0
    z_values=OrderedDict({90:1.282,95:1.645,97.5:1.960,99:2.326,99.5:2.576,99.9:3.090,99.99:3.719})
    z=z_values[95]
    result, standard_error=NND(lat,lon)
    Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance=result+(z*standard_error)
    f_cluster=cluster(lat, lon, Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance)
    if input():
        pass
    print("CLUSTERIG IS DOE")
    for acd in f_cluster:
        poi = []
        if len(list(set(acd[0])))>3:
            g += 1
            for t in zip(list(set(acd[0])),list(set(acd[1]))):
                poi.append([t[0],t[1]])
            convex_hull,poly=covex_hull(poi)
            if convex_hull not in convex_hull_f:
                shp([poly], g, "C:/Users\Hp\Desktop\TEST")
                convex_hull_f.append(convex_hull)
    print("over")
    return lat,lon,f_cluster,convex_hull_f