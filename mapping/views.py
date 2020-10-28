# -*- coding: utf-8 -*-
from sklearn.neighbors.kde import KernelDensity
from django.shortcuts import render
from osgeo import ogr
import json,xlsxwriter
import xlrd,math,scipy
#from .models import abcd,CrimeData
from collections import OrderedDict,Counter
from scipy import stats
from scipy.stats import norm
from scipy.spatial import ConvexHull
import numpy as np
import matplotlib.pyplot as plt
import statistics,glob,os,osgeo,shutil
#from .gis.HOTSPOT.KDE import *
#from .gis.HOTSPOT.NNH import *
#from .gis.HOTSPOT.GETIS_ORD import *
#from .gis.HOTSPOT.RATIONAL_STAC import *
from .gis.HOTSPOT.ANN_KDE import *
#from .gis.HOTSPOT.taert import *


def open_File_1(path):
    if path==None:
        filePath = str(input("file path"))
    else:
        filePath=path
    print ("Entered File Path is %s" % filePath)
    datasource = ogr.Open(filePath,True)
    return datasource

def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    print ("the number of Layers in the file on the entered file path is %d" % numLayers)
    return numLayers


def num_of_features_in_layer(source, Layers):
    datasource = source
    numLayers = Layers
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = layer.GetFeatureCount()
        print ("Layer (%s) has %d features:" % (layerIndex, numFeatures))
        return numFeatures


def get_geometry(path):
    datasource = open_File_1(path)
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            print (feature)
            geometry = feature.GetGeometryRef()
            name = geometry.GetGeometryName()
        return datasource,layer


def home (request):
    print("hello")
    return render(request,'simpy.html')

def open_File(path):
    if path is None:
        filePath = str(input("file path"))
    else:
        filePath = path
    datasource = ogr.Open(filePath, 0)
    return datasource

'''def dataloader(request):
    ki={}
    l ,j= [],[]
    data = open_File("F:/desktomat\DATA\COMBINEPOINT\COMBINEPOINT.shp")
    for layer in data:
        for feta in layer:
            for i in range(0, feta.GetGeometryRef().GetPointCount()):
                pt = feta.GetGeometryRef().GetPoint(i)
                l.append([pt[1], pt[0]])
    data = open_File("F:/desktomat\DATA\COMBINEPOINT\COMBINEPOINT.shp")
    for layer in data:
        for feta in layer:
            for i in range(0, feta.GetGeometryRef().GetPointCount()):
                pt = feta.GetGeometryRef().GetPoint(i)
                l.append([pt[1], pt[0]])
                abcd(lat=pt[1],lon=pt[0]).save()
    return render(request, 'simpy.html',{'pline':l})'''

'''def mean(request):
    ki={}
    maxlat=[]
    maxlon=[]
    lat = 0.00
    lon = 0.00
    count = 0.00
    j = 0
    fa = CrimeData.object.all()
    for a in fa:
        lat+=a.lat
        maxlat.append(a.lat)
        lon +=a.lon
        maxlon.append(a.lon)
        j = j + 1
    mlat=lat/j
    mlon =lon/j
    print(mlat,mlon,j)
    #open_file(path="C:/Users\Hp\Desktop\data/2016-01/2016-01-cleveland-street.xlsx")
    return render(request, 'simpy.html',{'pm':mlat,'pn':mlon,'north':max(maxlat),'south':min(maxlat),'east':max(maxlon),'west':min(maxlon)})
'''
def spliterer (l):
    list = l
    #list=latlon
    string = []

    var = ""
    var2 = ""
    count = 0
    for i in range(len(list)):
        if list[i] == "[" or list[i] == "]" or list[i] == "." or list[i] == "0" or list[i] == "1" or list[i] == "2" or list[i] == "3" or list[i] == "4" or \
                        list[
                            i] == "5" or list[i] == "6" or list[i] == "7" or list[i] == "8" or list[i] == "9" or list[i] == ",":
            var = var + list[i]
    string.append(var)

    #print(string)
    oordsString = string[0].split("[[[")
    #print(coordsString, len(coordsString))
    oordsString =  oordsString[1].split("]]]")
    #print(coordsString, len(coordsString))
    oordsString = oordsString[0].split("]],[[")
    #print (oordsString,len(oordsString))
    u=[]
    for k in oordsString:
        boordsString = k.split("],[")
        a=[]
        #print(boordsString)
        for y in boordsString:
            coordsString = y.split(",")
            coords=[]
            for k in range(len(coordsString)):
                coords.append(float(coordsString[k]))
            a.append(coords)
        u.append(a)
    return u

