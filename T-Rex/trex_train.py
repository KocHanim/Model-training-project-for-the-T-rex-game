#provide access to pictures and folders
import glob
import os
import numpy as np
#deep learning algorithm training
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten,Conv2D, MaxPooling2D
from PIL import Image
#labelling of data and use of labelled data
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
#dividing data sets into 2
from sklearn.model_selection import train_test_split
#visualisation
# import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

imgs = glob.glob("./img/*.png")

width = 125
height = 50

X = []
Y = []

#transformations required before training
for img in imgs:
    filename = os.path.basename(img)
    label = filename.split("_")[0]
    im = np.array(Image.open(img).convert("L").resize((width,height)))
    #normalize
    im = im/255
    X.append(im)
    Y.append(label)
    
X = np.array(X)
X = X.reshape(X.shape[0], width, height, 1)

#sns.countplot(Y)
   
#Converting "up,down,right" data in Y to numeric variable
def onehot_labels(values):
    label_encoder = LabelEncoder()
    integer_encoded = label_encoder.fit_transform(values)
    onehot_encoder = OneHotEncoder(sparse= False)
    #After the integer_encoded.shape command (296, ) we write (296,1) because this will give an error.
    #we convert to binary values
    integer_encoded = integer_encoded.reshape(len(integer_encoded),1)
    onehot_encoder = onehot_encoder.fit_transform(integer_encoded)
    return onehot_encoder

Y = onehot_labels(Y)
#X's are our images, Y's are the labels of these images.
# test_size, training data set 75%, test data set 25%
#random_state, random division (for not memorising)
train_X, test_X, train_Y, test_Y = train_test_split(X, Y, test_size=0.25, random_state = 2)

#cnn model
model = Sequential()
model.add(Conv2D(32, kernel_size=(3,3), activation="relu",input_shape = (width, height, 1)))
model.add(Conv2D(64, kernel_size=(3,3), activation="relu"))
#pixel insertion
model.add(MaxPooling2D(pool_size=(2,2)))
#dilution
model.add(Dropout(0.25))
#Flattening (for sorting)
model.add(Flatten())
model.add(Dense(128, activation="relu"))
model.add(Dropout(0.4))
#Output layer
model.add(Dense(3, activation="softmax"))

#if os.path.exists("./trex_weight.h5"):
#    model.load_weights("trex_weight.h5")
#    print("Weight yüklendi")


#loss function is used to calculate error
#optimizer to optimise parameters
#metrics will give the percentage of success as a result of the model
model.compile(loss="categorical_crossentropy", optimizer="Adam", metrics=["accuracy"])

#epochs, we specify how many times the training will occur
#batch_size, we tell how many batches of images to iterate into.
model.fit(train_X, train_Y, epochs=35, batch_size = 64)

score_train = model.evaluate(train_X,train_Y)
print("Eğitim Doğruluğu: %",score_train[1]*100)

score_test = model.evaluate(test_X,test_Y)
print("Test Doğruluğu: %",score_test[1]*100)

#to save the model
open("model_new.json", "w").write(model.to_json())
model.save_weights("trex_weight_new.h5")
    























