# coding:UTF-8
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
from webapp.gis.shortestpath.shapefilecreator import routej
from osgeo import ogr
import operator
#from.t import banakerahegeisbaar
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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def initial_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = radians(pointA[1])
    lat2 = radians(pointB[1])

    diffLong = radians(pointB[0] - pointA[0])

    x = sin(diffLong) * cos(lat2)
    y = cos(lat1) * sin(lat2) - (sin(lat1)
                                 * cos(lat2) * cos(diffLong))

    initial_bearing = atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing


def open_File(path):
    if path is None:
        filePath = str(input("file path"))
    else:
        filePath = path
    datasource = ogr.Open(filePath, 0)
    return datasource


def num_of_layers_in_file(source):
    datasource = source
    numLayers = datasource.GetLayerCount()
    return numLayers


def num_of_features_in_layer(source, Layers):
    datasource = source
    numLayers = Layers
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = layer.GetFeatureCount()
        return numFeatures


def creating_directory(folderPath,folderName):
    #folderName = "SHORTROUTE"
    #folderPath = "C:/Users\Hp\Desktop\DATA"
    path = folderPath + '\\' + folderName
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
    return (cnt, formatsList)


def entered_driver_availiblity(count, list):
    numberOfDriver = count
    driverList = list
    x = input("Enter driver name:")
    if x in driverList:
        print("ok")
        return x
    else:
        print("Value Error:%s is not in list" % x)




def featurelength(a):
    count = a.GetGeometryRef().GetPointCount()
    w = []
    l = 0
    for i in range(count):
        w.append(a.GetGeometryRef().GetPoint(i))
    for i in range(len(w) - 1):
        l = l + haversine(w[i], w[i + 1])
    return l


def generating_line_feature(a, b):
    return haversine(a, b), b





def police():
    datasource = open_File(path="C: / Users\Hp\Desktop\DATA\POLICELOCATION\POLICELOCATION.shp")
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.GetX(), geom.GetY()


def crime(crimepath):
    datasource = open_File(crimepath)
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.GetX(), geom.GetY()


def crimelink(crimepath, networkpath):
    crimedatasource = open_File(crimepath)
    crimelayer = crimedatasource.GetLayerByIndex(0)
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    f = crimelayer.GetFeature(0)
    poly = f.GetGeometryRef().Buffer(0.00010)
    layer.SetSpatialFilter(poly)
    for feature in layer:
        print("the crime link is" + str(feature.GetField("name")), "DATATYPE OF FIELD IS ",
              type(feature.GetField("name")))
        return feature.GetField("name")

def crimelinkwithcoord(q,r, networkpath):
    feature=None
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(q,r)
    for k in range(250):
        poly = point.Buffer(k/100000)
        layer.SetSpatialFilter(poly)
        if layer.GetFeatureCount()>0:
            for feature in layer:
                print("the crime link is" + str(feature.GetField("name")), "DATATYPE OF FIELD IS ",
                  type(feature.GetField("name")))
                '''if feature.GetGeometryRef().GetPointCount()==2:
                    count = feature.GetGeometryRef().GetPointCount()
                    q=((feature.GetGeometryRef().GetPoint(count - 1))[0]+(feature.GetGeometryRef().GetPoint(0)[0]))/2
                    r=((feature.GetGeometryRef().GetPoint(count - 1))[1]+(feature.GetGeometryRef().GetPoint(0)[1]))/2
                if feature.GetGeometryRef().GetPointCount()>2:
                    q=(feature.GetGeometryRef().GetPoint(1))[0]
                    r=(feature.GetGeometryRef().GetPoint(1))[1]'''
                return feature.GetField("name")


def policelink(c, d, networkpath):
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(c),float(d))
    for k in range(250):
        poly = point.Buffer(k/100000)
        layer.SetSpatialFilter(poly)
        if layer.GetFeatureCount()>0:
            for feature in layer:
                print("the police link is" + str(feature.GetField("name")), "DATATYPE OF FIELD IS ",
                      type(feature.GetField("name")))
                '''if feature.GetGeometryRef().GetPointCount()==2:
                    count = feature.GetGeometryRef().GetPointCount()
                    c=((feature.GetGeometryRef().GetPoint(count - 1))[0]+(feature.GetGeometryRef().GetPoint(0)[0]))/2
                    d=((feature.GetGeometryRef().GetPoint(count - 1))[1]+(feature.GetGeometryRef().GetPoint(0)[1]))/2
                if feature.GetGeometryRef().GetPointCount()>2:
                    c=(feature.GetGeometryRef().GetPoint(1))[0]
                    d=(feature.GetGeometryRef().GetPoint(1))[1]'''
                return feature.GetField("name")



