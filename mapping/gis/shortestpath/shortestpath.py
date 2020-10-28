#coding:UTF-8
import ogr
import osgeo
import os, os.path, shutil
import osgeo.ogr
import osgeo.osr
import glob
from osgeo import ogr
from math import radians, cos, sin, asin, sqrt, atan2, degrees


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
        filePath=path
    datasource = ogr.Open(filePath,0)
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

def creating_directory():
    folderName = input("Enter Folder Name")
    folderPath = input("Where you want to save folder ")
    path = folderPath + '\\' + folderName
    if os.path.exists("%s" % path):
        shutil.rmtree("%s" % path)
    os.mkdir("%s" % path)
    return (path, folderName)

def creating_directory_short_path(i):
    folderName = "NEWSHORTROUTE%d"%i
    folderPath = "C:\Users\Hp\Desktop\pol\SHORTROUTE"
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

def creating_shape_file_of_given_geometry (info):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    count, list = number_of_available_drivers()
    driverName = entered_driver_availiblity(count, list)
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation,folderName = creating_directory()
    name=input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp"%name)
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
    fieldList=[]
    for i in range (numField):
        ftype= input("please enter number corresponding to the type of field you want to make (integer value)")
        if ftype==1:
            fieldName=str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTInteger)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype==2:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTIntegerList)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype==3:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTReal)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype==4:
            fieldName = str(input("enter feild name"))
            fieldDef = osgeo.ogr.FieldDefn("%s" % fieldName, osgeo.ogr.OFTRealList)
            width = int(input("Enter field width"))
            fieldDef.SetWidth(width)
            dstLayer.CreateField(fieldDef)
            fieldList.append(fieldName)
        elif ftype==5:
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
    featureGeometryList= {"Unknown": 1, "POINT": 2, "LINESTRING": 3, "Polygon": 4, "MultiPoint": 5, "MultiLineString": 6, "MultiPolygon": 7,
            "GeometryCollection": 8, "CircularString": 9, "CompoundCurve": 10, "CurvePolygon": 11, "MultiCurve": 12, "MultiSurface": 13,
            "Curve ": 14,"Surface":15,"PolyhedralSurface":16,"TIN":17,"Triangle":18, "None":19, "LinearRing":20, "CircularStringZ":21,
                          "CompoundCurveZ":22, "CurvePolygonZ":23,"MultiCurveZ":24,"MultiSurfaceZ":25,"CurveZ":26,"SurfaceZ":27, "PolyhedralSurfaceZ":28,
                          "TINZ":29, "TriangleZ":30,"PointM":31,"LineStringM":32,"PolygonM":33,"MultiPointM":34,"MultiLineStringM":35, "MultiPolygonM":36,
                          "GeometryCollectionM":37,"CircularStringM":38,"CompoundCurveM":39,"CurvePolygonM":40,"MultiCurveM":41,"MultiSurfaceM":42,
                          "CurveM":43,"SurfaceM":44,"PolyhedralSurfaceM":45,"TINM":46,"TriangleM":47,"PointZM":48,"LineStringZM ":49,"PolygonZM":50,
                          "MultiPointZM ":51,"MultiLineStringZM":52,"MultiPolygonZM":53,"GeometryCollectionZM":54,"CircularStringZM":55,"CompoundCurveZM":56,
                          "CurvePolygonZM":57,"MultiCurveZM":58,"MultiSurfaceZM":59,"CurveZM":60,"SurfaceZM":61,"PolyhedralSurfaceZM":62,"TINZM":63,
                          "TriangleZM":64,"Point25D":65,"LineString25D":66,"Polygon25D":67,"MultiPoint25D":68,"MultiLineString25D":69,"MultiPolygon25D":70,
                          "GeometryCollection25D":71}
    print featureGeometryList
    a = "yes"
    j=0
    w = 1
    number = input("enter number of point")
    while a=="yes" or w<number:
        print number
        j = j + 1
        num=featureGeometryList[info[1]]
        if num==2:
            print "point geometry"
            point=info[0]
            w+=1
            print w
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(point)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("FieldID", j)
                feature.SetField("Longitude", point.GetX())
                feature.SetField("Latitude", point.GetY())
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        elif num==3:
            print "LineString geometry"
            line=info[0]
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(line)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i],value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        elif num==4:
            print "Polygon geometry"
            polygon=info[0]
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(polygon)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        elif num==5:
            print "Multipoint geometry"
            Multipoint=info[0]
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(Multipoint)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        elif num==6:
            print "MultiLineString geometry"
            MultiLineString=info[0]
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(MultiLineString)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()

        elif num==7:
            print "MultiPolygon geometry"
            MultiPolygon=info[0]
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(MultiPolygon)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()

        elif num==8:
            print "GeometryCollection geometry"
            GeometryCollection=info[0]
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(GeometryCollection)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        a=input("would you like to create more feature yes/no")
        if a=="yes":
            print "ok"
        else:
            break
    dstFile.Destroy()
    return dstPath