'''Crime ID
Month
Reported by
Falls within
Longitude
Latitude
Location
LSOA code
LSOA name
Crime type
Last outcome category
Context'''
'''def open_file_rtyui(path="C:/Users\Hp\Desktop/Data/2016-03-cleveland-street.xlsx"):
    CrimeData.object.all().delete()
    book = xlrd.open_workbook(path)
    for i in range(book.nsheets):
        sheet = book.sheet_by_index(i)
        for ro in range(sheet.nrows-1):
            ro+=1
            a1 = sheet.cell_value(rowx=ro, colx=1)
            a1at = sheet.cell_value(rowx=ro, colx=5)
            a1on = sheet.cell_value(rowx=ro, colx=4)
            afall = sheet.cell_value(rowx=ro, colx=3)
            acrime = sheet.cell_value(rowx=ro, colx=9)
            CrimeData(month=a1,lat=float(a1at),lon =float(a1on),Falls_within =afall,Crime_type=acrime ).save()


def SDD(request):
    ki = {}
    llat = []
    llon = []
    lat = 0.00
    lon = 0.00
    count = 0.00
    j = 0
    fa = CrimeData.object.all()
    for a in fa:
        lat += a.lat
        llat.append(a.lat)
        lon += a.lon
        llon.append(a.lon)
        j = j + 1
    mlat = lat / j
    mlon = lon / j
    sdd=0.000
    X=0.00
    Y=0.00
    Z=0.00
    L=0.000
    M=0.0000
    data=[]
    for i, k in zip(llat, llon):
        sdd+=math.pow(haversine( float(mlat), float(mlon),float(i),float(k)),2)
        X+=(i-mlat)
        Y+=(k-mlon)
        Z+=(i-mlat)*(k-mlon)
        L+=math.pow((i-mlat),2)
        M +=math.pow((k-mlon),2)
        data.append([i,k])
        #sdd+=(math.pow((mlat-i),2)+math.pow((mlon-j),2))
    result=sdd/(j-2)
    rotation=math.atan(((L-M)+math.pow((math.pow((L-M),2)+(4*math.pow(Z,2))),(1/2)))/(2*Z))
    sigx=0.000
    sigy=0.000
    for f, g in zip(llat, llon):
        sigx+=math.pow((((f - mlat)*math.cos(rotation))-((g-mlon)*math.sin(rotation))), 2)
        sigy += math.pow((((f - mlat) * math.cos(rotation)) - ((g - mlon) * math.sin(rotation))), 2)
    sigmax=2*math.sqrt(abs(2*sigx/(j-2)))
    sigmay=2*math.sqrt(abs(2*sigy/(j-2)))
    print(len(fa),"hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
    mode()

    return render(request, 'simpy.html',
                  {'pm': mlat, 'pn': mlon, 'north': max(llat), 'south': min(llat), 'east': max(llon),
                   'west': min(llon),'r':math.sqrt(abs(result)),'sx':sigmax,'sy':sigmay,'rotation':rotation*180/math.pi,'pline':data})


def data():
    llat = []
    llon = []
    lat = 0.00
    lon = 0.00
    count = 0.00
    j = 0
    fa = CrimeData.object.all()
    for a in fa:
        lat += a.lat
        llat.append(a.lat)
        lon += a.lon
        llon.append(a.lon)
        j = j + 1
    north= max(llat)
    south = min(llat)
    east = max(llon)
    west= min(llon)
    mlat = lat / j
    mlon = lon / j
    return llat,llon,north,south,east,west,mlat,mlon


'''

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

def area(maxlat,minlat,minlon,maxlon):
    l= haversine(maxlat, minlon,maxlat,maxlon)
    w= haversine(maxlat, maxlon,minlat,maxlon)
    return (l*w)


