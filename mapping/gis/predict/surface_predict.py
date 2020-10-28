from keras.models import load_model
import numpy



def predictio(lam):
    test_x = numpy.array([lam])
    score=load_model('C:\MappingSystem\mapping\gis\predict\hotspot_prediction_1_updated.h5').predict(test_x, batch_size=1, verbose=1)
    #print("Predicted distance = %s" % (score))
    return score