def featurelength(a):
    count=a.GetGeometryRef().GetPointCount()
    w=[]
    l=0
    for i in range(count):
        w.append(a.GetGeometryRef().GetPoint(i))
    for i in range(len(w)-1):
        l=l+haversine(w[i],w[i+1])
    return l

def generating_line_feature(a,b):
    return haversine(a,b),b

def making_crime_police_layer():
    print "MAKING CRIME POINT LAYER"
    point_1 = ogr.Geometry(ogr.wkbPoint)
    r= str(input("would u like to enter manually yes/no"))
    if r=="yes":
        point_1.AddPoint(float(input("ENTER LONGITUDE")), float(input("ENTER LATITUDE")))
    else:
        filePath=input("crime layer path")
        datasource = ogr.Open(filePath, 0)
        for feature in datasource.GetLayerByIndex(0):
            point_1.AddPoint(feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
    info_1 = [point_1, point_1.GetGeometryName()]
    crimepath=creating_shape_file_of_given_geometry(info_1)
    r=input("like to exit yes/no")
    if r=="no":
        print "MAKING POLICE POINT LAYER"
        point_2 = ogr.Geometry(ogr.wkbPoint)
        r = str(input("would u like to enter manually yes/no"))
        if r == "yes":
            point_2.AddPoint(float(input("ENTER LONGITUDE")), float(input("ENTER LATITUDE")))
        else:
            filePath = input("crime layer path")
            datasource = ogr.Open(filePath, 0)
            for feature in datasource.GetLayerByIndex(0):
                point_2.AddPoint(feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        info_2 = [point_2, point_2.GetGeometryName()]
        policepath=creating_shape_file_of_given_geometry(info_2)
        return crimepath,policepath
    else:
        return crimepath



def police():
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\POLICEPOINT.shp")
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.GetX(),geom.GetY()

def crime(crimepath):
    datasource = open_File(crimepath)
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.GetX(), geom.GetY()


def crimelink(crimepath,networkpath):
    crimedatasource = open_File(crimepath)
    crimelayer = crimedatasource.GetLayerByIndex(0)
    datasource = open_File(networkpath)
    layer = datasource.GetLayerByIndex(0)
    f=crimelayer.GetFeature(0)
    poly=f.GetGeometryRef().Buffer(0.00005)
    layer.SetSpatialFilter(poly)
    for feature in layer:
        print "the crime link is"+ str(feature.GetField("ID"))
        return feature.GetField("ID")

def remove_dead_ends(id):
    l=[]
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\CITYCENTERNODES.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    for feature in pointlayer:
        layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(0.00006))
        numFeatures = layer.GetFeatureCount()
        for fe in layer:
            if numFeatures == 1 and fe.GetField("ID") != id and fe.GetField("ID") not in l:
                l.append(fe.GetField("ID"))
    return l

def removing_higher_order_dead_end(l,id):
    x=True
    featureid=[]
    lila={}
    change={}
    change[0]=len(l)
    counter=0
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    for feature in layer:
        if feature.GetField("ID") not in l:
            featureid.append(feature.GetField("ID"))
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\CITYCENTERNODES.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    while x:
        counter+=1
        for feature in pointlayer:
            layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(0.00006))
            index = 0
            for fe in layer:
                if fe.GetField("ID") in featureid and fe.GetField("ID") not in l:
                    index+=1
                    lila[index]=fe.GetField("ID")
            if len(lila)==1 and lila[1]!=id:
                l.append(lila[1])
            lila.clear()
        change[counter]=len(l)
        if change[counter-1]==change[counter]:
            break
    return l