def circularring(q, r, c, d, crimelink, policelink,nodepath,networkpath):
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q, r)
    line.AddPoint(c, d)

    poly = line.Buffer(0.0015)
    datasource = open_File(nodepath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    dic = {}
    for feature in layer:
        geom = feature.GetGeometryRef()
        oint = ogr.Geometry(ogr.wkbPoint)
        oint.AddPoint(geom.GetX(), geom.GetY())
        oly = oint.Buffer(0.00006)
        source = open_File(networkpath)
        yer = source.GetLayerByIndex(0)
        yer.SetSpatialFilter(oly)
        ame = []
        for feat in yer:
            ame.append(feat.GetField("name"))
        dic[feature.GetField("name")] = ame
    return dic


def deadendremoval(q, r, c, d, crimelink, policelink, cimenodecord, policenodecord,nodepath,networkpath):
    deadlist = []
    dic = circularring(q, r, c, d, crimelink, policelink,nodepath,networkpath)
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q, r)
    line.AddPoint(c, d)

    poly = line.Buffer(0.0015)
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    for feature in layer:
        i = 0
        # print(feature.GetField("name"))
        for k, v in dic.items():
            if feature.GetField("name") in dic[k]:
                i = i + 1
        if i < 2 and feature.GetField("name") != crimelink and feature.GetField("name") != policelink:
            deadlist.append(feature.GetField("name"))
    remove_dead_ends(q, r, c, d, deadlist, crimelink, policelink,nodepath,networkpath)
    removing_higher_order_dead_end(q, r, c, d, deadlist, crimelink, policelink,nodepath,networkpath)
    legitimateroadlist, lit = roadidlist(q, r, c, d, deadlist,nodepath,networkpath)
    nonlegitimatenodelist = nodelst(q, r, c, d, deadlist,nodepath,networkpath)
    #deadlist.append(crimelink)
    #deadlist.append(policelink)
    lit = routel(cimenodecord, policenodecord, deadlist, legitimateroadlist, lit,nodepath,networkpath)
    # print("LIST OF REMOVED ROAD FEATURE IS",deadlist,"LIST OF LEGITIMATE ROAD FEATURE IS",legitimateroadlist)
    return deadlist, lit


def remove_dead_ends(q, r, c, d, deadlist, startlink, endlink,nodepath,networkpath):
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q, r)
    line.AddPoint(c, d)

    poly = line.Buffer(0.0015)
    datasource = open_File(nodepath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    for feature in layer:
        geom = feature.GetGeometryRef()
        oint = ogr.Geometry(ogr.wkbPoint)
        oint.AddPoint(geom.GetX(), geom.GetY())
        oly = oint.Buffer(0.00006)
        source = open_File(networkpath)
        yer = source.GetLayerByIndex(0)
        yer.SetSpatialFilter(oly)
        if yer.GetFeatureCount() == 1:
            for a in yer:
                if a.GetField("name") != startlink and a.GetField("name") != endlink and a.GetField(
                        "name") not in deadlist:
                    deadlist.append(a.GetField("name"))


def feautreid(q, r, c, d, deadlist,nodepath,networkpath):
    featureid = []
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q, r)
    line.AddPoint(c, d)

    poly = line.Buffer(0.0015)
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    for feature in layer:
        if feature.GetField("name") not in deadlist:
            featureid.append(feature.GetField("name"))
    return featureid


def removing_higher_order_dead_end(q, r, c, d, deadlist, startlink, endlink,nodepath,networkpath):
    x = True
    lila = {}
    change = {}
    change[0] = len(deadlist)
    counter = 0
    id = feautreid(q, r, c, d, deadlist,nodepath,networkpath)
    pointdatasource = open_File(path=nodepath)
    pointlayer = pointdatasource.GetLayerByIndex(0)
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q, r)
    line.AddPoint(c, d)

    poly = line.Buffer(0.0015)
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    while x:
        counter += 1
        pointlayer.SetSpatialFilter(poly)
        for feature in pointlayer:
            '''if feature.GetField("name")==151:
                print(feature.GetField("name"))'''
            layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(0.00010))
            index = 0
            for fe in layer:

                if fe.GetField("name") in id and fe.GetField("name") not in deadlist:
                    index += 1
                    '''if fe.GetField("name") == 348:
                        print(fe.GetField("name"), id, deadlist, lila)'''
                    lila[index] = fe.GetField("name")
            # print(lila)
            if len(lila) == 1 and lila[1] != startlink and lila[1] != endlink:
                deadlist.append(lila[1])
            lila.clear()
        change[counter] = len(deadlist)
        if change[counter - 1] == change[counter]:
            break


def roadidlist(q, r, c, d, deadlist,nodepath,networkpath):
    legitimateroadlist = []
    lit = []
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q, r)
    line.AddPoint(c, d)

    poly = line.Buffer(0.0015)
    routej(poly.ExportToWkt(), "C:/Users\Hp\Desktop","POLYGON")
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    for feat in layer:
        if feat.GetField("name") not in deadlist:
            legitimateroadlist.append(feat.GetField("name"))
            lit.append(feat.GetField("name"))
    return legitimateroadlist, lit


