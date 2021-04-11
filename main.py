# import the necessary packages
import numpy as np
import cv2

from camera import VideoCamera
from flask import Flask,jsonify,render_template,Response, request,redirect, url_for

from flask_cors import CORS 

app=Flask(__name__)
CORS(app)

def gen(camera):

    while True:
        frame=camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n'+ frame
               + b'Content-Type: \r\n\r\n'
               + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return jsonify({'message': 'success video feed'})
    # return Response(gen(VideoCamera()), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['GET'])
def First():
   return jsonify({'message': 'success root'})
    # return render_template('detect.html')


if __name__=="__main__":
    app.run(debug=True)


