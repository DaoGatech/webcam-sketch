from flask import Flask, render_template, Response, request, jsonify, json
from flask_restful import Resource, Api
from sketch import sketch, sharpen
from flask_bootstrap import Bootstrap
import cv2
import time
app = Flask(__name__)
Bootstrap(app)
api = Api(app)
webcamFunc = None
t_end = None

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

def sketchWebcam():
    global webcamFunc
    global t_end
    vc = cv2.VideoCapture(0)
    t_end = time.time() + 5
    """Video streaming generator function."""
    while time.time() < t_end:
        rval, frame = vc.read()
        if rval:
            cv2.imwrite('t.jpg', webcamFunc(frame))
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('t.jpg', 'rb').read() + b'\r\n')


@app.route('/webcam', methods=["GET", "POST"])
def webcam():
    global webcamFunc
    global t_end
    """Video streaming route. Put this in the src attribute of an img tag."""
    if request.method == 'GET':
        if not webcamFunc:
            webcamFunc = sketch

        return Response(sketchWebcam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    if request.content_type != 'application/json':
        return jsonify({})
    try:
        webcamMode = json.loads(request.data)
        webcamModeMap = {
            'sketch': sketch,
            'sharpen': sharpen
        }
        webcamFunc = webcamModeMap[webcamMode['mode']]
              
        return Response(sketchWebcam(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

    except ValueError as e:
        print(e)
        return jsonify({})
    

if __name__ == '__main__':
    app.run(debug=True)