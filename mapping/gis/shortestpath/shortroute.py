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
from .close import close
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

def featurelength(a):
    w=[]
    l=0
    for i in range(len(a.mpoly)):
        w.append(a.mpoly[i])
    for i in range(len(w)-1):
        l=l+haversine(w[i],w[i+1])

    return l

def generating_line_feature(a,b):
    return haversine(a,b),b

'''def crimelink(r,a):
    p=[]
    #for i in range(len(r)):
    #print(i," yeh to i print hua hai@@@@@@@@@@@@@")
    line=geometry.GEOSGeometry(r[52].mpoly)
    buff = line.buffer(0.00010)
    for i in range(len(buff[0])):
        p.append([buff[0][i][1],buff[0][i][0]])
    return p
        #print(line, " yeh to line object print hui hai@@@@@@@@@@@@@",buff.intersects(a[len(a) - 1].mpoly),"yeh intersect kar rahi hai ya nahi yeh  print hui hai@@@@@@@@@@@@@")
        #if buff.intersects(a[len(a) - 1].mpoly):
            #return buff.intersects(a[len(a) - 1].mpoly),r[i].name'''


def crimelink(r,a):
    for i in range(len(r)):

        line=geometry.GEOSGeometry(r[i].mpoly)
        buff = line.buffer(0.00010)

        if buff.intersects(a[len(a) - 1].mpoly):
            return buff.intersects(a[len(a) - 1].mpoly),r[i]


def remove_dead_ends(crime_road_feature,r,c):
    l1=[]
    removed_nasme=[]
    me=[]
    l2=[]
    for i in range(len(c)):

        node = geometry.GEOSGeometry(c[i].mpoly)
        buff=node.buffer(0.00010)
        for j in range(len(r)):
            if buff.intersects(r[j].mpoly):
                l1.append(r[j])
        if len(l1) == 1 and l1[0].name !=crime_road_feature.name and l1[0].name not in l2:
            l2.append(l1[0])
        l1.clear()
        me.clear()

    #print(l2,"yeh pehli list hai dead end ki))))))))))))))))(((((((((((((((((((")
    return l2

def removing_higher_order_dead_end(r,l,nme,c):
    x = True
    na=[]
    for i in range(len(l)):
        na.append(l[i].name)
    featureid = []
    lila = {}
    change = {}
    change[0] = len(l)
    counter = 0
    for a in range(len(r)):
        if r[a].name not in na:
            featureid.append(r[a].name)
    while x:
        for i in range(len(l)):
            na.append(l[i].name)
        counter += 1
        for j in range(len(c)):
            node = geometry.GEOSGeometry(c[j].mpoly)
            buff = node.buffer(0.00006)
            index = 0
            for a in range(len(r)):
                if buff.intersects(r[a].mpoly) and r[a].name in featureid and r[a].name not in na:
                    index += 1
                    lila[index] = r[a]
            if len(lila) == 1 and lila[1].name != nme.name:
                l.append(lila[1])
            lila.clear()
        change[counter] = len(l)
        if change[counter - 1] == change[counter]:
            break
    return l


def firstcord_1(u,c):
    cord = {}
    id={}
    linelength=[]
    pointfeature = {}
    for feat in range(len(c)):
        a=(c[feat].mpoly[0],c[feat].mpoly[1])
        l=haversine(a,u)
        linelength.append(l)
        cord[l] = (c[feat].mpoly[0],c[feat].mpoly[1])
        id [l]=c[feat].name
        pointfeature[l] = c[feat]
    a=min(linelength)
    firstcord = cord[a]
    pfeat = pointfeature[a]
    pointfeature.clear()
    return firstcord,pfeat


def roadlink(pfeat,fcord,m,n,nme,l,name_list,roadId,c,r):
    kdic={}
    start_end_cord={}
    liladhar=[]
    fid = {}
    route = {}
    roade = geometry.GEOSGeometry(pfeat.mpoly)
    buffe = roade.buffer(0.00010)
    for fea in range(len(r)) :
        if buffe.intersects(r[fea].mpoly):
            if r[fea] is None:
                return None,None,"NO FEATURE FOUND"
            if r[fea].name in name_list or r[fea].name in roadId :
                continue
            if r[fea].name==nme.name:
                s = "THE END"
                return r[fea], (r[fea].mpoly[0],r[fea].mpoly[1]), s

            a = featurelength(r[fea])

            line_last_length,lastcord=generating_line_feature(fcord,(r[fea].mpoly[0][0],r[fea].mpoly[0][1]))
            line_start_length,startcord=generating_line_feature(fcord,(r[fea].mpoly[len(r[fea].mpoly)-1][0], r[fea].mpoly[len(r[fea].mpoly)-1][1]))
            b = min(line_last_length, line_start_length)
            d = max(line_last_length, line_start_length)

            kdic[line_start_length] = startcord
            kdic[line_last_length] = lastcord
            cl, outcord = generating_line_feature((m,n), (kdic[d][0],kdic[d][1]))

            start_end_cord[a+b+cl]=(kdic[d][0],kdic[d][1])
            fid[a+b+cl] = r[fea].name

            route[a+b+cl] = r[fea]
            liladhar.append(a+b+cl)
        else:
            continue

    final_route, firstcord, s=check(liladhar,m,n,route,nme,l,name_list,start_end_cord,c,r)
    return final_route,firstcord,s