#Thus, t he in dex com pa r es the aver age dis t ance from the closest neighbor t o each
#point with a dist ance that would be expect ed on the bas is of chance. If the observed
#avera ge dista nce is about the same as the mean random dist ance, th en the rat io will be
#about 1.0. On the other hand, if the obser ved aver age dista nce is sm aller than the mean
#r andom dis t ance, t ha t is , poin t s ar e actua lly closer together than would be expect ed on the
#ba sis of chance, t hen the nea r est neighbor in dex will be less than 1.0. This is evidence for
#clustering. Conversely, if th e observed average dista nce is great er th an th e mean random
#dis t ance, t hen the in dex will be gr ea t er than 1.0. This would be evidence for disper sion ,
#that point s a re more widely disper sed t han would be expect ed on the bas is of chance.
'''def NND():
    llat = []
    llon = []
    lat = 0.00
    lon = 0.00
    count = 0.00
    j = 0
    fa = CrimeData.object.all()
    for a in fa:
        lat += a.lat
        llat.append(a.lat)
        lon += a.lon
        llon.append(a.lon)
        j = j + 1
    print("llat is preperaded")
    cc=[]
    kw=0'''
'''for o in fa:
        mi=[]
        for i, k in zip(llat, llon):
            mi.append(haversine(o.lat, o.lon, i, k))
        cc.append(min(mi))
        kw += 1
        print(kw)
    avg=0.00
    u=0.00
    for h in cc:
        avg+=h
        u+=1
    dra=avg/u'''
'''ar=area(max(llat), min(llat), min(llon), max(llon))
    r=0.5*math.sqrt(ar/j)
    #result=dra/r
    se=math.sqrt(abs(((4-math.pi)*ar)/(4*math.pi*math.pow(j,2))))
    #z_stat=(dra-r)/se
    #p_values_1_tail = scipy.stats.norm.sf(abs(z_stat))
    #p_values_2_tail = scipy.stats.norm.sf(abs(z_stat))
    return r,se,llat,llon
'''


'''
def mode(path):
    llat = []
    llon = []
    cc = []
    mi, rank = OrderedDict(), OrderedDict()
    ra,fa = 0,0
    lon = 0.00
    count = 0.00
    if path is not None:
        result, frequency, lat, lon = ope_file(path)
        for a in zip(lat,lon):
            llat.append(a[0]-54+78)
            llon.append(a[1]+1+26)
        for iu, ku in zip(llat, llon):
            j = 0
            for il, kl in zip(llat, llon):
                if iu==il and ku ==kl:
                    j+=1
            mi[j] = (iu, ku)
            cc.append(j)
    else:
        fa = CrimeData.object.all()
        for a in fa:
            llat.append(a.lat)
            llon.append(a.lon)
        for o in fa:
            j = 0
            for i, k in zip(llat, llon):
                if o.lat==i and o.lon ==k:
                    j+=1
            mi[j] = (o.lat,o.lon)
            cc.append(j)
    cc.sort(reverse=True)
    for r in cc:
        ra+=1
        rank[ra]=mi[r]
    return mi,rank

'''

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


'''
def test(request):
    fa = CrimeData.object.all()
    llat, llon, north, south, east, west, mlat, mlon = data()
    horzontal = haversine(north, west, north, east)
    vertical = haversine(north, east, south, east)
    x = horzontal / 20
    y = vertical / 20
    print(x,y,north, south, east, west,"shashhahshsha")
'''






""" for i in range(20):
        h+=math.pow(-1,i+1)
        for j in range(20):
            #[[north-(i*y),west+(j*x)],[north-(i*y),west+((j+1)*x)],[ north - ((i+1)*y),west+((j+1)*x)],[ north - ((i+1)*y),west+(i*x)]]
            lat2,lon2=ewlatlo(lat1,lon1,x,agl=((2*h)+1))
            if lat1==lat2:
                print("latitude is same goig good")
            od[(j)] = [lat1, lat2, lon1, lon2]
            lon1=lon2
        if lon1==east:
            print("reached east")
        lat2, lon2 = ewlatlo(lat1, lon1, y,agl=2)
        lat1 = lat2
        lon1=lon2
        if lon1==east:
            print("logitude is same goig good")
        for key,value in od.items():
            j=0
            for a in fa:
                if a.lat>=value[1] and a.lat<=value[0] and a.lon>=value[2] and a.lon<=value[3]:
                    j+=1
            count[key]=j
            path.append([[north-(i*y),west+(j*x)],[north-(i*y),west+((j+1)*x)],[ north - ((i+1)*y),west+((j+1)*x)],[ north - ((i+1)*y),west+(i*x)]])
    print(path)"""


