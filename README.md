This is a Django app for RSVP
1. `virtualenv env`
2. `source ./env/bin/activate`
3. `pip install -r requirement.txt`
4. `FLASK_APP=predict.py flask run` or `FLASK_APP=predict_vgg.py flask run`

Note - uploaded images should be from same distribution as training images, other images might get predicted wrong prediction.