def nodelst(q, r, c, d, deadlist,nodepath,networkpath):
    nonlegitimatenodelist = []
    legitimatenodelist = []
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(q,r)
    line.AddPoint(c,d)

    poly = line.Buffer(0.0015)
    datasource = open_File(nodepath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    source = open_File(path=networkpath)
    r = source.GetLayerByIndex(0)
    test = []
    for feat in layer:
        r.SetSpatialFilter(feat.GetGeometryRef().Buffer(0.00010))
        for f in r:
            if f.GetField("name") not in deadlist:
                test.append(f.GetField("name"))
        count = len(test)
        if count == 0:
            nonlegitimatenodelist.append(feat.GetField("name"))
        else:
            legitimatenodelist.append(feat.GetField("name"))
        test.clear()
    return nonlegitimatenodelist


def routel(cimenodecord, policenodecord, deadlist, legitimateroadlist, lit,nodepath,networkpath):
    # print(cimenodecord, policenodecord,deadlist,legitimateroadlist)
    line = ogr.Geometry(ogr.wkbLineString)
    line.AddPoint(cimenodecord[0], cimenodecord[1])
    line.AddPoint(policenodecord[0], policenodecord[1])

    poly = line.Buffer(0.0015)
    routej(poly.ExportToWkt(),"C:/Users\Hp\Desktop" ,"POLY")
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(poly)
    # print(layer.GetFeatureCount())
    for feat in layer:
        if feat.GetField("name") not in deadlist and feat.GetField("name") not in lit:
            lit.append(feat.GetField("name"))
    return lit


def farendcord(fcord, b,nodepath,networkpath):
    datasource = open_File(path=networkpath)
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") == b:
                feature = feat
                count = feature.GetGeometryRef().GetPointCount()
                kdic = {}
                line_last_length, lastcord = generating_line_feature(fcord,
                                                                     feature.GetGeometryRef().GetPoint(count - 1))
                line_start_length, startcord = generating_line_feature(fcord, feature.GetGeometryRef().GetPoint(0))
                d = max(line_last_length, line_start_length)
                kdic[line_start_length] = startcord
                kdic[line_last_length] = lastcord
                return kdic[d]
            else:
                continue


def feature_in_buffer(pfeat):
    datasource = open_File(path="C:/Users\Hp\Desktop\DATA\ROADNETWORK\ROADNETWORK.shp")
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(pfeat.GetGeometryRef().Buffer(0.00010))
    count = layer.GetFeatureCount()
    if count == 1:
        print("NO FEATURE FOUND")
        return "NO FEATURE FOUND"


def roadlink(pfeat, fcord, q, r, id, l, roadId, lit,dynadead,fruit,nodepath,networkpath):

    kdic = {}
    start_end_cord = {}
    liladhar = []
    fid = {}
    route = {}
    datasource = open_File(path=networkpath)
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(pfeat.GetGeometryRef().Buffer(0.00010))
    fcount = layer.GetFeatureCount()
    for feature in layer:
        if feature is None:
            return None, None, "NO FEATURE FOUND"
        if feature.GetField("name") in l or feature.GetField("name") in roadId:
            continue
        if feature.GetField("name") not in lit and feature.GetField("name") not in fruit:
            continue
        if feature.GetField("name") in dynadead:
            continue
        if (feature.GetField("name")) == (id):
            s = "THE END"
            return feature, (feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1]), s
        a = featurelength(feature)
        count = feature.GetGeometryRef().GetPointCount()
        line_last_length, lastcord = generating_line_feature(fcord, (
            feature.GetGeometryRef().GetPoint(count - 1)[0], feature.GetGeometryRef().GetPoint(count - 1)[1]))
        line_start_length, startcord = generating_line_feature(fcord, (
            feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1]))
        b = min(line_last_length, line_start_length)
        d = max(line_last_length, line_start_length)
        kdic[line_start_length] = startcord
        kdic[line_last_length] = lastcord
        c, outcord = generating_line_feature((q, r), (kdic[d][0], kdic[d][1]))
        start_end_cord[a + b + c] = (kdic[d][0], kdic[d][1])
        fid[a + b + c] = (feature.GetField("name"))
        route[a + b + c] = feature
        liladhar.append(a + b + c)
    # print(a, feature.GetField("name"))
    #print(fid,"ROUTE LIST FROM NODE")

    final_route, firstcord, s = check(liladhar, q, r, route, id, l, start_end_cord, lit,nodepath,networkpath)

    return final_route, firstcord, s


def check(liladhar, q, r, route, id, l, start_end_cord, lit,nodepath,networkpath):
    tup = (q, r)
    s = "CONTINUE"
    x = True
    while x:
        if len(liladhar) == 0:
            return None, (0, 0), "NOT OK FINISH LIST"
        d = min(liladhar)
        # print("MINIMUM LENGTH FOR THE ABOVE SELECTED ROAD FEATURE IS", d)
        w = start_end_cord[d]
        f = route[d]
        firstcord, pfeat = firstcord_1(w[0], w[1],nodepath,networkpath)
        # print("CITY CENTERNODE CLOSEST TO THE END POINT OF THE SELECTED ROAD FEATURE", f.GetField("name"), "IS",pfeat.GetField("name"))
        # print("NOW WE WILL CHECK THAT ROAD FEATURE GENERATING FROM THIS NODE IS OK OR NOT")
        r = nodecheck(firstcord[0], firstcord[1], id, l, tup[0], tup[1], lit,nodepath,networkpath)
        # print("node check", r)
        if r == "ok":
            return f, (w[0], w[1]), s
        else:
            liladhar.remove(d)
            x = True


def nodecheck(x, y, id, l, q, r, lit,nodepath,networkpath):
    li = []
    s = "ok"
    t = "not ok"
    pointdatasource = open_File(path=nodepath)
    pointlayer = pointdatasource.GetLayerByIndex(0)
    datasource = open_File(path=networkpath)
    layer = datasource.GetLayerByIndex(0)
    for feature in pointlayer:
        if feature.GetGeometryRef().GetX() == x and feature.GetGeometryRef().GetY() == y:
            layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(0.00010))
            for feat in layer:
                if feat.GetField("name") not in lit:
                    continue
                if feat.GetField("name") not in l and feat.GetField("name") not in li:
                    o = (feat.GetField("name"))
                    # print("ROAD FEATURE EMERGING FROM THIS NODE", feature.GetField("name"), "is", o)
                    if o == id:
                        # print("THE ROAD FEATURE IS CRIME LINK HENCE SEARCH IS OVER")
                        return s
                    # print("CHECKING WHETHER THIS ROAD FEATURE IS TOWARD CRIME LOCATION OR AWAY FROM IT")
                    num = mindist(o, q, r, x, y, lit,nodepath,networkpath)
                    if num is not None:
                        # print("id of road feature toward crime location", num)
                        li.append(num)
    if len(li) != 0:
        return s
    else:
        return t