#Nnh routine uses a method that defines a threshold distance and  compares the threshold to the distances for all pairs of points
#Only points that are closer to one or more other points than the threshold distance are selected for clustering
#In addition, the user can specify a minimum number of points to be included in a cluster. Only points that fit both criteria - closer than the threshold and belonging to a group having the minimum number of points, are clustered at the first level (first-order clusters)

def cluster(llat,llon,Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance):
    f_cluster=[]
    for a in zip(llat,llon):
        cluster,midcl=[],[]
        for h in zip(llat,llon):
            dist=haversine(a[0],a[1],h[0],h[1])
            if dist <=Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance:
                cluster.append(list(h))
                print(cluster)
        if len(cluster)>5:
                f_cluster.append(cluster)
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






'''
def pathlist():
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
    fa = CrimeData.object.all()
    llat, llon, north, south, east, west, mlat, mlon = data()
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
            for a in fa:
                if a.lat <= lagtitu[row] and a.lat >= lagtitu[row + 1] and a.lon >= logitu[col] and a.lon <= logitu[col + 1]:
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
    return path,north, south, east, west, mlat, mlon,cout,od,centroid,countdiction,pathdistion,sqcout,llat,llon
'''
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


def creating_directory_rt(folderName, i):
    path = folderName + '\\' + i
    # print (path)
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
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


def uffe(lat,lon,d):
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(lat,lon)
    poly = point.Buffer(d)
    return poly



def ormalize(dist,sq_dist):
    t_value_99 = {1:318.310,2:22.326,3:10.213,4:7.173,5:5.893,6:5.208,7:4.785,8:4.501,9:4.297,10:4.144,11:4.025,12:3.930,13:3.852,14:3.787,15:3.733,
                  16:3.686,17:3.646,18:3.610,19:3.579,20:3.552,21:3.527,22:3.505,23:3.485,24:3.467,25:3.450,26:3.435,27:3.421,28:3.408,29:3.396,
                  30:3.3854}
    orma=[]
    lamda =0
    mea = scipy.mean(dist)
    mea_sq = scipy.mean(sq_dist)
    se = math.pow((mea_sq - math.pow(mea, 2)), 0.5)
    for i in dist:
        orma.append((i-mea)/se)
    if len(dist)<=30:
        lamda= mea + (t_value_99[len(dist)]*se)
    else:
        lamda= mea + (3.2*se)
    return lamda


def he_calci(geomgt,ar,la,lo):
    dist,X,Y,DX,DY,D2X,D2Y,sq_dist,uy,cum_freq,dis_Dslope = [],[],[],[],[],[],[],[],OrderedDict(),0,[]
    for h in geomgt:
        if la!=h[0] and lo!=h[1]:
            dist.append(haversine(la,lo,h[0],h[1]))
            sq_dist.append(math.pow(haversine(la,lo,h[0],h[1]),2))
    lamda=0
    hj=Counter(dist)#returs {element: frequency}
    mea =scipy.mean(dist)
    for l in range(len(set(dist))):
        cum_freq+=hj[sorted(list(set(dist)))[l]]
        uy[cum_freq/len(geomgt)]=sorted(list(set(dist)))[l]
        X.append(cum_freq/len(geomgt))
        Y.append(sorted(list(set(dist)))[l])
    '''plt.plot(np.array(Y),np.array(X))
    plt.title(ar)
    plt.show()'''
    for j in range(len(X)):
        if j<(len(X)-1):
            DY.append((math.atan((X[j+1]-X[j])/(Y[j+1]-Y[j])))*180/math.pi)
            DX.append(Y[j+1])
    hj_2 = Counter(DY)
    hj_2_freq=hj_2[max(DY)]
    dis_slope=[]
    for u in range(len(DY)):
        if DY[u]==max(DY):
            dis_slope.append(DX[u])
    #print( hj_2_freq,max(DY), dis_slope)
    '''plt.plot(np.array(DX),np.array(DY))
    plt.title(ar)
    plt.show()'''

    for j in range(len(DX)):
        if j<(len(DX)-1):
            D2Y.append((math.atan((DY[j+1]-DY[j])/(DX[j+1]-DX[j])))*180/math.pi)
            D2X.append(DX[j+1])

    if len(D2Y)!=0:
        hj_3 = Counter(D2Y)
        hj_3_freq = hj_3[max(D2Y)]
        for u in range(len(D2Y)):
            if D2Y[u] == max(D2Y):
                dis_Dslope.append(D2X[u])
        lamda = min(dis_Dslope)
    elif len(DY)!=0:
        lamda = min(dis_slope)
    else:
        lamda = max(dist)


    #print(hj_3_freq, max(D2Y), min(dis_Dslope))
    '''plt.plot(np.array(D2X),np.array(D2Y))
    plt.title(ar)
    plt.show()'''
    z_values = OrderedDict({90: 1.282, 95: 1.645, 97.5: 1.960, 99: 2.326, 99.5: 2.576, 99.9: 3.090, 99.99: 3.719})
    z = z_values[95]
    r = 0.5 * math.sqrt(ar / len(geomgt))
    se = math.sqrt(abs(((4 - math.pi) * ar) / (4 * math.pi * math.pow(len(geomgt), 2))))
    lamda_2 = r + (z * se)
    return lamda


