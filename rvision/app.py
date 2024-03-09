from flask import Flask,render_template,redirect,url_for,flash
from flask import request
import os
import keras
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2
from keras.preprocessing import image
import numpy as np
from keras.models import load_model

def return_class(img_path):
    model_1=load_model('main_model.h5')
    model_2=load_model('model1.h5')
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions_1 = model_1.predict(img_array)
    predictions_2 = model_2.predict(img_array)
    
    class_name_1=np.argmax(predictions_1)
    class_name_2=np.argmax(predictions_2)
    
    print(class_name_1)
    
    output1=predictions_1[0][class_name_1]
    output2=predictions_2[0][class_name_2] 
    
    
    '''if class_name_1==0:
        return output1*100
    else:
        return output1*100'''
    for i in predictions_1:
        for j in i:
            return j*100
    for i in predictions_2:
        for j in i:
            return j*100

    
    
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html',display1='flex',display2='none')


@app.route('/result',methods=['POST']) 
def result():
    if request.method == 'POST':
        input_image=request.files['image']
        print(input_image.filename)
    
        extension=input_image.filename.split('.')[-1]
        filename=input_image.filename.split('.')[0]
        input_image.save('static/'+input_image.filename)
        output=return_class('static/'+input_image.filename)
        print(output)
        print("Hello workld")
        return render_template('index.html',output=output,filename=input_image.filename,display1='none',display2="flex")


if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    