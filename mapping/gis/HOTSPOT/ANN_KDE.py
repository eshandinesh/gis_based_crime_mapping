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
from ..predict.surface_predict import *



def ewlatlo(lat1,lon1,d,bearing):
    R = 6371                     #Radius of the Earth
    brng = math.radians(bearing) #convert degrees to radians
    #d = d*1.852                  #convert nautical miles to km
    lat1 = math.radians(lat1)    #Current lat point converted to radians
    lon1 = math.radians(lon1)    #Current long point converted to radians
    lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1),math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2,lon2



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


def data(lat,lon):
    llat = []
    llon = []
    llat = 0.00
    llon = 0.00
    count = 0.00
    j = 0
    for a in zip(lat,lon):
        llat += a[0]
        llon += a[1]
        j = j + 1
    north= max(lat)
    south = min(lat)
    east = max(lon)
    west= min(lon)
    mlat = llat / j
    mlon = llon / j
    return mlat,mlon,north,south,east,west

def create_a_polygon_gt(ge,score):
    #Create ring
    tryAgain = "yes"
    poly_li=[]
    score_list=[]
    for i in range(len(ge)):
        poly = ogr.Geometry(ogr.wkbPolygon)
        ring = ogr.Geometry(ogr.wkbLinearRing)
        for j in ge[i]:
            ring.AddPoint(j[0],j[1])
        score_list.append(score[i])
        poly.AddGeometry(ring)
        poly_li.append(poly)
    return poly_li,score_list


def pathlist(lat,lon):
    pathdistion = OrderedDict()
    centroid = OrderedDict()
    countdiction = OrderedDict()
    colordic = OrderedDict()
    colordic[10] = '#F6FFE5'
    colordic[30] = '#E7FFBA'
    colordic[50] = '#BFEAA3'
    colordic[70] = '#DFFFA5'
    colordic[100] = '#B6EA7D'
    colordic[130] = '#8ED95B'
    colordic[150] = '#FF3030'
    colordic[200] = '#FF0000'
    colordic[250] = '#CD0000'
    colordic[300] = '#8B0000'
    colordic[350] = '#800000'
    colordic[400] = '#660000'
    colordic[500] = '#330000'

    mlat,mlon,north, south, east, west = data(lat,lon)
    horzontal = haversine(north, west, north, east)
    vertical = haversine(north, east, south, east)
    x = horzontal / 20
    y = vertical / 20
    od = OrderedDict()
    logitu = OrderedDict()
    lagtitu = OrderedDict()
    count = OrderedDict()
    path, cout, color, asp,sqcout = [], [], [], [],[]
    for key, value in colordic.items():
        for i in range(key):
            asp.append(key)
    lat1 = north
    lon1 = west
    logitu[0] = lon1
    lagtitu[0] = lat1
    for i in range(20):
        lat2, lon2 = ewlatlo(lat1, lon1, x, bearing=90)
        logitu[i + 1] = lon2
        lon1 = lon2
    lat1 = north
    lon1 = west
    for j in range(20):
        lat2, lon2 = ewlatlo(lat1, lon1, y, bearing=180)
        lagtitu[j + 1] = lat2
        lat1 = lat2
    for row in range(20):
        for col in range(20):
            od[(row, col)] = [[lagtitu[row], logitu[col]], [lagtitu[row], logitu[col + 1]],
                              [lagtitu[row + 1], logitu[col + 1]], [lagtitu[row + 1], logitu[col]]]
            centroid[(row, col)]=[statistics.mean([lagtitu[row],lagtitu[row + 1]]),statistics.mean([logitu[col],logitu[col + 1]])]
            j = 0
            for a in zip(lat,lon):
                if a[0] <= lagtitu[row] and a[0] >= lagtitu[row + 1] and a[1] >= logitu[col] and a[1] <= logitu[col + 1]:
                    j += 1
            countdiction[(row, col)]=j
            pathdistion[(row, col)]=[(row-1,col-1),(row-1,col),(row-1,col+1),(row,col-1),(row,col),(row,col+1),(row+1,col-1),(row+1,col),(row+1,col+1)]
            if j != 0:
                cout.append(j)
                sqcout.append(j**2)
                for l in asp:
                    if j <= l:
                        y = l
                color.append(colordic[y])
                path.append([[lagtitu[row], logitu[col]], [lagtitu[row], logitu[col + 1]],
                             [lagtitu[row + 1], logitu[col + 1]], [lagtitu[row + 1], logitu[col]]])
            count[(row, col)] = j
            #print(path)
    return mlat,mlon,path,north, south, east, west,cout,od,centroid,countdiction,pathdistion,sqcout



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