def covex_hull(poi):
    poi.append(poi[0])
    convex_hull=[]
    points = np.array(poi)
    hull = ConvexHull(points)
    for t in hull.vertices:
        convex_hull.append(list(points[t]))
    poly =create_a_polygon(convex_hull)
    return convex_hull,poly


def tot_area():
    poi=[]
    result, frequency, llat, llon = ope_file(path="C:/Users\Hp\Desktop\Data")
    for i in zip(llat,llon):
        poi.append([i[0],i[1]])
    convex_hull,poly=covex_hull(poi)
    print(poly.GetArea())






'''def New_app (request):
    #path, north, south, east, west, mlat, mlon, cout, od, centroid, countdiction, pathdistion, sqcout,llat,llon= pathlist()
    re_score,poly_fial,re_scor_slope,poly_geom_fial,cluster=[],[],[],OrderedDict(),[]
    result,frequency,llat, llon=ope_file(path="C:/Users\Hp\Desktop\Data")
    fi_score = OrderedDict()
    we,ew=llat, llon
    ite=0
    for i in zip(list(set(we)),list(set(ew))):
        print(i[0],i[1])
        geomety,score,derivate,ANN=OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict()
        t_cout, d = 0, 0
        ri = cr_shp(llat, llon)
        scor_li,geomgt=[],[]
        while t_cout<(0.6*len(llat)):
            la,lo = [],[]
            d+=0.01000
            poly = uffe(i[0],i[1],d)
            #shp([poly])
            for ji in (ri):
                intersection = poly.Intersection(ji)
                if intersection.GetPointCount()!=0:
                    ri.remove(ji)
                    #print(intersection,"domeeeeeeeeeee")
                    geomgt.append([intersection.GetPoint()[0],intersection.GetPoint()[1]])
            for jp in geomgt:
                la.append(jp[0])
                lo.append(jp[1])
            t_cout=len(geomgt)
            if len(set(la))>2:
                ite += 1
                convex_hull,poly = covex_hull(geomgt)
                lamda = he_calci(geomgt,poly.GetArea(),i[0],i[1])
                geomety[poly.GetArea()] = [poly, geomgt, t_cout / (lamda * poly.GetArea()),poly.GetArea(),d,t_cout]
                ANN[i[0],i[1],d]=[t_cout, t_cout / (lamda * poly.GetArea()),poly.GetArea(),d]
                file2 = open(r"C:/Users\Hp\Desktop\Folder\FILE\File%s.txt"%ite, "a")
                file2.write(str([i[0],i[1],d,t_cout,poly.GetArea()]))
                file3 = open(r"C:/Users\Hp\Desktop\Folder\FILE\Score%s.txt"%ite, "a")
                file3.write(str([t_cout/poly.GetArea()]))
                file2.close()
                file3.close()
                score[t_cout/(lamda*poly.GetArea())]=poly.GetArea()
                scor_li.append([t_cout/(lamda*poly.GetArea()),poly.GetArea()])
                #point = ogr.Geometry(ogr.wkbPoint)
                #point.AddPoint(i[0], i[1])
                #shp([point], ite * 100000000)
                shp([poly], ite,"C:/Users\Hp\Desktop\Folder")
                print(poly.GetArea(), t_cout, len(llat),len(ri),t_cout/(lamda*poly.GetArea()),lamda,len(geomgt), "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
            else:pass
        fd=[]
        for kt,at in score.items():
            fd.append(kt)
        shp([geomety[score[max(fd)]][0]],"result%s"%ite,"C:/Users\Hp\Desktop\Folder\Result")
        #re_score.append()
        poly_fial.append(score[max(fd)])
        poly_geom_fial[score[max(fd)]]=[geomety[score[max(fd)]][0],geomety[score[max(fd)]][4]]



        for j in range(len(scor_li)):
            if (j)<len(scor_li)-1:
                derivate[(math.atan((scor_li[j+1][0]- scor_li[j][0])/((scor_li[j+1][1]+0.00000000001)- scor_li[j][1])))*180/math.pi]=scor_li[j+1][1]
        for m,j in derivate.items():
            fd.append(m)
        fi_score[i[0],i[1]]=geomety[derivate[max(fd)]]
        print(len(fi_score))
    for jas in range(len(re_score)):
        if (jas) < len(re_score) - 1:
             re_scor_slope.append(math.atan((re_score[jas + 1] - re_score[jas]) / ((poly_fial[jas + 1] + 0.00000000001) - poly_fial[jas]))*(180/math.pi))

    ouyt=0
    poly_fial.sort(reverse=True)
    for iwer in poly_fial:
        ite += 1
        shp([poly_geom_fial[iwer][0]], "cluster%s" % ite, "C:/Users\Hp\Desktop\Folder\FRESULT")

    #print(fi_score)
    return render(request, 'himpy.html',
                  {'pm': mlat, 'pn': mlon, 'north': north, 'south': south, 'east': east, 'west': west, 'path': path,
                   'cout': cout})
'''

