import numpy as np
import io
from PIL import Image
import keras
import base64
from keras import backend as K
from keras.models import Sequential
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
from keras.preprocessing.image import img_to_array
from keras.preprocessing.image import load_img
from flask import request
from flask import jsonify
from flask import Flask, render_template
import re
from werkzeug.utils import secure_filename
import operator
import os

app = Flask(__name__)
# model = Sequential()
def get_model():
	global model
	model = load_model('_weights.h5')
	print("Model loaded!")

def preprocess_image(image, target_size):
	if image.mode != "RGB":
		image = image.convert("RGB")
	image = image.resize(target_size)
	image = img_to_array(image)
	image = np.expand_dims(image, axis=0)
	image /= 255
	return image

# print ("Loading Keras model...")
# get_model()

def convertImage(imgData1):
	imgstr = re.search(r'base64,(.*)',imgData1).group(1)
	#print(imgstr)
	with open('output.png','wb') as output:
		output.write(imgstr.decode('base64'))

@app.route("/")
def home():
	return render_template('index.html')

@app.route("/raj")
def test():
	di = os.getcwd()
	return ("dir:-"+di)


@app.route("/predict", methods=["POST"])
def predict():
	model = load_model('_weights.h5')
	# message = request.get_json(force=True)
	# encoded = message['image']
	encoded = request.files['img_form']
	encoded.save(secure_filename(encoded.filename))

	# print('*********************')
	# print(type(encoded))
	# decoded = base64.b64decode(encoded)
	# image = Image.open(io.BytesIO(decoded))
	# image_arr = preprocess_image(image, target_size=(150, 150))
	
	# prediction = model.predict(processed_image).tolist()

	# convertImage(encoded)
	# x = imread('output.png',mode='L')
	# image_arr = preprocess_image(x, target_size=(150, 150))
	target_size=(150,150)

	# prepare image for classification using keras utility functions
	image = load_img(encoded.filename, target_size=target_size)

	image_arr = img_to_array(image) # convert from PIL Image to NumPy array
	# the dimensions of image should now be (150, 150, 3)

	# to be able to pass it through the network and use batches, we want it with shape (1, 150, 150, 3)
	image_arr = np.expand_dims(image_arr, axis=0)
	image_arr /= 255

	# image = load_img(encoded.filename)
	# image = preprocess_image(image, target_size)

	class_labels = ['safe_driving', 'texting_right', 'talking_on_phone_right', 'texting_left', 'talking_on_phone_left',
                'operating_radio', 'drinking', 'reaching_behind', 'doing_hair_makeup', 'talking_to_passanger']
	predictions = model.predict(image_arr)

	# get human-readable labels of the preditions, as well as the corresponding probability
	decoded_predictions = dict(zip(class_labels, predictions[0]))

	# sort dictionary by value
	decoded_predictions = sorted(decoded_predictions.items(), key=operator.itemgetter(1), reverse=True)

	print()
	count = 1
	for key, value in decoded_predictions[:1]:
	    print("{}. {}: {:8f}%".format(count, key, value*100))
	    pred = key
	    count+=1

	response = { 'prediction': str(pred)}

	os.remove(encoded.filename)
	K.clear_session()
	return jsonify(response)


