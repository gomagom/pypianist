import cv2
import glob
import random
import numpy as np
from sklearn import model_selection
classes = ["8kyu", "4kyu", "flatto"]
num_classes = len(classes)
img_widh = 50
img_height = 100

X = []
Y = []
data_set=[]
for idx, classlabel in enumerate(classes):
    photos_dir = "../data/notedata_set/" + classlabel
    files = glob.glob(photos_dir + "/*.png")
    for i, file in enumerate(files):
        #if i >= 300:    
            #break
        img = cv2.imread(file)
        data = cv2.resize(img,(img_widh, img_height))
        img2=np.asarray(data)
        data_set.append((idx,img2))
random.shuffle(data_set)
for x in data_set:
    X.append(x[1])  
    Y.append(x[0])
X = np.array(X)
Y = np.array(Y)
X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("../data/notedata_set/note.npy", xy)
