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





def open_File_1(path):
    if path==None:
        filePath = str(input("file path"))
    else:
        filePath=path
    print ("Entered File Path is %s" % filePath)
    datasource = ogr.Open(filePath,True)
    return datasource

def get_geometry(path):
    datasource = open_File_1(path)
    numLayers = num_of_layers_in_file(datasource)
    geom=[]
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            print (feature)
            geometry = feature.GetGeometryRef()
            name = geometry.GetGeometryName()
            geom.append(geometry)



def xls (filePath):
    with open(filePath, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        coord=[]
        for (row) in(spamreader):
            #a=row[0].split(',')
            #print a[1],a[2]
            ', '.join(row)
            a = row[0].split(',')
            tuple=(a[1], a[2])
            coord.append(tuple)
        return coord

def creating_directory():
    folderName = input("Enter Folder Name")
    folderPath = input("Where you want to save folder ")
    path = folderPath + '\\' + folderName
    print (path)
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
        print ("\n".join(formatsList))
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

def create_point_shp():
    point = ogr.Geometry(ogr.wkbPoint)
    point.ExportToWkt()
    return point



def create_a_point(w,filePath) :
    #eply = input("want to add point using csv yes/no\n")
    #f reply=='yes':
    coord=xls(filePath)
    long= (coord[w][1])
    lat=coord[w][0]
   #else:
       #long = float(input("ENTER LONGITUDE"))
       #lat = float(input("ENTER LATITUDE"))
    point = ogr.Geometry(ogr.wkbPoint)
    point.AddPoint(float(long),float(lat))
    tryAgain ="yes"
   #while tryAgain == "yes":
       #takePrint = input("would you like to see added point")
       #if takePrint == "yes"# :

    point.ExportToWkt()
           # break
        #elif takePrint != "yes":
         #   print "Your reply is inappropriate"
        #exit = input("Do You Want to Exit yes\ no")
        #if exit == "yes":
         #   break
    return point



def create_a_linestring():
    line = ogr.Geometry(ogr.wkbLineString)
    tryAgain = "yes"
    reply = input("want to add point manually yes/no\n")
    while reply == "yes":
        long = float(input("ENTER LONGITUDE\n"))
        lat = float(input("ENTER LATITUDE \n"))
        line.AddPoint(long,lat)
        reply = input("want to add more point yes/no \n")
        if reply=="yes":
            print ("ok")
        elif reply=="no" :
            break
    while reply=="no":

        datasource = open_File_1(path=None)
        numLayers = num_of_layers_in_file(datasource)
        for layerIndex in range(numLayers):
            layer = datasource.GetLayerByIndex(layerIndex)
            numFeatures = num_of_features_in_layer(datasource, numLayers)
            for featureIndex in range(numFeatures):
                print ("feature number %d" % featureIndex)
                feature = layer.GetFeature(featureIndex)
                geometry = feature.GetGeometryRef()
                name = geometry.GetGeometryName()
                if name == "LINESTRING":
                    line = ogr.Geometry(ogr.wkbLineString)
                    for i in range(0, geometry.GetPointCount()):
                        pt = geometry.GetPoint(i)
                        long = pt[0]
                        lat = pt[1]
                        print (pt, lat, long)
                        line.AddPoint(long, lat)
        r = str(input("like to exit yes/no"))
        if r == "yes":
            break
    return line

def create_a_polygon():
    # Create ring
    tryAgain = "yes"
    poly = ogr.Geometry(ogr.wkbPolygon)
    ring = ogr.Geometry(ogr.wkbLinearRing)
    reply = input("want to add point in ring of polygon yes/no\n")
    while reply == "yes":
        long = float(input("ENTER LONGITUDE\n"))
        lat = float(input("ENTER LATITUDE \n"))
        ring.AddPoint(long,lat)
        reply = input("want to add more point yes/no \n")
        if reply == "yes":
            print ("ok, then add why you are asking to me")
        elif reply == "no":
            print ("thanks for not adding any more points")
            break
    poly.AddGeometry(ring)
    while tryAgain=="yes":
        takePrint=input("would you like to see created polygon")
        if takePrint=="yes":
            print (poly.ExportToWkt())
            break
        elif takePrint!="yes":
            print ("Your reply is inappropriate")
        exit=input("Do You Want to Exit yes\ no")
        if exit=="yes":
            break
    return poly






def create_polygon_with_hole():
    # Create polygon
    poly = ogr.Geometry(ogr.wkbPolygon)
    tryAgain = "yes"
    # Create outer ring
    reply = input("want to create outer ring and start adding point in it yes/no\n")
    outRing = ogr.Geometry(ogr.wkbLinearRing)
    while reply == "yes":
        long = float(input("ENTER LONGITUDE\n"))
        lat = float(input("ENTER LATITUDE \n"))
        outRing.AddPoint(long, lat)
        reply = input("want to add more point yes/no \n")
        if reply == "yes":
            print ("ok, then add why you are asking to me")
        elif reply == "no":
            print ("thanks for not adding any more points")
            break
    poly.AddGeometry(outRing)
    reply = input("want to create inner ring yes/no\n")
    more = "yes"
    while more == "yes":
        innerRing = ogr.Geometry(ogr.wkbLinearRing)
        while reply == "yes":
            long = float(input("ENTER LONGITUDE\n"))
            lat = float(input("ENTER LATITUDE \n"))
            innerRing.AddPoint(long, lat)
            reply = input("want to add more point yes/no \n")
            if reply == "yes":
                print ("ok, then add why you are asking to me")
            elif reply == "no":
                print ("thanks for not adding any more points")
                break
        poly.AddGeometry(innerRing)
        more = input("want to create more inner ring yes/no\n")
        if more == "yes":
            reply = "yes"
            print ("ok, then create why you are asking to me")
        elif reply == "no":
            print ("thanks for not creating any more inner rings")
            break
    while tryAgain=="yes":
        takePrint=input("would you like to see created polygon")
        if takePrint=="yes":
            print (poly.ExportToWkt())
            break
        elif takePrint!="yes":
            print ("Your reply is inappropriate")
        exit=input("Do You Want to Exit yes\ no")
        if exit=="yes":
            break
    return poly



def create_multipoint():
    multipoint = ogr.Geometry(ogr.wkbMultiPoint)
    tryAgain = "yes"
    reply = input("want to add point yes/no\n")
    point = ogr.Geometry(ogr.wkbPoint)
    while reply == "yes":
        long = float(input("ENTER LONGITUDE\n"))
        lat = float(input("ENTER LATITUDE \n"))
        point.AddPoint(long, lat)
        reply = input("want to add more point yes/no \n")
        if reply == "yes":
            print ("ok")
        elif reply == "no":
            break
        multipoint.AddGeometry(point)
    while tryAgain == "yes":
        takePrint = input("would you like to see created multipoint")
        if takePrint == "yes":
            print (multipoint.ExportToWkt())
            break
        elif takePrint != "yes":
            print ("Your reply is inappropriate")
        exit = input("Do You Want to Exit yes\ no")
        if exit == "yes":
            break
    return multipoint



def multiLineString():
    multiline = ogr.Geometry(ogr.wkbMultiLineString)
    tryAgain = "yes"
    reply = input("Want to start adding point in a Line String yes/no\n")

    more = "yes"
    while more == "yes":
        line = ogr.Geometry(ogr.wkbLineString)
        while reply == "yes":
            long = float(input("ENTER LONGITUDE\n"))
            lat = float(input("ENTER LATITUDE \n"))
            line.AddPoint(long, lat)
            reply = input("want to add more point yes/no \n")
            if reply == "yes":
                print ("ok")
            elif reply == "no":
                break
        multiline.AddGeometry(line)
        more = input("want to create more line string yes/no\n")
        if more == "yes":
            reply = "yes"
            print ("ok, then create why you are asking to me")
        elif reply == "no":
            print ("thanks for not creating any more inner rings")
            break
    while tryAgain == "yes":
        takePrint = input("would you like to see created multiline ")
        if takePrint == "yes":
            print (multiline.ExportToWkt())
            break
        elif takePrint != "yes":
            print ("Your reply is inappropriate")
        exit = input("Do You Want to Exit yes\ no")
        if exit == "yes":
            break
    return multiline


def create_multipolygon ():
    multipolygon = ogr.Geometry(ogr.wkbMultiPolygon)
    tryAgain = "yes"
    reply = input("want to create polygon yes/no\n")
    morePolygon = "yes"
    moreRing = "yes"
    while morePolygon=="yes":
        poly = ogr.Geometry(ogr.wkbPolygon)
        while moreRing == "yes":
            ring = ogr.Geometry(ogr.wkbLinearRing)
            while reply == "yes":
                long = float(input("ENTER LONGITUDE\n"))
                lat = float(input("ENTER LATITUDE \n"))
                ring.AddPoint(long, lat)
                reply = input("want to add more point yes/no \n")
                if reply == "yes":
                    print ("ok, then add why you are asking to me")
                elif reply == "no":
                    print ("thanks for not adding any more points")
                    break
            poly.AddGeometry(ring)
            moreRing = input("want to create more ring yes/no\n")
            if moreRing == "yes":
                reply = "yes"
                print ("ok, then create why you are asking to me")
            elif reply == "no":
                print ("thanks for not creating any more ring")
                break
        multipolygon.AddGeometry(poly)
        morePolygon = input("want to create more polygon yes/no\n")
        if morePolygon == "yes":
            reply = "yes"
            moreRing="yes"
            print ("ok, then create why you are asking to me")
        elif reply == "no":
            print ("thanks for not creating any more polygon")
            break
    while tryAgain == "yes":
        takePrint = input("would you like to see created multiple polygon")
        if takePrint == "yes":
            print (multipolygon.ExportToWkt())
            break
        elif takePrint != "yes":
            print ("Your reply is inappropriate")
        exit = input("Do You Want to Exit yes\ no")
        if exit == "yes":
            break
    return multipolygon


def create_geometryCollection ():
    # Create a geometry collection
    geomcol = ogr.Geometry(ogr.wkbGeometryCollection)
    tryAgain = "yes"
    anotherGeometry="yes"
    while anotherGeometry=="yes":
        reply= int(input ("what type of geometry would you like to add in this Geometry Collection (Type index number corresponding to the geometry):\n1:POINT\n2:LINE\n3:POLYGON\n4:MULTIPOINT\n5:MULTILINESTRING\n6:MULTIPOLYGON\n7:POLYGON WITH HOLES"))
        if reply==1:
            point=create_a_point()
            geomcol.AddGeometry(point)
        elif reply==2:
            lineString = create_a_linestring()
            geomcol.AddGeometry(lineString)
        elif reply==3:
            polygon = create_a_polygon()
            geomcol.AddGeometry(polygon)
        elif reply==4:
            multipoint = create_multipoint()
            geomcol.AddGeometry(multipoint)
        elif reply==5:
            multiline = multiLineString()
            geomcol.AddGeometry(multiline)
        elif reply==6:
            multipolygon = create_multipolygon ()
            geomcol.AddGeometry(multipolygon)
        elif reply==7:
            polygonWithHoles = create_polygon_with_hole()
            geomcol.AddGeometry(polygonWithHoles)
        anotherGeometry=input("like to add another geometry yes/no")
        if anotherGeometry!="yes":
            break
    while tryAgain == "yes":
        takePrint = input("would you like to see created Geometry Collection")
        if takePrint == "yes":
            print (geomcol.ExportToWkt())
            break
        elif takePrint != "yes":
            print ("Your reply is inappropriate")
        exit = input("Do You Want to Exit yes\ no")
        if exit == "yes":
            break
    return geomcol

def create_layer_from_base():
    datasource=open_File_1(path=None)
    layer = datasource.GetLayerByIndex(0)
    feature = layer.GetFeature(0)
    count, list = number_of_available_drivers()
    driverName = entered_driver_availiblity(count, list)
    driver = osgeo.ogr.GetDriverByName("%s" % driverName)
    folderLocation, folderName = creating_directory()
    name = input("enter shape file name")
    dstPath = os.path.join(folderLocation, "%s.shp" % name)
    dstFile = driver.CreateDataSource("%s" % dstPath)
    dstLayer = dstFile.CreateLayer("resulting layer",layer.GetSpatialRef(),ogr.wkbLineString)
    out_row = ogr.Feature(dstLayer.GetLayerDefn())
    del dstFile
    return dstPath

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

def creating_shape_file_of_given_geometry ():
    spatialReference=None
    reply = input ("would you like geographic coordinate system or projected coordinate system as spatial reference ")
    if reply =="geographic coordinate system":
        geographicCoordinateSystem = ["WGS84", "WGS72", "NAD27", "NAD83", "EPSG:4326", "EPSG:4322", "EPSG:4267",
                                      "EPSG:4269"]
        listGcs = input("whether want to see Geographic Coordinate System list answer in yes/no")
        if listGcs == "yes":
            print ("\n".join(geographicCoordinateSystem))
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
            print (projectionCordinateSystem)
        pcs = input("Enter projection Cordinate System's zone number:")
        hemisphere = input("Enter True for north hemisphere and False for southern hemisphere")
        spatialReference = osr.SpatialReference()
        spatialReference.SetUTM("%d,%s" % (pcs, hemisphere))
	print (spatialReference)
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
    print (list)
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
    featureGeometryList= {"Unknown": 1, 'POINT': 2, "LINESTRING": 3, "Polygon": 4, "MultiPoint": 5, "MultiLineString": 6, "MultiPolygon": 7,
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
    print (featureGeometryList)
    a = "yes"
    j=0
    w = 1
    number = input("enter number of point")
    while a=="yes" or w<number:
        print number
        j = j + 1
        num=int(input("Enter number corresponding to the geometry you want to assign to feature"))
        if num==2:
            print "point geometry"
            point=create_a_point(w)
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
            line=create_a_linestring()
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(line)
            for i in range(len(fieldList)):
                print fieldList[i]
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i],value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        elif num==4:
            print ("Polygon geometry")
            polygon=create_a_polygon()
            feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
            feature.SetGeometry(polygon)
            for i in range(len(fieldList)):
                print (fieldList[i])
                value=input("Enter field Value")
                feature.SetField("%s"% fieldList[i], value)
            dstLayer.CreateFeature(feature)
            feature.Destroy()
        elif num==5:
            print "Multipoint geometry"
            Multipoint=create_multipoint()
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
            MultiLineString=multiLineString()
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
            MultiPolygon=create_multipolygon ()
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
            GeometryCollection=create_geometryCollection ()
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


def csvtoshp ():
    filePath = str(input("Enter path of your CSV file"))
    reply = input("would you like geographic coordinate system or projected coordinate system as spatial reference ")
    if reply == "geographic coordinate system":
        geographicCoordinateSystem = ["WGS84", "WGS72", "NAD27", "NAD83", "EPSG:4326", "EPSG:4322", "EPSG:4267",
                                      "EPSG:4269"]
        listGcs = input("whether want to see Geographic Coordinate System list answer in yes/no")
        if listGcs == "yes":
            print ("\n".join(geographicCoordinateSystem))
        gcs = input("Enter Geographic Coordinate System's name: as shown in the list")
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    #count, list = number_of_available_drivers()
    #driverName = entered_driver_availiblity(count, list)
    #driver = osgeo.ogr.GetDriverByName("%s" % driverName)#ESRI Shapefile
    driver = osgeo.ogr.GetDriverByName("ESRI Shapefile")
    print ("Creating Directory For ShapeFile")
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
        point = create_a_point(w,filePath)
        print w
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        for i in range(len(fieldList)):
            #print fieldList[i]
            #value = input("Enter field Value")
            feature.SetField("FieldID", j)
            feature.SetField("Longitude", point.GetX())
            feature.SetField("Latitude", point.GetY())
            feature.SetField("%s" % fieldList[i], 1)
            dstLayer.CreateFeature(feature)
            feature.Destroy()


def creating_an_empty_shape_file():
    spatialReference = osgeo.osr.SpatialReference()
    spatialReference.SetWellKnownGeogCS("WGS84")
    # count, list = number_of_available_drivers()
    # driverName = entered_driver_availiblity(count, list)
    # driver = osgeo.ogr.GetDriverByName("%s" % driverName)#ESRI Shapefile
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

    featureGeometryList = {"Unknown": 1, "Point": 2, "LineString": 3, "Polygon": 4, "MultiPoint": 5,
                           "MultiLineString": 6, "MultiPolygon": 7,
                           "GeometryCollection": 8, "CircularString": 9, "CompoundCurve": 10, "CurvePolygon": 11,
                           "MultiCurve": 12, "MultiSurface": 13,
                           "Curve ": 14, "Surface": 15, "PolyhedralSurface": 16, "TIN": 17, "Triangle": 18, "None": 19,
                           "LinearRing": 20, "CircularStringZ": 21,
                           "CompoundCurveZ": 22, "CurvePolygonZ": 23, "MultiCurveZ": 24, "MultiSurfaceZ": 25,
                           "CurveZ": 26, "SurfaceZ": 27, "PolyhedralSurfaceZ": 28,
                           "TINZ": 29, "TriangleZ": 30, "PointM": 31, "LineStringM": 32, "PolygonM": 33,
                           "MultiPointM": 34, "MultiLineStringM": 35, "MultiPolygonM": 36,
                           "GeometryCollectionM": 37, "CircularStringM": 38, "CompoundCurveM": 39, "CurvePolygonM": 40,
                           "MultiCurveM": 41, "MultiSurfaceM": 42,
                           "CurveM": 43, "SurfaceM": 44, "PolyhedralSurfaceM": 45, "TINM": 46, "TriangleM": 47,
                           "PointZM": 48, "LineStringZM ": 49, "PolygonZM": 50,
                           "MultiPointZM ": 51, "MultiLineStringZM": 52, "MultiPolygonZM": 53,
                           "GeometryCollectionZM": 54, "CircularStringZM": 55, "CompoundCurveZM": 56,
                           "CurvePolygonZM": 57, "MultiCurveZM": 58, "MultiSurfaceZM": 59, "CurveZM": 60,
                           "SurfaceZM": 61, "PolyhedralSurfaceZM": 62, "TINZM": 63,
                           "TriangleZM": 64, "Point25D": 65, "LineString25D": 66, "Polygon25D": 67, "MultiPoint25D": 68,
                           "MultiLineString25D": 69, "MultiPolygon25D": 70,
                           "GeometryCollection25D": 71}
    print featureGeometryList
    num = int(input("Enter number corresponding to the geometry you want to assign to feature"))
    if num == 2:
        print "point geometry"
        point = ogr.Geometry(ogr.wkbPoint)
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(point)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    elif num == 3:
        print "LineString geometry"
        line = ogr.Geometry(ogr.wkbLineString)
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(line)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    elif num == 4:
        print "Polygon geometry"
        poly = ogr.Geometry(ogr.wkbPolygon)
        ring = ogr.Geometry(ogr.wkbLinearRing)
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        poly.AddGeometry(ring)
        feature.SetGeometry(poly)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    elif num == 5:
        print "Multipoint geometry"
        Multipoint = create_multipoint()
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(Multipoint)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    elif num == 6:
        print "MultiLineString geometry"
        MultiLineString = multiLineString()
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(MultiLineString)
        dstLayer.CreateFeature(feature)
        feature.Destroy()

    elif num == 7:
        print "MultiPolygon geometry"
        MultiPolygon = create_multipolygon()
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(MultiPolygon)
        dstLayer.CreateFeature(feature)
        feature.Destroy()

    elif num == 8:
        print "GeometryCollection geometry"
        GeometryCollection = create_geometryCollection()
        feature = osgeo.ogr.Feature(dstLayer.GetLayerDefn())
        feature.SetGeometry(GeometryCollection)
        dstLayer.CreateFeature(feature)
        feature.Destroy()
    dstFile.Destroy()


def analyzeGeometry(geometry, indent=0):
    s = []
    s.append(" " * indent)
    s.append(geometry.GetGeometryName())
    if geometry.GetPointCount() > 0:
        s.append(" with %d data points" % geometry.GetPointCount())
    print "number of geometry element %d" % geometry.GetGeometryCount()
    if geometry.GetGeometryCount() > 0:
        s.append("containing:")
    print "".join(s)
    for i in range(geometry.GetGeometryCount()):
        analyzeGeometry(geometry.GetGeometryRef(i), indent + 1)



def frange(start, stop, step):
    i = 0
    while (start + (i * step)) < stop:
        yield start + i * step
        i += 1

def createBuffer():
    bufferDist = []
    num = int(input("number of buffer"))
    rep = str(input('like to enter manually yes\No'))
    dist = 0
    datasource = open_File()
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        folderLocation, folderName = creating_directory()
        dstPath = os.path.join(folderLocation, "%s.shp" % folderName)
        shpdriver = ogr.GetDriverByName('ESRI Shapefile')
        if os.path.exists(dstPath):
            shpdriver.DeleteDataSource(dstPath)
        outputBufferds = shpdriver.CreateDataSource(dstPath)
        bufferlyr = outputBufferds.CreateLayer(dstPath, layer.GetSpatialRef(), geom_type=ogr.wkbPolygon)
        out_row = ogr.Feature(bufferlyr.GetLayerDefn())
        fieldDef = osgeo.ogr.FieldDefn("distance", osgeo.ogr.OFTReal)
        fieldDef.SetWidth(32)
        bufferlyr.CreateField(fieldDef)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print "feature number %d" % featureIndex
            feature = layer.GetFeature(featureIndex)
            print feature
            geometry = feature.GetGeometryRef()
            for j in range(num):
                if rep == 'yes':
                    dist = float(input("buffer distance"))
                    bufferDist.append(dist)
                else:
                    dist +=0.00001
                    bufferDist.append(dist)
            li=[]
            for i in range(len(bufferDist)):
                poly = geometry.Buffer(bufferDist[i])
                out_row.SetGeometry(poly)
                li.append(i+1)
                out_row.SetField("distance",li[i])
                bufferlyr.CreateFeature(out_row)
                print (i+1)

    datasource=None


#createBuffer()



def union():
    datasource = open_File()
    numLayers = num_of_layers_in_file(datasource)
    for layerIndex in range(numLayers):
        layer = datasource.GetLayerByIndex(layerIndex)
        reply=input("Have output datasource yes/no")
        if reply=="no":
            count, list = number_of_available_drivers()
            driverName = entered_driver_availiblity(count, list)
            driver = osgeo.ogr.GetDriverByName("%s" % driverName)
            folderLocation, folderName = creating_directory()
            name = input("enter shape file name")
            dstPath = os.path.join(folderLocation, "%s.shp" % name)
            dstFile = driver.CreateDataSource("%s" % dstPath)
            dstLayer = dstFile.CreateLayer("resulting layer", layer.GetSpatialRef(), ogr.wkbLineString)
            out_row = ogr.Feature(dstLayer.GetLayerDefn())
        else:
            dstFile = open_File()
            numLayers_output = num_of_layers_in_file(dstFile)
            for layerIndex in range(numLayers_output):
                dstLayer = dstFile.GetLayerByIndex(layerIndex)
                numFeatures_output = num_of_features_in_layer(dstFile, numLayers_output)
                for featureIndex in range(numFeatures_output):
                    print ("feature number %d" % featureIndex)
                    out_row = layer.GetFeature(featureIndex)
        multilinestring = ogr.Geometry(ogr.wkbMultiLineString)
        numFeatures = num_of_features_in_layer(datasource, numLayers)
        for featureIndex in range(numFeatures):
            print ("feature number %d" % featureIndex)
            feature = layer.GetFeature(featureIndex)
            print (feature)
            geometry = feature.GetGeometryRef()
            print (geometry)
            name = geometry.GetGeometryName()
            multilinestring.AddGeometry(geometry)
        poly={}
        for i in range(numFeatures):
            poly[i]=multilinestring.GetGeometryRef(i)

        line = {}
        line[0]=poly[0]
        for i in range(numFeatures-1):
            a = poly[i+1].Union(line[i])
            line[i+1]=a
        out_row.SetGeometry(line[numFeatures-1])
        dstLayer.CreateFeature(out_row)
        dstFile.Destroy()


#union()
#createBuffer()


"G:\Data\shashankdata\Factorlayer\Road.shp,ESRI Shapefile"



def Geometry_Analysis ():
    geometry =get_geometry()
    analyzeGeometry(geometry, indent=0)


def get_Area():
    geometry = get_geometry()
    print ("Area = %d" % geometry.GetArea())

def envelop():
    geometry = get_geometry()
    env = geometry.GetEnvelope()
    print ("minX: %d, minY: %d, maxX: %d, maxY: %d" % (env[0], env[2], env[1], env[3]))

def Length ():
    geometry = get_geometry()
    print ("Length = %d" % geometry.Length())

def intersection_of_geometry():
    poly1= get_geometry()
    poly2= get_geometry()
    intersection = poly1.Intersection(poly2)
    return intersection

def union():
    poly1 = get_geometry()
    poly2 = get_geometry()
    union = poly1.Union(poly2)
    return union()


def get_spatial_reference():
    source = open_File()
    numLayers=num_of_layers_in_file(source)
    for layerNum in range(numLayers):
        layer = source.GetLayer(layerNum)
        spatialRef = layer.GetSpatialRef()
        spatialRef_1 = layer.GetSpatialRef().ExportToProj4()
        print ("Layer %d has spatial reference %s" % (layerNum, spatialRef))
        print ("Layer %d has proj spatial reference %s" % (layerNum, spatialRef_1))
        return (spatialRef,spatialRef_1)

def creating_shapefile_from_existing():
    print ("open file to write")
    source = open_File()
    layer = source.GetLayerByIndex(0)
    while True:
        print ("open file to read")
        datasource=open_File()
        numLayers = num_of_layers_in_file(datasource)
        for layerIndex in range(numLayers):
            layer = datasource.GetLayerByIndex(layerIndex)
            numFeatures = num_of_features_in_layer(datasource, numLayers)
            for featureIndex in range(numFeatures):
                print ("feature number %d" % featureIndex)
                feature = layer.GetFeature(featureIndex)
                geometry = feature.GetGeometryRef()
                name = geometry.GetGeometryName()
                if name == "POINT":
                    featureDefn = layer.GetLayerDefn()
                    feature = ogr.Feature(featureDefn)
                    point = ogr.CreateGeometryFromWkt(geometry)
                    feature.SetGeometry(point)
                    feature.SetField("id",num_of_features_in_layer(source, num_of_layers_in_file(source))+1 )
                    layer.CreateFeature(feature)
                    feature = None
                elif name == "LINESTRING":
                    featureDefn = layer.GetLayerDefn()
                    feature = ogr.Feature(featureDefn)
                    line = ogr.Geometry(ogr.wkbLineString)
                    for i in range(0, geometry.GetPointCount()):
                        pt = geometry.GetPoint(i)
                        long = pt[0]
                        lat = pt[1]
                        print (pt,lat,long)
                        line.AddPoint(long, lat)
                    feature.SetGeometry(line)
                    feature.SetField("FieldID", num_of_features_in_layer(source, num_of_layers_in_file(source)) + 1)
                    layer.CreateFeature(feature)
                    feature.Destroy()
                    del source,layer
                elif name == "POLYGON":
                    poly = ogr.Geometry(ogr.wkbPolygon)
                    ring = ogr.Geometry(ogr.wkbLinearRing)
                    feature = osgeo.ogr.Feature(layer.GetLayerDefn())
                    poly.AddGeometry(geometry)
                    feature.SetGeometry(poly)
                    feature.SetField("id", num_of_features_in_layer(source, num_of_layers_in_file(source)) + 1)
                    layer.CreateFeature(feature)
                    feature.Destroy()
        r=str(input("like to exit yes/no"))
        if r=="yes":
            break


def add_field (path):
    source = open_File_1(path)
    layer = source.GetLayerByIndex(0)
    fieldDef = osgeo.ogr.FieldDefn("Longitude", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    layer.CreateField(fieldDef)
    fieldDef = osgeo.ogr.FieldDefn("Latitude", osgeo.ogr.OFTReal)
    fieldDef.SetWidth(30)
    layer.CreateField(fieldDef)
    for feature in layer:
        feature.SetField("Longitude", feature.GetGeometryRef().GetX())
        print (feature.GetGeometryRef().GetX())
        feature.SetField("Latitude", feature.GetGeometryRef().GetY())
        print (feature.GetGeometryRef().GetY())
        feature.Destroy()




