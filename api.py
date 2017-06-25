from flask import Flask, render_template, Response, request, jsonify, json
from flask_restful import Resource, Api
from sketch import sketch, sharpen
from flask_bootstrap import Bootstrap
import cv2
app = Flask(__name__)
Bootstrap(app)
api = Api(app)
vc = None

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def sketchWebcam():
    global vc
    if vc:
        vc.release()
        vc = None
    vc = cv2.VideoCapture(0)
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', sketch(frame))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

def sharpenWebcam():
    global vc
    if vc:
        print("here")
        vc.release()
        vc = None
    vc = cv2.VideoCapture(0)
    """Video streaming generator function."""
    while True:
        rval, frame = vc.read()
        cv2.imwrite('t.jpg', sharpen(frame))
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')

@app.route('/webcam', methods=["GET", "POST"])
def webcam():
    """Video streaming route. Put this in the src attribute of an img tag."""
    if request.method == 'GET':
        return Response(sketchWebcam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    if request.content_type != 'application/json':
        return jsonify({})
    try:
        webcamMode = json.loads(request.data)
        webcamModeMap = {
            'sketch': sketchWebcam,
            'sharpen': sharpenWebcam
        }
        webcamFunc = webcamModeMap[webcamMode['mode']]      
        return Response(sharpenWebcam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    except ValueError as e:
        print(e)
        return jsonify({})
    

if __name__ == '__main__':
    app.run(debug=True)