def mindist(b, q, r, x, y, lit,nodepath,networkpath):
    dictionary = {}
    datasource = open_File(path=networkpath)
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") not in lit:
                continue
            if feat.GetField("name") == b:
                a = feat
                count = a.GetGeometryRef().GetPointCount()
                lengthend, tupcordend = generating_line_feature((q, r), (
                    a.GetGeometryRef().GetPoint(count - 1)[0], a.GetGeometryRef().GetPoint(count - 1)[1]))
                dictionary[lengthend] = tupcordend
                lengthstart, tupcordstart = generating_line_feature((q, r), (
                    a.GetGeometryRef().GetPoint(0)[0], a.GetGeometryRef().GetPoint(0)[1]))
                dictionary[lengthstart] = tupcordstart
                w = farendcord((x, y), b,nodepath,networkpath)
                # print(w)
                d = min(lengthend, lengthstart)
                if dictionary[d] == (w[0], w[1]):
                    # print("THE ROAD FEATURE WHICH IS TOWARD CRIME LINK IS", "=", b)
                    return b
                else:
                    return None


def firstcord_1(c, d,nodepath,networkpath):
    cord = {}
    id = {}
    linelength = []
    pointdatasource = open_File(path=nodepath)
    pointlayer = pointdatasource.GetLayerByIndex(0)
    pointfeature = {}
    for feature in pointlayer:
        a = (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        b = (c, d)
        l = haversine(a, b)
        linelength.append(l)
        cord[l] = (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        id[l] = (feature.GetField("name"))
        pointfeature[l] = feature
    a = min(linelength)
    firstcord = cord[a]
    pfeat = pointfeature[a]
    pointfeature.clear()
    return firstcord, pfeat


def nearest_policia(path, crimepath):
    d = {}
    patht = {}
    l = []
    crimedatasource = open_File(crimepath)
    clayer = crimedatasource.GetLayerByIndex(0)
    cfeat = clayer.GetFeature(0)
    datasource = open_File(path)
    layer = datasource.GetLayerByIndex(0)
    for feat in layer:
        pointA = (feat.GetGeometryRef().GetX(), feat.GetGeometryRef().GetY())
        pointB = (cfeat.GetGeometryRef().GetX(), cfeat.GetGeometryRef().GetY())
        length = haversine(pointA, pointB)
        patht[length] = (feat.GetField("name"))
        d[length] = feat
        l.append(length)
    return d[min(l)].GetGeometryRef().GetX(), d[min(l)].GetGeometryRef().GetY()


def a(flink, t):
    l = {}
    datasource = open_File(path="C:/Users\Hp\Desktop\DATA\ROADNETWORK\ROADNETWORK.shp")
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") == flink:
                a = feat
                count = a.GetGeometryRef().GetPointCount()
                w = ((a.GetGeometryRef().GetPoint(count - 1)[0], a.GetGeometryRef().GetPoint(count - 1)[1]),
                     (a.GetGeometryRef().GetPoint(0)[0], a.GetGeometryRef().GetPoint(0)[1]))
                l[haversine(w[0], t)] = w[0]
                l[haversine(w[1], t)] = w[1]
                pointdatasource = open_File(path="C:/Users\Hp\Desktop\DATA/NODES/NODES.shp")
                pointlayer = pointdatasource.GetLayerByIndex(0)
                '''for feature in pointlayer:
                    if (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY()) == w[0]:
                        #print(feature.GetField("name"))
                    elif (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY()) == w[1]:
                        # print(feature.GetField("name"))'''
                xmin = l[min(haversine(w[0], t), haversine(w[1], t))]
                ymax = l[max(haversine(w[0], t), haversine(w[1], t))]
                return xmin, ymax


def shortest_path_forward(q, r, c, d, cimelink, plink, policenodefeat, policenodecord, cimenodecord,dynadead,fruit,nodepath,networkpath):
    cordlist = []
    finalroute = []
    roadId = []
    l, lit = deadendremoval(q, r, c, d, cimelink, plink, cimenodecord, policenodecord,nodepath,networkpath)
    # firstcord, pfeat=firstcord_1(c,d)
    cordlist.append(policenodecord)
    x = True
    while x:
        final_route, firstcord, s = roadlink(policenodefeat, policenodecord, float(cimenodecord[0]),
                                             float(cimenodecord[1]), cimelink, l, roadId, lit,dynadead,fruit,nodepath,networkpath)
        if s == "NOT OK FINISH LIST":
            # print(s)
            break
        policenodecord, policenodefeat = firstcord_1(firstcord[0], firstcord[1],nodepath,networkpath)
        cordlist.append(firstcord)
        finalroute.append(final_route)
        roadId.append((final_route.GetField("name")))
        print(roadId)

        # print ("THE PATH COMPRISES OF FOLLOWING LINK",roadId,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if s == "THE END":
            x = False
            # print("LOCATION REACHED")
    # print(roadId)
    return roadId


def shortest_path_reverse(q, r, c, d, cimelink, plink, policenodefeat, policenodecord, cimenodecord,dynadead,fruit,nodepath,networkpath):
    cordlist = []
    finalroute = []
    revroadId = []
    l, lit = deadendremoval(q, r, c, d, cimelink, plink, cimenodecord, policenodecord,nodepath,networkpath)
    # firstcord, pfeat=firstcord_1(c,d)
    cordlist.append(policenodecord)
    x = True
    while x:
        final_route, firstcord, s = roadlink(policenodefeat, policenodecord, float(cimenodecord[0]),
                                             float(cimenodecord[1]), cimelink, l, revroadId, lit,dynadead,fruit,nodepath,networkpath)
        if s == "NOT OK FINISH LIST":
            # print(s)
            break
        policenodecord, policenodefeat = firstcord_1(firstcord[0], firstcord[1],nodepath,networkpath)
        cordlist.append(firstcord)
        finalroute.append(final_route)
        revroadId.append((final_route.GetField("name")))
        # print ("THE PATH COMPRISES OF FOLLOWING LINK",roadId,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        if s == "THE END":
            x = False
            # print("LOCATION REACHED")
    # print(revroadId)
    return revroadId


def commonid(forwardroute, reverseroute):
    print(forwardroute, "forwardroute", reverseroute, "reverseroute")
    l = []
    x = 0
    for element in range(len(forwardroute)):
        a = []
        if forwardroute[element] in reverseroute:
            for m, n in enumerate(forwardroute):
                if n == forwardroute[element]:
                    a.append(m)
                    print(m, forwardroute[element])
            for i, j in enumerate(reverseroute):
                if j == forwardroute[element]:
                    a.append(i)
                    print(i, forwardroute[element])
            l.append(a)
    print(l)
    return l


def list_of_possible_path(forwardroute, reverseroute, l):
    final_route = []
    for t in range(len(l)):
        final_sub_route = []
        for element in range(len(forwardroute)):
            if element < l[t][0]:
                final_sub_route.append(forwardroute[element])
        for element in range(len(reverseroute)):
            if element < (l[t][1] + 1):
                final_sub_route.append(reverseroute[l[t][1] - element])
        final_route.append(final_sub_route)
    print(final_route)
    return final_route


def route_id_list(possible_route,nodepath,networkpath):
    lengthd = {}
    lengthl = []
    for i in range(len(possible_route)):
        a = 0
        for j in range(len(possible_route[i])):
            datasource = open_File(path=networkpath)
            for layer in datasource:
                for f in layer:
                    if f.GetField("name")==possible_route[i][j]:
                        a = a + featurelength(f)
        lengthd[a] = i
        lengthl.append(a)
        a = 0
    x = lengthd[min(lengthl)]
    return possible_route[x]


def wktlist(finalroute,cli,pli,nodepath,networkpath):
    li = []
    datasource = open_File(path=networkpath)
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") in finalroute and feat.GetField("name") !=cli and feat.GetField("name") !=pli :
                print(feat.GetGeometryRef().ExportToWkt(),type(feat.GetGeometryRef().ExportToWkt()))
                li.append(feat.GetGeometryRef().ExportToWkt())
    return li

def wktsingle(froute,networkpath):
    datasource = open_File(path=networkpath)
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") in froute:
                return feat.GetGeometryRef().ExportToWkt()


def route(li,path,name):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directory(path,name)
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)
    for i in li:
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        line = ogr.CreateGeometryFromWkt(i)
        feature.SetGeometry(line)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    dstFile.Destroy()


def shortroute(q, r, c, d, cimelink, plink, policenodefeat, policenodecord, crimenodefeat, crimenodecord, cimenodecord):
    forwardroute = shortest_path_forward(q, r, c, d, cimelink, plink, policenodefeat, policenodecord, cimenodecord)
    print("THE FORWARD ROUTE IS AS FOLLOWS", forwardroute)
    reverseroute = shortest_path_reverse(c, d, q, r, plink, cimelink, crimenodefeat, crimenodecord, policenodecord)
    print("THE REVERSE ROUTE IS AS FOLLOWS", reverseroute)
    l = commonid(forwardroute, reverseroute)
    print("COMMON ID Are AS FOLLOWS", l)
    possible_route = list_of_possible_path(forwardroute, reverseroute, l)
    print("THE POSSIBLE ROUTES ARE AS FOLLOWS", possible_route)
    froute = route_id_list(possible_route)
    print(froute,
          "result@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    lk = wktlist(froute)
    route(lk)

    return froute


def bufgeo(point, dist):
    pointA = point[0]
    pointB = point[1]
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(pointA, pointB)
    poly = point.Buffer(dist)
    return poly


def listofnode(flink, plink,nodepath,networkpath):
    policenodelist = {}
    crimenodelist = {}
    datasource = open_File(path=networkpath)
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") == flink:
                count = feat.GetGeometryRef().GetPointCount()
                p = bufgeo((feat.GetGeometryRef().GetPoint(count - 1)[0], feat.GetGeometryRef().GetPoint(count - 1)[1]),
                           0.00010)
                qd = bufgeo((feat.GetGeometryRef().GetPoint(0)[0], feat.GetGeometryRef().GetPoint(0)[1]), 0.00010)
                nodedatasource = open_File(path=nodepath)
                for k in nodedatasource:
                    k.SetSpatialFilter(p)
                    for w in k:
                        crimenodelist[w] = (w.GetField("name"))
                    k.SetSpatialFilter(qd)
                    for e in k:
                        crimenodelist[e] = (e.GetField("name"))
            if feat.GetField("name") == plink:
                count = feat.GetGeometryRef().GetPointCount()
                p = bufgeo((feat.GetGeometryRef().GetPoint(count - 1)[0], feat.GetGeometryRef().GetPoint(count - 1)[1]),
                           0.00010)
                qd = bufgeo((feat.GetGeometryRef().GetPoint(0)[0], feat.GetGeometryRef().GetPoint(0)[1]), 0.00010)
                nodedatasource = open_File(path=nodepath)
                for k in nodedatasource:
                    k.SetSpatialFilter(p)
                    for f in k:
                        policenodelist[f] = (f.GetField("name"))
                    k.SetSpatialFilter(qd)
                    for s in k:
                        policenodelist[s] = (s.GetField("name"))

    return (policenodelist, crimenodelist)


def pointsetgenerator(policepoint, crimepoint, policenodelist, crimenodelist):
    p = {}
    c = {}
    for k, v in policenodelist.items():
        p[k] = policepoint[policenodelist[k]]

    for a, b in crimenodelist.items():
        c[a] = crimepoint[crimenodelist[a]]
    return p, c


def anbtobanjao(c, d, q, r,nodepath,networkpath):

    policepoint = {}
    crimepoint = {}
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(q, r)
    li = point.ExportToWkt()
    routej(li, name="CRIMELOCATION", path="C:/Users\Hp\Desktop\POLYGON")
    crimepath = "C:/Users\Hp\Desktop\POLYGON\CRIMELOCATION\CRIMELOCATION.shp"
    flink = (crimelink(crimepath, networkpath))
    plink = policelink(c, d, networkpath)
    print(flink,"asdfghjkjhgfdsasdfghjhgfds", plink)
    a = input("enter code")
    if a == 1:
        pass
    policenodelist, crimenodelist = listofnode(flink, plink,nodepath,networkpath)

    for k, v in policenodelist.items():
        policepoint[policenodelist[k]] = (k.GetGeometryRef().GetX(), k.GetGeometryRef().GetY())
    for l, m in crimenodelist.items():
        crimepoint[crimenodelist[l]] = (l.GetGeometryRef().GetX(), l.GetGeometryRef().GetY())

    police, crime = pointsetgenerator(policepoint, crimepoint, policenodelist, crimenodelist)

    return police, crime, plink, flink


def abhibanega(flink, plink,nodepath,networkpath):

    policepoint = {}
    crimepoint = {}
    policenodelist, crimenodelist = listofnode(flink, plink,nodepath,networkpath)
    for k, v in policenodelist.items():
        policepoint[policenodelist[k]] = (k.GetGeometryRef().GetX(), k.GetGeometryRef().GetY())
    for l, m in crimenodelist.items():
        crimepoint[crimenodelist[l]] = (l.GetGeometryRef().GetX(), l.GetGeometryRef().GetY())
    police, crime = pointsetgenerator(policepoint, crimepoint, policenodelist, crimenodelist)
    return police, crime, plink, flink

def bansaktahaiforwardroute(police, crime, plink, flink,a,dynadead,fruit,nodepath,networkpath):
    nextgen = {}
    jahis={}
    kash=[]
    crimeLink = None
    policeLink = None
    forwardroute = None
    reverseroute = None
    policenodefeat, policenodecord, crimenodefeat, crimenodecord,cor=None,None,None,None,None
    link = [flink, plink]
    datasource = open_File(path=networkpath)

    for layer in datasource:

        for z, x in police.items():
            for o, p in crime.items():
                policenodefeat = z
                policenodecord = police[z]
                crimenodefeat = o
                crimenodecord = crime[o]
                #print(policenodefeat.GetField("name"), policenodecord, crimenodefeat.GetField("name"), crimenodecord)
                goly=bufgeo(policenodecord,0.00010)
                layer.SetSpatialFilter(goly)
                if layer.GetFeatureCount()==1:
                    continue
                holy=bufgeo(crimenodecord,0.00010)
                layer.SetSpatialFilter(holy)
                if layer.GetFeatureCount()==1:
                    continue
                jahis[haversine(policenodecord,crimenodecord)]=[policenodefeat, policenodecord, crimenodefeat, crimenodecord]

                kash.append(haversine(policenodecord,crimenodecord))
    if a == 1:
        policenodefeat, policenodecord, crimenodefeat, crimenodecord=jahis[min(kash)][0],jahis[min(kash)][1],jahis[min(kash)][2],jahis[min(kash)][3]
        cor=[policenodefeat, policenodecord, crimenodefeat, crimenodecord]
    if a==0:
        policenodefeat, policenodecord, crimenodefeat, crimenodecord = jahis[max(kash)][0], jahis[max(kash)][1], \
                                                                       jahis[max(kash)][2], jahis[max(kash)][3]
        cor = [policenodefeat, policenodecord, crimenodefeat, crimenodecord]
    print(policenodefeat.GetField("name"), policenodecord, crimenodefeat.GetField("name"), crimenodecord,"YOU GOT SELECTED")
    lis = [crimenodecord[0], crimenodecord[1], policenodecord[0], policenodecord[1]]
    forwardroute = shortest_path_forward(lis[2], lis[3], lis[0], lis[1], flink, plink, policenodefeat,
                                         policenodecord,
                                         crimenodecord,dynadead,fruit,nodepath,networkpath)
    if len(forwardroute) is not 0:
        return forwardroute,forwardroute[len(forwardroute)-1]
    else:
        return forwardroute, plink

def bansaktahaibackwardroute(police, crime, plink, flink,a,dynadead,fruit,nodepath,networkpath):
    nextgen = {}
    h=0
    jahis={}
    kash={}
    crimeLink = None
    policeLink = None
    forwardroute = None
    reverseroute = None
    policenodefeat, policenodecord, crimenodefeat, crimenodecord,cor=None,None,None,None,None
    link = [flink, plink]
    datasource = open_File(path=networkpath)
    for layer in datasource:

        for z, x in police.items():
            for o, p in crime.items():

                policenodefeat = z
                policenodecord = police[z]
                crimenodefeat = o
                crimenodecord = crime[o]
                #print(policenodefeat.GetField("name"), policenodecord, crimenodefeat.GetField("name"), crimenodecord)
                goly=bufgeo(policenodecord,0.00010)
                layer.SetSpatialFilter(goly)
                if layer.GetFeatureCount()==1:
                    continue
                holy=bufgeo(crimenodecord,0.00010)
                layer.SetSpatialFilter(holy)
                if layer.GetFeatureCount()==1:
                    continue
                jahis[haversine(policenodecord,crimenodecord)]=[policenodefeat, policenodecord, crimenodefeat, crimenodecord]
                kash[h]=haversine(policenodecord,crimenodecord)
                h=h+1
    policenodefeat, policenodecord, crimenodefeat, crimenodecord=jahis[kash[a]][0],jahis[kash[a]][1],jahis[kash[a]][2],jahis[kash[a]][3]
    cor=[policenodefeat, policenodecord, crimenodefeat, crimenodecord]
    #print(policenodefeat.GetField("name"), policenodecord, crimenodefeat.GetField("name"), crimenodecord,"YOU GOT SELECTED")
    lis = [crimenodecord[0], crimenodecord[1], policenodecord[0], policenodecord[1]]
    reverseroute = shortest_path_reverse(lis[0], lis[1], lis[2], lis[3], link[1], link[0], cor[2], cor[3],
                                         cor[1],dynadead,fruit,nodepath,networkpath)
    if len(reverseroute) is not 0:
        return reverseroute,reverseroute[len(reverseroute)-1]
    else:
        return reverseroute,flink

def banakerahege(c,d,q,r,fruit,nodepath,networkpath,path,name,a):
    kkk=0
    s="no matching"
    forddic={}
    cli=crimelinkwithcoord(q, r, networkpath)
    pli=policelink(c, d, networkpath)
    froute=None
    if cli!=pli:
        print(cli,pli)
        g=a
        rev=[]
        ford = []
        dynadead=[]
        crimeLink, policeLink=None,None
        police, crime, plink, flink=abhibanega(cli, pli,nodepath,networkpath)
        forwardroute, plink= bansaktahaiforwardroute(police, crime, plink, flink,g,dynadead,fruit,nodepath,networkpath)
        police, crime, plink, flink=abhibanega(flink, plink,nodepath,networkpath)
        reverseroute,flink=bansaktahaibackwardroute(police, crime, plink, flink,g,dynadead,fruit,nodepath,networkpath)
        for i in forwardroute:
            if i not in ford:
                ford.append(i)
        for k in reverseroute:
            if k not in rev:
                rev.append(k)
        kkk = kkk + int(1)
        forddic[kkk] = [len(ford), len(rev)]

        l = commonid(ford, rev)
        if len(l) == 0:
            if len(forwardroute) is 0:
                policeLink = plink
            if len(forwardroute) is not 0:
                policeLink = forwardroute[len(forwardroute) - 1]
            if len(reverseroute) is 0:
                crimeLink = flink
            if len(reverseroute) is not 0:
                crimeLink = reverseroute[len(reverseroute) - 1]
            #dynadead.append(policeLink)
            #dynadead.append(crimeLink)
            while len(l) is 0:
                police, crime, plink, flink = abhibanega(flink, plink,nodepath,networkpath)
                forwardroute, plink = bansaktahaiforwardroute(police, crime, plink, flink, g, dynadead,fruit,nodepath,networkpath)
                police, crime, plink, flink = abhibanega(flink, plink,nodepath,networkpath)
                reverseroute, flink = bansaktahaibackwardroute(police, crime, plink, flink, g, dynadead,fruit,nodepath,networkpath)
                for i in forwardroute:
                    if i not in ford:
                        ford.append(i)
                for k in reverseroute:
                    if k not in rev:
                        rev.append(k)
                kkk = kkk + 1
                forddic[kkk] = [len(ford), len(rev)]

                for i in range(len(forddic)):
                    if forddic[(len(forddic))-1]==forddic[len(forddic)]:
                        return ford,rev,s

                l = commonid(ford, rev)
                if len(l) == 0:
                    if len(forwardroute) is 0:
                        policeLink = plink
                    if len(forwardroute) is not 0:
                        policeLink = forwardroute[len(forwardroute) - 1]
                    if len(reverseroute) is 0:
                        crimeLink = flink
                    if len(reverseroute) is not 0:
                        crimeLink = reverseroute[len(reverseroute) - 1]
                    #dynadead.append(policeLink)
                    #dynadead.append(crimeLink)
                if len(l) > 0:
                    possible_route = list_of_possible_path(ford, rev, l)
                    print("THE POSSIBLE ROUTES ARE AS FOLLOWS", possible_route)

                    froute = route_id_list(possible_route,nodepath,networkpath)
                    print(froute,
                          "result@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
                    #lk = wktlist(froute)
                    #route(lk,path,name)
                    print(froute,"yehui na baat")
                    if cli not in froute:
                        froute.append(cli)
                    if pli not in froute:
                        froute.append(pli)
                    #lk = wktlist(froute)
                    #route(lk, path, name)
                    return froute,cli,pli
        if len(l) > 0:
            possible_route = list_of_possible_path(ford, rev, l)

            print("THE POSSIBLE ROUTES ARE AS FOLLOWS", possible_route)

            froute = route_id_list(possible_route,nodepath,networkpath)
            print(froute,
                  "result@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
            #lk = wktlist(froute)
            #route(lk,path,name)
            print(froute, "yehui na baat")
            if cli not in froute:
                froute.append(cli)
            if pli not in froute:
                froute.append(pli)
            return froute, cli, pli
            #lk = wktlist(froute)
            #route(lk, path, name)
    if cli==pli:
        line = ogr.Geometry(ogr.wkbLineString)
        line.AddPoint(q, r)
        line.AddPoint(c, d)
        line.ExportToWkt()
        routej(line,path,name)
#fruit=[]
#routf=banakerahege(78.19940686225893,26.20554286060711,78.19471758105658,26.211987787553117, "C:/Users\Hp\Desktop\DATA", "SHORTROUTE",fruit)

def boundingpre(cli,pli,nodepath,networkpath):
    cbuf1, cbuf2, pbuf1, pbuf2=None,None,None,None
    ccord1,ccord2=[],[]
    pcord1,pcord2=[],[]
    datasource = open_File(path=networkpath)
    for layer in datasource:
        for feat in layer:
            if feat.GetField("name") == cli:
                feature = feat
                count = feature.GetGeometryRef().GetPointCount()
                kdic = {}
                cbuf1=bufgeo(feature.GetGeometryRef().GetPoint(count - 1), 0.00010)
                ccord1=[feature.GetGeometryRef().GetPoint(count - 1)[0],feature.GetGeometryRef().GetPoint(count - 1)[1]]
                cbuf2=bufgeo(feature.GetGeometryRef().GetPoint(0), 0.00010)
                ccord2 = [feature.GetGeometryRef().GetPoint(0)[0],
                          feature.GetGeometryRef().GetPoint(0)[1]]
            if feat.GetField("name") == pli:
                feature = feat
                count = feature.GetGeometryRef().GetPointCount()
                kdic = {}
                pbuf1 = bufgeo(feature.GetGeometryRef().GetPoint(count - 1), 0.00010)
                pcord1=[feature.GetGeometryRef().GetPoint(count - 1)[0],feature.GetGeometryRef().GetPoint(count - 1)[1]]
                pbuf2 = bufgeo(feature.GetGeometryRef().GetPoint(0), 0.00010)
                pcord2=[feature.GetGeometryRef().GetPoint(0)[0],feature.GetGeometryRef().GetPoint(0)[1]]
    print(pcord1,pcord2,ccord1,ccord2)
    return cbuf1,cbuf2,pbuf1,pbuf2,pcord1,pcord2,ccord1,ccord2

def boundingmains(c,d,q,r,froute,cbuf1,cbuf2,pbuf1,pbuf2,pcord1,pcord2,ccord1,ccord2,cli,pli,nodepath,networkpath):
    cline,pline=None,None
    datasource = open_File(path=networkpath)
    for layer in datasource:
        layer.SetSpatialFilter(cbuf1)
        for feat in layer:
            if feat.GetField("name") in froute and feat.GetField("name")!= cli:
                cline = ogr.Geometry(ogr.wkbLineString)
                cline.AddPoint(q,r)
                cline.AddPoint(ccord1[0], ccord1[1])

        layer.SetSpatialFilter(cbuf2)
        for feat in layer:
            if feat.GetField("name") in froute and feat.GetField("name")!= cli:
                cline = ogr.Geometry(ogr.wkbLineString)
                cline.AddPoint(q, r)
                cline.AddPoint(ccord2[0], ccord2[1])

        layer.SetSpatialFilter(pbuf1)
        for feat in layer:
            if feat.GetField("name") in froute and feat.GetField("name")!= pli:
                pline = ogr.Geometry(ogr.wkbLineString)
                pline.AddPoint(c, d)
                pline.AddPoint(pcord1[0], pcord1[1])

        layer.SetSpatialFilter(pbuf2)
        for feat in layer:
            if feat.GetField("name") in froute and feat.GetField("name")!= pli:
                pline = ogr.Geometry(ogr.wkbLineString)
                pline.AddPoint(c, d)
                pline.AddPoint(pcord2[0], pcord2[1])
    return cline.ExportToWkt(),pline.ExportToWkt()


def prefinaldest(cline,pline,cli,pli,froute,path,name,nodepath,networkpath):
    li=wktlist(froute, cli, pli,nodepath,networkpath)
    li.append(cline)
    li.append(pline)

    route(li, path, name)

def main(c, d, q, r, path, name, fruit):
    por={}
    lg=[]
    e,p=None,None
    networkpath="C:/Users\Hp\Desktop\DATA\DELHIRODES\DELHIRODES.shp"
    nodepath="C:/Users\Hp\Desktop\DATA\DELHINODES\DELHINODES.shp"

    for a in range(4):
        froute, cli, pli = banakerahege(c, d, q, r, fruit, nodepath, networkpath, path, name,a)
        if pli!="null":
            por[a]=[froute,cli,pli]
    for k,v in por.items():
        lg.append(por[k][0])
    x = route_id_list(lg, nodepath, networkpath)
    for k, v in por.items():
        if por[k][0]==x:
            e=por[k][1]
            p=por[k][2]

    if len(x)>1:
        cbuf1, cbuf2, pbuf1, pbuf2, pcord1, pcord2, ccord1, ccord2=boundingpre(e, p,nodepath,networkpath)
        cline, pline=boundingmains(c,d,q, r, x, cbuf1, cbuf2, pbuf1, pbuf2, pcord1, pcord2, ccord1, ccord2, c, p,nodepath,networkpath)
        prefinaldest(cline, pline, c, p, x, path, name,nodepath,networkpath)
    '''if len(x)==1:
        a=wktsingle(x, networkpath)
        route(a,path,name)'''

"C:/Users\Hp\Desktop\DATA\ROADNETWORK\ROADNETWORK.shp"
"C:/Users\Hp\Desktop\DATA/NODES/NODES.shp"
"C:/Users\Hp\Desktop\DATA\DELHINODES\DELHINODES.shp"
"C:/Users\Hp\Desktop\DATA\DELHIRODES\DELHIRODES.shp"





#main(77.2070318533531,	28.5970108816524,	77.2123072680898,	28.6027296091383, "C:/Users\Hp\Desktop\DATA", "SHORTROUTE40",fruit=[])
#main(77.21468681896567,28.609010178655325,77.20864841003504,28.605942763516996, "C:/Users\Hp\Desktop\DATA", "SHORTROUTE13",fruit=[])
# shortroute(q,r, c, d, flink,plink,policenodefeat,policenodecord,crimenodefeat,crimenodecord,cimenodecord=crime[o])

# shortroute(crimepath="C:/Users\Hp\Desktop\DATA\CRIMELOCATION\CRIMELOCATION.shp", c=78.19112258984933,d=26.208934878226977)





