import keras
import numpy as np

def prediction(file):
    model = keras.models.load_model('new_model.h5')
    x = []
    def test_model():
        # img = keras.preprocessing.image.load_img(file)
        img = file
        img = img.resize((200,200))
        x.append(img)
        
    test_model()
    x = np.array(x)
    x = x/255
    y_pred = model.predict(x)

    result = y_pred[0][0]*100

    return result