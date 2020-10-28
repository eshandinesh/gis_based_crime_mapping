from keras.models import load_model
import numpy,glob,os,xlrd
import plotly.graph_objs as go
import plotly.offline as ply

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
    return result,frequency

def label(frequency):#rank urf probability
    a=0
    rank=[]
    for j in frequency:
        a+=j
    for k in frequency:
        rank.append(k/a)
    return rank
lat,lon,rankplot,predictscore,z1,z2,z,di=[],[],[],[],[],[],[],{}
def output(result, rank):
    for i,j in zip(result,rank):
        print([i,j])
test_result, test_frequency= ope_file(path="C:/Users\AMITY UNIVERSITY\Desktop/test_data")
for h in test_result:
    lat.append(h[0])
    lon.append(h[1])
for k in lat:
    for t in lon:
        print([k,t])
        z1.append([k,t])
test_result=numpy.array(z1)
test_result=numpy.array(test_result)
test_rank=label(test_frequency)
test_rank=numpy.array(test_rank)
score=load_model('hotspot_prediction_1.h5').predict(test_result, batch_size=1, verbose=1)

for i in range(len(score)):
    print("Latitude, Longitude = %s, Predicted Crime = %s" % (test_result[i], score[i]))
    print("Latitude, Longitude = %s, Exact Crime = %s" % (test_result[i], test_rank[i]))
    di[z1[i]]=score[i]
    print(test_result[i],z1[i])

for k in lat:
    for t in lon:
        z2.append(di[[k,t]])
    z.append(z2)
data=[
    go.Surface(x=numpy.array(lat),y=numpy.array(lon),z=numpy.array(z))
]
ply.plot(data,filename="plot.html")