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
from ..predict.EW_STAC_TEST import*





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


def New_app (path="C:/Users\Hp\Desktop\DATA"):
    #path, north, south, east, west, mlat, mlon, cout, od, centroid, countdiction, pathdistion, sqcout,llat,llon= pathlist()
    re_score,poly_fial,re_scor_slope,poly_geom_fial,cluster,file_tuple,file_score,traui=[],[],[],OrderedDict(),[],[],[],OrderedDict()
    #for iot in glob.glob(os.path.join(path, "*")):

    result,frequency,llat, llon=ope_file(path="C:/Users\AMITY UNIVERSITY\Desktop\QWER\TEST_DATA")
    ri = cr_shp(llat, llon)
    # shp(ri,"DATA","C:/Users\Hp\Desktop\d2\yu")
    fi_score = OrderedDict()
    we,ew=llat, llon
    ite=0
    for i in zip(list(set(we)),list(set(ew))):
        print(i[0],i[1])
        geomety,score,derivate,ANN,var1,var2,var3=OrderedDict(),OrderedDict(),OrderedDict(),OrderedDict(),[],[],[]
        t_cout, d = 0, 0
        ri = cr_shp(llat, llon)
        #shp(ri,"DATA","C:/Users\Hp\Desktop\d2\yu")
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
                lam = he_calci(geomgt,poly.GetArea(),i[0],i[1])
                print(predictio(lam))
                lamda=predictio(lam)[0][0]
                geomety[poly.GetArea()] = [poly, geomgt, t_cout / (lamda * poly.GetArea()),poly.GetArea(),d,t_cout]
                ANN[i[0],i[1],d]=[t_cout, t_cout / (lamda * poly.GetArea()),poly.GetArea(),d]
                #file2 = open(r"C:/Users\Hp\Desktop\Folder\FILE\File.txt", "a")
                #file2.write(str([i[0],i[1],d,t_cout,poly.GetArea()])+",")
                #file3 = open(r"C:/Users\Hp\Desktop\Folder\FILE\Score.txt", "a")
                #file3.write(str([t_cout/poly.GetArea()])+",")
                #file2.close()
                #file3.close()
                #var1.append(d)
                #var2.append(t_cout / (lamda * poly.GetArea()))
                #var3.append(t_cout/poly.GetArea())
                score[t_cout/(lamda*poly.GetArea())]=poly.GetArea()
                scor_li.append([t_cout/(lamda*poly.GetArea()),poly.GetArea()])
                #point = ogr.Geometry(ogr.wkbPoint)
                #point.AddPoint(i[0], i[1])
                #shp([point], ite * 100000000)
                shp([poly], ite,"C:/Users\AMITY UNIVERSITY\Desktop\QWER\Folder")
                print(poly.GetArea(), t_cout, len(llat),len(ri),t_cout/(lamda*poly.GetArea()),lamda,len(geomgt), "ZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZZ")
            else:pass
        fd=[]
        #qwer,rewq=0,0
        #for c, e in enumerate(var2):
         #   if e == max(var2):
                #qwer=c
        #for c2, e2 in enumerate(var3):
            #print("gf4")
            #if e2 == max(var3):
                #rewq=c2

        #traui[i[0],i[1]]=[var1[qwer],var1[rewq]]
        for kt,at in score.items():
            fd.append(kt)
        shp([geomety[score[max(fd)]][0]],"result%s"%ite,"C:/Users\AMITY UNIVERSITY\Desktop\QWER\Folder\Result")
        #re_score.append()
        poly_fial.append(score[max(fd)])
        poly_geom_fial[score[max(fd)]]=[geomety[score[max(fd)]][0],geomety[score[max(fd)]][4]]
        '''for j in range(len(scor_li)):
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
    '''
    poly_fial.sort(reverse=True)
    for iwer in range(len(poly_fial)):
        if iwer<26:
            ite += 1
            shp([poly_geom_fial[poly_fial[iwer]][0]], "cluster%s" % ite, "C:/Users\AMITY UNIVERSITY\Desktop\QWER\Folder\FRESULT")

    #file4 = open(r"C:/Users\Hp\Desktop\Folder\FILE\D.txt", "a")
    #file4.write(str(traui))
    #file4.close()
    #print(fi_score)