def check(liladhar,m,n,route,nme,l,name_list,start_end_cord,c,r):
    tup=(m,n)
    s = "CONTINUE"
    x=True
    while x:
        if len(liladhar)==0:
            return None,(0,0),"NOT OK FINISH LIST"
        d=min(liladhar)

        w=start_end_cord[d]
        f=route[d]

        firstcord, pfeat=firstcord_1(w,c)

        r=nodecheck(firstcord[0],firstcord[1], nme, l,name_list,tup[0],tup[1],c,r)

        if r=="ok":
            print("SELECTED FEATURE",f.name,"ITS FAR END COORD",(w[0],w[1]),s)
            return f,(w[0],w[1]),s

        else:
            liladhar.remove(d)
            x=True

def nodecheck(x,y,id,l,name_list,m,n,c,r):

    li=[]
    s="ok"
    t="not ok"
    #pointdatasource = open_File(path="C:/Users\Hp\Desktop\pol\DATA\CITYCENTERNODES.shp")
    #pointlayer = pointdatasource.GetLayerByIndex(0)
    #datasource = open_File(path="C:/Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    #layer = datasource.GetLayerByIndex(0)
    for t in range(len(c)):
        if c[t].mpoly[0]==x and c[t].mpoly[1]==y:
            print ("node Id",c[t].name)
            roa = geometry.GEOSGeometry(c[t].mpoly)
            buffe = roa.buffer(0.00010)
            for fet in range(len(r)):

                if buffe.intersects(r[fet].mpoly) and r[fet].name not in name_list and r[fet].name not in li:
                    o=r[fet].name
                    print("THE SELECTED ROAD FEATURE IS ",o)
                    if o ==id.name:
                        return s
                    num=mindist(r[fet],m,n,x,y,c,r)
                    if num is not None:
                        print("NEXT LINK TO THE CONCERNERD LINK WHICH IS OK FOR CONSIDERATION", r[fet].name)
                        li.append(r[fet].name)

    if len(li)!=0:
        return s
    else:
        return t

def mindist(b,m,n,x,y,c,r):
    dictionary={}
    lengthend, tupcordend = generating_line_feature((m,n),(b.mpoly[0][0], b.mpoly[0][1]))
    dictionary[lengthend] = tupcordend
    lengthstart, tupcordstart = generating_line_feature((m,n),(b.mpoly[len(b.mpoly)-1][0], b.mpoly[len(b.mpoly)-1][1]))
    dictionary[lengthstart] = tupcordstart

    w=farendcord((x,y),b,c,r)

    d=min(lengthend,lengthstart)
    if dictionary[d]==(w[0],w[1]):
        return b
    else:
        return None


def farendcord(fcord,b,c,r):
    kdic={}
    line_last_length, lastcord = generating_line_feature(fcord,(b.mpoly[0][0], b.mpoly[0][1]))
    line_start_length, startcord = generating_line_feature(fcord,(b.mpoly[len(b.mpoly)-1][0], b.mpoly[len(b.mpoly)-1][1]))
    d = max(line_last_length, line_start_length)
    kdic[line_start_length] = startcord
    kdic[line_last_length] = lastcord
    return kdic[d]


def short(v,r,c,a):
    '''road_dictionary={}
    citycenter_node={}
    for i in range(len(r)):
        road_dictionary[r[i].mpoly]=r[i].name
    for j in range(len(c)):
        citycenter_node[c[j].mpoly]=c[j].name'''
    cordlist = []
    name_list=[]
    finalroute = []
    roadId = []
    u=close(v,a)
    result,crime_road_feature=crimelink(r,a)
    l=remove_dead_ends(crime_road_feature,r,c)
    l= removing_higher_order_dead_end(r,l,crime_road_feature,c)
    for i in range(len(l)):
       name_list.append(l[i].name)
    firstcord, pfeat = firstcord_1(u,c)
    cordlist.append(firstcord)
    x = True
    while x:
        final_route, firstcord, s = roadlink(pfeat, firstcord, float(a[len(a) - 1].mpoly[0]), float(a[len(a) - 1].mpoly[1]), crime_road_feature, l,name_list,roadId,c,r )



