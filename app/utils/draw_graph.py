import matplotlib.pyplot as plt

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