def farendcord(fcord,b):
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    feature = layer.GetFeature(b)
    count = feature.GetGeometryRef().GetPointCount()
    kdic={}
    line_last_length, lastcord = generating_line_feature(fcord,feature.GetGeometryRef().GetPoint(count - 1))
    line_start_length, startcord = generating_line_feature(fcord,feature.GetGeometryRef().GetPoint(0))
    d = max(line_last_length, line_start_length)
    kdic[line_start_length] = startcord
    kdic[line_last_length] = lastcord
    return kdic[d]

def feature_in_buffer(pfeat):
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(pfeat.GetGeometryRef().Buffer(0.00005))
    count=layer.GetFeatureCount()
    if count==1:
        print "NO FEATURE FOUND"
        return "NO FEATURE FOUND"



def roadlink(pfeat,fcord,q,r,id,l,roadId):
    kdic={}
    start_end_cord={}
    liladhar=[]
    fid = {}
    route = {}
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    layer.SetSpatialFilter(pfeat.GetGeometryRef().Buffer(0.00005))
    fcount=layer.GetFeatureCount()
    for feature in layer:
        if feature is None:
            return None,None,"NO FEATURE FOUND"
        if feature.GetField("ID") in l or feature.GetField("ID") in roadId :
            continue
        if feature.GetField("ID")==id:
            s = "THE END"
            return feature, (feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1]), s
        print feature.GetField("ID")
        a = featurelength(feature)
        print "feature length", a
        count = feature.GetGeometryRef().GetPointCount()
        line_last_length,lastcord=generating_line_feature(fcord,(feature.GetGeometryRef().GetPoint(count - 1)[0],feature.GetGeometryRef().GetPoint(count - 1)[1]))
        line_start_length,startcord=generating_line_feature(fcord,(feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1]))
        b = min(line_last_length, line_start_length)
        d = max(line_last_length, line_start_length)
        print "min and max dist from nearest cord", b,d
        kdic[line_start_length] = startcord
        kdic[line_last_length] = lastcord
        c, outcord = generating_line_feature((q,r),(kdic[d][0],kdic[d][1]))
        print "c",c
        print "a+b+c",a+b+c
        start_end_cord[a+b+c]=(kdic[d][0],kdic[d][1])
        fid[a+b+c] = feature.GetField("ID")
        print "fid", fid
        route[a+b+c] = feature
        liladhar.append(a+b+c)
    print "liladhar", liladhar
    final_route, firstcord, s=check(liladhar,q,r,route,id,l,start_end_cord)
    return final_route,firstcord,s



def check(liladhar,q,r,route,id,l,start_end_cord):
    tup=(q,r)
    s = "CONTINUE"
    x=True
    while x:
        if len(liladhar)==0:
            return None,(0,0),"NOT OK FINISH LIST"
        d=min(liladhar)
        print "min lilaadhar",d
        w=start_end_cord[d]
        f=route[d]
        firstcord, pfeat=firstcord_1(w[0],w[1])
        print "node at end of line feature",f.GetField("ID"),"=",pfeat.GetField("ID")
        r=nodecheck(firstcord[0],firstcord[1], id, l,tup[0],tup[1])
        print "node check",r
        if r=="ok":
            return f,(w[0],w[1]),s
        else:
            liladhar.remove(d)
            x=True

def nodecheck(x,y,id,l,q,r):
    li=[]
    s="ok"
    t="not ok"
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\CITYCENTERNODES.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    for feature in pointlayer:
        if feature.GetGeometryRef().GetX()==x and feature.GetGeometryRef().GetY()==y:
            print "node Id",feature.GetField("ID")
            layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(0.00006))
            for feat in layer:
                if feat.GetField("ID") not in l and feat.GetField("ID") not in li:
                    o=feat.GetField("ID")
                    print "road feature from ckeck node",feature.GetField("ID"),"is",o
                    if o ==id:
                        return s
                    num=mindist(o,q,r,x,y)
                    if num is not None:
                        print "id of road feature toward crime location",num
                        li.append(num)
    if len(li)!=0:
        return s
    else:
        return t