'''def Getis_ord_star(request):
    path,north, south, east, west, mlat, mlon,cout,od,centroid,countdiction,pathdistion,sqcout,llat,llon = pathlist()
    Gi_star=OrderedDict()
    X_BAR=statistics.mean(cout)
    W_X_X_BAR=X_BAR*9
    S=((statistics.mean(sqcout)-(X_BAR**2))**0.5)
    form=((9*len(sqcout)-81)/(len(sqcout)-1))**0.5
    for key,value in pathdistion.items():
        X_i = 0
        print(key)
        for i in value:
            row,col=i[0],i[1]
            if row>=0 and row<=19 and col>=0 and col<=19:
                X_i+=countdiction[(row, col)]
                Gi_star[key]=((X_i-W_X_X_BAR)/(S*form))
        print(X_i,X_BAR,W_X_X_BAR,S,form,((X_i-W_X_X_BAR)/(S*form)))
    return render(request, 'himpy.html',{'pm': mlat, 'pn': mlon, 'north': north, 'south': south, 'east': east,'west': west,'path':path,'cout':cout})
'''
def ope_file(path):
    lat, lon, result, frequency = [], [], [], []
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


'''def KDE(request):
    k,v=[],[]
    score_kde={}
    cou=0
    result,frequency,lat,lon=ope_file(path="C:/Users\Hp\Desktop/c_data")
    path,north, south, east, west, mlat, mlon,cout,od,centroid,countdiction,pathdistion,sqcout,llat,llon = pathlist()
    for key,value in centroid.items():
        print(key)
        for i in zip(result, frequency):
            X = np.array([i[0]])
            kde = KernelDensity(kernel='gaussian', bandwidth=0.3).fit(X)
            cou+=kde.score_samples(centroid[key])*i[1]
        score_kde[key]=cou
        k.append(key)
        v.append(cou)
    li =colo(v)
    print(score_kde,k,v,li)
    return render(request, 'KDE.html',
                  {'pm': mlat, 'pn': mlon, 'north': north, 'south': south, 'east': east, 'west': west, 'path': path,
                   'color': li,'value':v})'''


