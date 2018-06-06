import matplotlib.pyplot as plt
import cv2
import numpy as np
from keras.models import model_from_json

def minify_images(resolution, images):
    tmp = []
    for img in images:
        tmp.append(cv2.resize(img, dsize=resolution, interpolation=cv2.INTER_CUBIC))

    return np.array(tmp)

def draw_graph(history, save_name):
	fig, ax = plt.subplots(2, 1)
	ax[0].plot(history.history['acc'], 'ro-', label = "Train Accuracy")
	ax[0].plot(history.history['val_acc'], 'go-', label = "Test Accuracy")
	ax[0].set_xlabel("Epoch")
	ax[0].set_ylabel("Accuracy / %")
	ax[0].legend(loc = "best")
	ax[0].grid('on')

	ax[1].plot(history.history['loss'], 'ro-', label = "Train Loss")
	ax[1].plot(history.history['val_loss'], 'go-', label = "Test Loss")
	ax[1].set_xlabel("Epoch")
	ax[1].set_ylabel("Loss")
	ax[1].legend(loc = "best")
	ax[1].grid('on')

	plt.tight_layout()
	plt.savefig(f"{save_name}.pdf", bbox_inches = "tight")

def load_model(datapaths, model_name, nx, ny):
    filename = datapaths.model_data / f"{model_name}_{nx}_{ny}.json"
    json_file = open(filename, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(datapaths.model_data / f"{model_name}_{nx}_{ny}.h5")

    return loaded_model