def colo(v):
    li=[]
    q = sorted(v, reverse=True)
    a = list(set(q))
    def chunkIt(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    out = chunkIt(sorted(a, reverse=True), 10)
    for t in out:
        li.append(min(t))
    return li

def shp(ring,name,folderLocation,score):
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
    fieldDef = osgeo.ogr.FieldDefn("Score", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    dstLayer.CreateField(fieldDef)
    for u in range(len(ring)):
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(ring[u])
        feature.SetField("FieldID", 1)
        feature.SetField("Score", score[u])
        dstLayer.CreateFeature(feature)


def KDE():
    ite = 0
    k,v,v_f,norm_score,poly_li_finale=[],[],[],[],[]
    score_kde,u={},0
    result,frequency,lat,lon=ope_file(path="C:/Users\AMITY UNIVERSITY\Desktop\QWER\TEST_DATA")
    mlat,mlon,path,north, south, east, west,cout,od,centroid,countdiction,pathdistion,sqcout = pathlist(lat,lon)
    for key,value in centroid.items():
        poly_li_finale.append(od[key])
        score=predictio(value)
        print(key, value,score, "key", "value","score")
        score_kde[key]=score[0][0]
        k.append(key)
        v.append(score[0][0])
    li = colo(v)
    print(li, v, len(v))
    for i in v:
        if i >= li[0]:
            v_f.append(0)
        elif li[0] > i >= li[1]:
            v_f.append(1)
        elif li[1] > i >= li[2]:
            v_f.append(2)
        elif li[2] > i >= li[3]:
            v_f.append(3)
        elif li[3] > i >= li[4]:
            v_f.append(4)
        elif li[4] > i >= li[5]:
            v_f.append(5)
        elif li[5] > i >= li[6]:
            v_f.append(6)
        elif li[6] > i >= li[7]:
            v_f.append(7)
        elif li[7] > i >= li[8]:
            v_f.append(8)
        elif li[8] > i >= li[9]:
            v_f.append(9)
    poly_good,score_list=create_a_polygon_gt(poly_li_finale,v_f)
    print(score_list,poly_good)
    shp(poly_good, "result%s" % ite, "C:/Users\AMITY UNIVERSITY\Desktop\KERAS_name", score_list)
    '''
    average=scipy.mean(norm_score)
    xcd=sorted(norm_score)
    for uyt in norm_score:

    plt.scatter(w, y_data, label='Data')
    plt.plot(w, y_test_data, label='Fitted function')
    plt.legend(loc='best')
    plt.show()

    li =colo(v)
    print(li, v, len(v))
    for i in v:
        if i >= li[0]:
            v_f.append(0)
        elif li[0] > i >= li[1]:
            v_f.append(1)
        elif li[1] > i >= li[2]:
            v_f.append(2)
        elif li[2] > i >= li[3]:
            v_f.append(3)
        elif li[3] > i >= li[4]:
            v_f.append(4)
        elif li[4] > i >= li[5]:
            v_f.append(5)
        elif li[5] > i >= li[6]:
            v_f.append(6)
        elif li[6] > i >= li[7]:
            v_f.append(7)
        elif li[7] > i >= li[8]:
            v_f.append(8)
        elif li[8] > i >= li[9]:
            v_f.append(9)
    print(score_kde,k,v,li)
    return mlat,mlon,path, north, south, east, west, cout, od, centroid, countdiction, pathdistion, sqcout,v,li,v_f

'''