def mindist(b,q,r,x,y):
    dictionary={}
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    a = layer.GetFeature(b)
    count = a.GetGeometryRef().GetPointCount()
    lengthend, tupcordend = generating_line_feature((q, r), (a.GetGeometryRef().GetPoint(count - 1)[0], a.GetGeometryRef().GetPoint(count - 1)[1]))
    dictionary[lengthend] = tupcordend
    lengthstart, tupcordstart = generating_line_feature((q, r),(a.GetGeometryRef().GetPoint(0)[0], a.GetGeometryRef().GetPoint(0)[1]))
    dictionary[lengthstart] = tupcordstart
    print dictionary
    w=farendcord((x,y),b)
    print w
    d=min(lengthend,lengthstart)
    if dictionary[d]==(w[0],w[1]):
        print "min dist function give next road link as","=",b
        return b
    else:
        return None

def route(finalroute,i):
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    folderLocation, folderName = creating_directory_short_path(i)
    name = "NEWSHORTROUTE%d"%i
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer", spatialReference)
    out_row = ogr.Feature(dstLayer.GetLayerDefn())
    multilinestring = ogr.Geometry(ogr.wkbMultiLineString)
    for k in range(len(finalroute)):
        multilinestring.AddGeometry(finalroute[k].GetGeometryRef())
    poly = {}
    for i in range(len(finalroute)):
        poly[i] = multilinestring.GetGeometryRef(i)
    line = {}
    line[0] = poly[0]
    for i in range(len(finalroute) - 1):
        line[i + 1] = poly[i + 1].Union(line[i])
    out_row.SetGeometry(line[len(finalroute) - 1])
    dstLayer.CreateFeature(out_row)
    dstFile.Destroy()


