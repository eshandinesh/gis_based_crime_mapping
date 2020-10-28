import ogr
def open_File(path):
    if path is None:
        filePath = str(input("file path"))
    else:
        filePath = path
    datasource = ogr.Open(filePath, 0)
    return datasource

'''f=open_File("C:/Users\Hp\Desktop\desktomat\DATA\SHORTROUTE\SHORTROUTE.shp")
for a in f:
    for r in a:
        g=r.GetGeometryRef()
        print(g)
        for u in range(g.GetGeometryCount()):
            print(g.GetGeometryRef)
            l=[]
            for f in range(g.GetGeometryRef(u).GetPointCount()):
                a=[g.GetGeometryRef(u).GetPoint(f)[1],g.GetGeometryRef(u).GetPoint(f)[0]]
                l.append(a)
            #print(l)


b=[]
f=open_File("C:/Users\Hp\Desktop\desktomat\DATA\SHORTROUTE\SHORTROUTE.shp")
for a in f:
    for r in a:
        o=[]
        g=r.GetGeometryRef()
        for i in range(0, g.GetPointCount()):
                pt = g.GetPoint(i)
                print (i)
                o.append([pt[1],pt[0]])
        b.append(o)
    print(b)

f=open_File("C:/Users\Hp\Desktop\shp\datia.shp")
for a in f:
    print(a.GetFeatureCount())
    if input("press enter"):
        pass
    for feat in a:
        l=[]
        print(feat.GetField('name'))
        for k in feat.GetGeometryRef():
            for count in range(k.GetPointCount()):
                l.append([k.GetPoint(count)[1],k.GetPoint(count)[0]])
        print(l)'''
wkt = "POINT (78.45547199249268 25.660289064684854)"
pt = ogr.CreateGeometryFromWkt(wkt)
bufferDistance = 0.000500
poly = pt.Buffer(bufferDistance)
for k in poly:
    l=[]
    for count in range(k.GetPointCount()):
        l.append([k.GetPoint(count)[1],k.GetPoint(count)[0]])
    print(l)

a=[[26.2081168673041,78.1884911730817],[26.207139837723,78.1888023093275],[26.2067740511394,78.1889256909421],[26.2067740511394,78.1889256909421],[26.2069665705372,78.1900200322202],[26.2069646462726,78.1900125230691],[26.2070052059809,78.1919054129465],[26.206721239852,78.1919536927088],[ 26.2063939559966,78.191991243635],[26.2074816899632,78.1898883917673],[26.2075779491167,78.1905696728571],[26.2075779491167,78.1905696728571],[26.2070485227873,78.1906501391276],[26.2070485227873,78.1906501391276],[26.2068511905394,78.1906769612177],[26.2063939559966,78.191991243635],[26.2064902160496,78.1929782965525],[26.2068511905394,78.1906715967997],[26.2070052059811,78.1919054129465],[26.206499842051,78.1931124070032],[26.20649021605,78.1929782965525],[26.2050078024081,78.1931928732737],[26.2050318677154,78.1933001616343],[26.2050318677154,78.1933001616343],[26.2057345724941,78.1932250597819],[26.2057345724941,78.1932250597819],[26.2064998420512,78.1931177714213],[26.2079039570929,78.1889791829101],[26.2081168673041,78.1884911730817],[26.2052436996913,78.1940147994496],[26.2050366807763,78.1933001616343]]