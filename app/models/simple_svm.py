# Path hack.
import sys, os
sys.path.insert(0, os.path.abspath('..'))

from utils.load_data import load_data
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.externals import joblib
import numpy as np

images, keyboards = load_data(start_index = 1)
lb = LabelEncoder()
clf = SVC()

lb.fit(keyboards)
keyboards = lb.fit_transform(keyboards)
np.save('svm_classes.npy', lb.classes_)

nsamples, nx, ny = images.shape
# Rewrite original to optimize memory usage
images = images.reshape((nsamples,nx*ny))

# Memory optmizing.
images, x_test, keyboards, y_test = train_test_split(images, keyboards, test_size=0.1)

clf.fit(images, keyboards)
y_pred = clf.predict(x_test)

score = accuracy_score(y_test,y_pred)
print(f"My score is: {score}, Yay!")

joblib.dump(clf, 'simple_svm.pkl')