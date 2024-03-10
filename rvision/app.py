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
    model_1=load_model('D00_D40.h5')
    model_2=load_model('D10_D40.h5')
    model_3=load_model('D10_D20.h5')
    img = image.load_img(img_path, target_size=(224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    
    predictions_1 = model_1.predict(img_array)
    predictions_2 = model_2.predict(img_array)
    predictions_3 = model_3.predict(img_array)
    
    class_name_1=np.argmax(predictions_1)
    class_name_2=np.argmax(predictions_2)
    class_name_3=np.argmax(predictions_3)
    
    print(class_name_1)
    print(class_name_2)
    print(class_name_3)
    output1=predictions_1[0][class_name_1]
    output2=predictions_2[0][class_name_2] 
    output3=predictions_3[0][class_name_3]
    
    if output1>output2 and output1>output3:
        return output1,"Longitudinal Cracks"
    elif output2>output1 and output2>output3: 
        return output2,"Alligator Crack"
    elif output3>output1 and output3>output2:
        return output3,"Potholes"
    else:
        return output3,"Transverse Crack"
    

# from twilio.rest import Client
#  # Your Twilio Account SID and Auth Token
# account_sid = 'AC9c4da5ec7502ef1b5f12debc80622960'
# auth_token = '8578d8b7dd3ec722b7e9dc056c7c17e0'
# client = Client(account_sid, auth_token)

# def send_sms(to, body):
#     message = client.messages.create(
#         body=body,
#         from_='+15169798339',
#         to=to
#     )
# print("SMS sent successfully!")

# # Example usage:
# send_sms('+91 6379656039', 'Thank you for using our service!') 

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
    
@app.route('/result',methods=['POST']) 
def result():
    if request.method == 'POST':
        input_image=request.files['input_image']
        print(input_image.filename)
        extension=input_image.filename.split('.')[-1]
        filename=input_image.filename.split('.')[0]
        input_image.save('static/'+input_image.filename)
        output=return_class('static/'+input_image.filename)
        return render_template("index.html",img_path=input_image.filename,output=output)



if __name__ == '__main__':
    app.run(debug=True)