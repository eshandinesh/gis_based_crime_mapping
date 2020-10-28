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
import xlrd
from osgeo import ogr
import operator
import shapely

def open_File(path):
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

def creating_shape_file_of_given_geometry (info):
    reply = input ("would you like geographic coordinate system or projected coordinate system as spatial reference ")
    if reply =="geographic coordinate system":
        geographicCoordinateSystem = ["WGS84", "WGS72", "NAD27", "NAD83", "EPSG:4326", "EPSG:4322", "EPSG:4267", "EPSG:4269"]
        listGcs = input("whether want to see Geographic Coordinate System list answer in yes/no")
        if listGcs == "yes":
            print "\n".join(geographicCoordinateSystem)
        gcs = input("Enter Geographic Coordinate System's name: as shown in the list")
        spatialReference = osgeo.osr.SpatialReference()
        spatialReference.SetWellKnownGeogCS("%s" %gcs)
    elif reply =="projected coordinate system" :
        projectionCordinateSystem = []
        x = 0
        y = 59
        while x <= y:
            x = x + 1
            projectionCordinateSystem.append(x)
        reply = input("whether want to see projection System list answer in yes/no")
        if reply == "yes":
            print projectionCordinateSystem
        pcs = input("Enter projection Cordinate System's zone number:")
        hemisphere = input("Enter True for north hemisphere and False for southern hemisphere")
        spatialReference = osr.SpatialReference()
        spatialReference.SetUTM("%d,%s" % (pcs, hemisphere))
	print spatialReference
    count, list = number_of_available_drivers()
    driverName = entered_driver_availiblity(count, list)
    driver = osgeo.ogr.GetDriverByName("%s" % driverName)
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

def police():
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\olice\Police.shp")
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        print "feature number %d" % featureIndex
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.ExportToWkt(), geom.GetX(),geom.GetY(),layer

def crime():
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\Crimepoint\Crimepoint.shp")
    numLayers = num_of_layers_in_file(datasource)
    layer = datasource.GetLayerByIndex(0)
    numFeatures = num_of_features_in_layer(datasource, numLayers)
    for featureIndex in range(numFeatures):
        print "feature number %d" % featureIndex
        feature = layer.GetFeature(featureIndex)
        geom = feature.GetGeometryRef()
        return geom.ExportToWkt(), geom.GetX(), geom.GetY(),layer



def roadlink(fcord,q,r):
    d1 = {}
    l1 = {}
    length = {}
    route_1 = {}
    featureindex = 0
    route = {}
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\Road\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    for feature in layer:
        a = feature.GetGeometryRef().Length()
        featureindex += 1
        count = feature.GetGeometryRef().GetPointCount()
        route[featureindex] = feature
        line_last = ogr.Geometry(ogr.wkbLineString)
        line_last.AddPoint(feature.GetGeometryRef().GetPoint(count - 1)[0],
                           feature.GetGeometryRef().GetPoint(count - 1)[1])
        line_last.AddPoint(fcord[0], fcord[1])
        line_start = ogr.Geometry(ogr.wkbLineString)
        line_start.AddPoint(feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1])
        line_start.AddPoint(fcord[0], fcord[1])
        b = min(line_last.Length(), line_start.Length())
        del line_start, line_last
        line_last = ogr.Geometry(ogr.wkbLineString)
        line_last.AddPoint(feature.GetGeometryRef().GetPoint(count - 1)[0],
                           feature.GetGeometryRef().GetPoint(count - 1)[1])
        line_last.AddPoint(q, r)
        line_start = ogr.Geometry(ogr.wkbLineString)
        line_start.AddPoint(feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1])
        line_start.AddPoint(q, r)
        c = min(line_last.Length(), line_start.Length())
        length[featureindex] = (a + b + c)
    route_1[min(length.keys(), key=(lambda k: length[k]))] = length[min(length.keys(), key=(lambda k: length[k]))]
    f=route[min(length.keys(), key=(lambda k: length[k]))]
    count=f.GetGeometryRef().GetPointCount()
    w=(f.GetGeometryRef().GetPoint(0)[0],f.GetGeometryRef().GetPoint(0)[1])
    print w
    e=(f.GetGeometryRef().GetPoint(count - 1)[0],f.GetGeometryRef().GetPoint(count - 1)[1])
    print e
    line_last = ogr.Geometry(ogr.wkbLineString)
    line_last.AddPoint(w[0],w[1])
    line_last.AddPoint(q, r)
    d1[line_last.Length()]=w
    print d1
    line_start = ogr.Geometry(ogr.wkbLineString)
    line_start.AddPoint(e[0],e[1])
    line_start.AddPoint(q, r)
    d1[line_start.Length()] = e
    print d1
    print f,d1[min(line_last.Length(),line_start.Length())]
    return f,d1[min(line_last.Length(),line_start.Length())]