'''def nnh(request):
    convex_hull_f = []
    g=0
    w = OrderedDict()
    f_cluster_i=0
    z_values=OrderedDict({90:1.282,95:1.645,97.5:1.960,99:2.326,99.5:2.576,99.9:3.090,99.99:3.719})
    z=z_values[95]
    result, standard_error, llat,llon=NND()
    Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance=result+(z*standard_error)
    f_cluster=cluster(llat, llon, Upper_Value_of_Confidence_Interval_for_Mean_Random_Distance)
    print("CLUSTERIG IS DOE")
    for acd in f_cluster:
        convex_hull, poi = [], []
        for q in acd:
            if q not in poi:
                poi.append([q[0], q[1]])
        if len(poi) > 2:
            points = np.array(poi)
            hull = ConvexHull(points)
            for t in hull.vertices:
                convex_hull.append(list(points[t]))
        print(convex_hull)
        if len(convex_hull) > 1:
            convex_hull_f.append(convex_hull)
    print("over")
    return render(request, 'dimpy.html',
                  {'pm': scipy.mean(llat), 'pn': scipy.mean(llon), 'north': max(llat), 'south': min(llat),
                   'east': max(llon),
                   'west': min(llon), 'hull': convex_hull_f, 'cluster': f_cluster})'''







def testist(request):
    i= [54.687296, - 1.186874]
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(i[0], i[1])
    #shp([point], "name")
    result, frequency, llat, llon = ope_file(path="C:/Users\Hp\Desktop\Data")
    ite = 0
    geomety, score, derivate = OrderedDict(), OrderedDict(), OrderedDict()
    t_cout, d = 0, 0
    ri = cr_shp(llat, llon)
    scor_li, geomgt = [], []
    while t_cout < len(llat):
        la, lo = [], []
        d += 0.01000
        poly = uffe(i[0], i[1], d)
        # shp([poly])
        for ji in (ri):
            intersection = poly.Intersection(ji)
            if intersection.GetPointCount() != 0:
                ri.remove(ji)
                # print(intersection,"domeeeeeeeeeee")
                geomgt.append([intersection.GetPoint()[0], intersection.GetPoint()[1]])
        for jp in geomgt:
            la.append(jp[0])
            lo.append(jp[1])
        t_cout = len(geomgt)
        if len(set(la)) > 2:
            convex_hull, poly = covex_hull(geomgt)
            lamda = he_calci(geomgt, poly.GetArea(), i[0], i[1])
            geomety[poly.GetArea()] = [poly, geomgt, t_cout / (lamda * poly.GetArea()), poly.GetArea()]
            score[t_cout / (lamda * poly.GetArea())] = poly.GetArea()
            scor_li.append([t_cout / (lamda * poly.GetArea()), poly.GetArea()])
            ite += 1
            # point = ogr.Geometry(ogr.wkbPoint)
            # point.AddPoint(i[0], i[1])
            # shp([point], ite * 100000000)
            shp([poly], ite)
            print(poly.GetArea(), t_cout, len(llat), len(ri), t_cout / (lamda * poly.GetArea()), lamda, len(geomgt),
                  "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")


def HOTSPOTS (request):
    mlat,mlon,path, north, south, east, west, cout, od, centroid, countdiction, pathdistion, sqcout,v,li,v_f=KDE()
    #mlat, mlon, north, south, east, west, v, v_f=ultasidha()
    #lat, lon, f_cluster, convex_hull_f=nnh()
    #mlat,mlon,north,south,east,west,path,cout,v,li,v_f = Getis_ord_star()
    #New_app()
    '''lis=[]
    i=0
    mi,rank = mode("C:/Users\Hp\Desktop\TEST_DATA")
    for ke,val in rank.items():
        i+=1
        if i>10:
            break
        else:
            lis.append(list(rank[ke]))'''
    #return render(request, 'himpy.html',{'pm': mlat, 'pn': mlon,  'north': north, 'south': south, 'east': east, 'west': west, 'path': path,'cout': cout})
    #return render(request, 'dimpy.html',{'pm': scipy.mean(lat), 'pn': scipy.mean(lon), 'north': max(lat), 'south': min(lat),'east': max(lon),'west': min(lon), 'hull': convex_hull_f, 'cluster': f_cluster})
    return render(request, 'KDE.html',{'pm': mlat, 'pn': mlon, 'north': north, 'south': south, 'east': east, 'west': west, 'path': path,'cout': cout,'GI':v,'check':v_f})
