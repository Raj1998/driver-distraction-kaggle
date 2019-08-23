import keras
from keras.layers import Dropout, Flatten, Dense

def modelDeDe():
	vgg_model = keras.applications.vgg16.VGG16(weights='imagenet')

	vgg_model.layers.pop()
	vgg_model.layers.pop()
	vgg_model.layers.pop()
	vgg_model.layers.pop()

	model = keras.models.Sequential()

	for layers in vgg_model.layers:
		model.add(layers)

	for layer in model.layers:
		layer.trainable = False

	model.add(Flatten())
	model.add(Dense(256, activation='relu'))
	model.add(Dropout(0.5))
	model.add(Dense(10, activation='softmax'))

	return model