def route(finalroute):
    spatialReference = None
    reply = input("would you like geographic coordinate system or projected coordinate system as spatial reference ")
    if reply == "geographic coordinate system":
        geographicCoordinateSystem = ["WGS84", "WGS72", "NAD27", "NAD83", "EPSG:4326", "EPSG:4322", "EPSG:4267",
                                      "EPSG:4269"]
        listGcs = input("whether want to see Geographic Coordinate System list answer in yes/no")
        if listGcs == "yes":
            print "\n".join(geographicCoordinateSystem)
        gcs = input("Enter Geographic Coordinate System's name: as shown in the list")
        spatialReference = osgeo.osr.SpatialReference()
        spatialReference.SetWellKnownGeogCS("%s" % gcs)
    elif reply == "projected coordinate system":
        projectionCordinateSystem = []
        x = 0
        y = 59
        while x <= y:
            x = x + 1
            projectionCordinateSystem.append(x)
        reply = input("whether want to see projection System list answer in yes/no")
        if reply == "yes":
            print projectionCordinateSystem
        pcs = input("Enter projection Cordinate System's zone number:")
        hemisphere = input("Enter True for north hemisphere and False for southern hemisphere")
        spatialReference = osr.SpatialReference()
        spatialReference.SetUTM("%d,%s" % (pcs, hemisphere))
    count, list = number_of_available_drivers()
    driverName = entered_driver_availiblity(count, list)
    driver = osgeo.ogr.GetDriverByName("%s" % driverName)
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
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



def remove_dead_ends(q,r):
    index=0
    l=[]
    d={}
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\NODES\P.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\Road\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    for feature in pointlayer:
        line= ogr.Geometry(ogr.wkbLineString)
        line.AddPoint(feature.GetGeometryRef().GetX(),feature.GetGeometryRef().GetY())
        line.AddPoint(q,r)
        layer.SetSpatialFilter(feature.GetGeometryRef().Buffer(0.0001))
        numFeatures = layer.GetFeatureCount()
        if numFeatures ==1 and line.Length()>0.0005:
            for feature in layer:
                print feature.GetField("ID")
                l.append(feature.GetField("ID"))
    print l
    return l


def check():
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\Road\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    l = remove_dead_ends()
    for feature in layer:
        if feature.GetField("ID") in l:
            print "yes"
        else:
            print feature.GetField("ID")



def shortest_path():
    g, c, d, policelayer = police()
    p, q, r, crimelayer = crime()

    finalroute = []
    index=0
    cord={}
    pointdatasource = open_File(path="C:\Users\Hp\Desktop\pol\NODES\P.shp")
    pointlayer = pointdatasource.GetLayerByIndex(0)
    first_length={}
    for feature in pointlayer:
        index+=1
        line = ogr.Geometry(ogr.wkbLineString)
        line.AddPoint(feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        line.AddPoint(c,d)
        cord[index]=(feature.GetGeometryRef().GetX(), feature.GetGeometryRef().GetY())
        first_length[index]=line.Length()
    firstcord=cord[min(first_length.keys(), key=(lambda k: first_length[k]))]
    print cord, "\n", first_length,"\n", firstcord,"\n",first_length[min(first_length.keys(), key=(lambda k: first_length[k]))]
    first_length.clear()
    datasource = open_File(path="C:\Users\Hp\Desktop\pol\Road\ROADCITYCENTER.shp")
    layer = datasource.GetLayerByIndex(0)
    route={}
    featureindex=0
    for feature in layer:
        a = feature.GetGeometryRef().Length()
        featureindex += 1
        count = feature.GetGeometryRef().GetPointCount()
        route[featureindex] = feature
        line_last = ogr.Geometry(ogr.wkbLineString)
        line_last.AddPoint(feature.GetGeometryRef().GetPoint(count - 1)[0],
                           feature.GetGeometryRef().GetPoint(count - 1)[1])
        line_last.AddPoint(firstcord[0], firstcord[1])
        line_start = ogr.Geometry(ogr.wkbLineString)
        line_start.AddPoint(feature.GetGeometryRef().GetPoint(0)[0], feature.GetGeometryRef().GetPoint(0)[1])
        line_start.AddPoint(firstcord[0], firstcord[1])
        b = min(line_last.Length(), line_start.Length())
        print firstcord,line_last.Length(), line_start.Length(),b,featureindex