def firstcord_1(c,d):
    cord = {}
    id={}
    linelength=[]
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\CITYCENTERNODES.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    pointfeature = {}
    for feature in pointlayer:
        a=(feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        b=(c, d)
        l=haversine(a,b)
        linelength.append(l)
        cord[l] = (feature.GetGeometryRef().GetX(),feature.GetGeometryRef().GetY())
        id [l]=feature.GetField("ID")
        pointfeature[l] = feature
    a=min(linelength)
    firstcord = cord[a]
    pfeat = pointfeature[a]
    pointfeature.clear()
    print id[a]
    return firstcord,pfeat

def nearest_policia(path,crimepath):
    d={}
    patht={}
    l=[]
    crimedatasource = open_File(crimepath)
    clayer = crimedatasource.GetLayerByIndex(0)
    cfeat = clayer.GetFeature(0)
    for i in range(len(path)):
        datasource = open_File(path[i])
        layer = datasource.GetLayerByIndex(0)
        feat=layer.GetFeature(0)
        pointA=(feat.GetGeometryRef().GetX(),feat.GetGeometryRef().GetY())
        pointB=(cfeat.GetGeometryRef().GetX(),cfeat.GetGeometryRef().GetY())
        length=haversine(pointA,pointB)
        patht[length]=str(path[i])
        d[length]=feat
        l.append(length)
    print patht[min(l)]
    return d[min(l)].GetGeometryRef().GetX(),d[min(l)].GetGeometryRef().GetY()


def a(flink,(c,d)):
    l={}
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    a = layer.GetFeature(flink)
    count=a.GetGeometryRef().GetPointCount()
    w=((a.GetGeometryRef().GetPoint(count-1)[0],a.GetGeometryRef().GetPoint(count-1)[1]),(a.GetGeometryRef().GetPoint(0)[0],a.GetGeometryRef().GetPoint(0)[1]))
    l[haversine(w[0],(c,d))] = w[0]
    l[haversine(w[1],(c,d))] = w[1]
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\CITYCENTERNODES.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    for feature in pointlayer:
        if (feature.GetGeometryRef().GetX(),feature.GetGeometryRef().GetY())==w[0]:
            print feature.GetField("ID")
        elif (feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY()) == w[1]:
            print feature.GetField("ID")
    xmin=l[min(haversine(w[0],(c,d)),haversine(w[1],(c,d)))]
    ymax=l[max(haversine(w[0],(c,d)),haversine(w[1],(c,d)))]
    print xmin,ymax
    return xmin,ymax


def shortest_path_forward(crimepath):
    cordlist=[]
    finalroute = []
    roadId = []
    path=["C:\Users\Hp\Desktop\pol\olice\POLICEPOINT1.shp","C:\Users\Hp\Desktop\pol\olice\POLICEPOINT2.shp","C:\Users\Hp\Desktop\pol\olice\POLICEPOINT3.shp","C:\Users\Hp\Desktop\pol\DATA\POLICEPOINT.shp"]
    c,d = nearest_policia(path,crimepath)
    #c,d=police()
    q,r = crime(crimepath)
    id=crimelink(crimepath,networkpath="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    l = remove_dead_ends(id)
    l=removing_higher_order_dead_end(l,id)
    firstcord, pfeat=firstcord_1(c,d)
    cordlist.append(firstcord)
    x=True
    while x:
        final_route,firstcord,s=roadlink(pfeat,firstcord,float(q),float(r),id,l,roadId)
        if  s=="NOT OK FINISH LIST":
            print s
            break
        firstcord, pfeat = firstcord_1(firstcord[0],firstcord[1])
        cordlist.append(firstcord)
        finalroute.append(final_route)
        roadId.append(final_route.GetField("ID"))
        #print roadId
        if s=="THE END":
            x=False
            print "LOCATION REACHED"
    print roadId
    return roadId

def shortest_path_reverse(crimepath):
    reversecordlist=[]
    reversefinalroute=[]
    q,r=crime(crimepath)
    flink=crimelink(crimepath, networkpath="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    reverseroadId=[flink]
    lo=remove_dead_ends(flink)
    l=removing_higher_order_dead_end(lo,flink)
    path = ["C:\Users\Hp\Desktop\pol\olice\POLICEPOINT1.shp", "C:\Users\Hp\Desktop\pol\olice\POLICEPOINT2.shp",
            "C:\Users\Hp\Desktop\pol\olice\POLICEPOINT3.shp", "C:\Users\Hp\Desktop\pol\DATA\POLICEPOINT.shp"]
    c, d = nearest_policia(path,crimepath)
    fcord,ffeat=firstcord_1(c,d)
    xmin,ymax=a(flink,(c,d))
    m,n=firstcord_1(xmin[0],xmin[1])
    s = feature_in_buffer(n)
    if s=="NO FEATURE FOUND":
        m, n = firstcord_1(ymax[0], ymax[1])
    x = True
    while x:
        final_route, firstcord, s = roadlink(n, m, fcord[0], fcord[1], id, l, reverseroadId)
        if  s=="NOT OK FINISH LIST":
            print s
            break
        m, n = firstcord_1(firstcord[0], firstcord[1])
        reversecordlist.append(fcord)
        reversefinalroute.append(final_route)
        reverseroadId.append(final_route.GetField("ID"))
    print reverseroadId
    return reverseroadId

def commonid(forwardroute,reverseroute):
    l=[]
    x=0
    for element in range(len(forwardroute)):
        if x==0:
            if forwardroute[element] in reverseroute:
                for m,n in enumerate(forwardroute):
                    if n == forwardroute[element]:
                        l.append(m)
                        print m, forwardroute[element]
                for i, j in enumerate(reverseroute):
                    if j == forwardroute[element]:
                        l.append(i)
                        print i, forwardroute[element]
                x+=1
        else:
            break
    print  l
    return l


def shortroute(i,crimepath):
    print crimepath
    final_route=[]
    final_route_feature=[]
    forwardroute=shortest_path_forward(crimepath)
    reverseroute=shortest_path_reverse(crimepath)
    l=commonid(forwardroute, reverseroute)
    for element in range(len(forwardroute)):
        if element<l[0]:
            final_route.append(forwardroute[element])
    for element in range(len(reverseroute)):
        if element<(l[1]+1):
            final_route.append(reverseroute[l[1]-element])
    print final_route
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\DATA\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    for element in range(len(final_route)):
        final_route_feature.append(layer.GetFeature(final_route[element]))
    route(final_route_feature,i)

os.chdir("C:\Users\Hp\Desktop\pol\CRIMEDATA")
file = glob.glob('*.shp')
for i in range(len(file)):
    shortroute(i+1,crimepath=file[i])