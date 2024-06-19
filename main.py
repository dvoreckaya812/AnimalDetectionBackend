import base64
import time
import json
from flask import request, render_template, redirect, url_for, Flask, Response, jsonify
from sessions.Session import Session
import cv2
from modelloader.YOLOModelLoader import YOLOModelLoader
from cachesystem.Cache import Cache


app = Flask(__name__)
cache = Cache()


@app.route('/image-animal-detection', methods=['POST'])
def image_animal_detection():
    model = YOLOModelLoader()
    model.load_model('static/files/best.pt')
    classes = []
    data = request.data
    user_session = Session(request.remote_addr + ":" + str(request.environ.get('REMOTE_PORT')))
    source_filepath = str(user_session) + "/source.jpg"
    result_filepath = str(user_session) + "/result.jpg"
    with open(source_filepath, "wb") as data_file:
        data_file.write(data)
    el = cache.check_cached(source_filepath)
    if not el:
        image = cv2.imread(source_filepath, cv2.IMREAD_COLOR)
        result = model.find_objects(data_to_predict=image)
        for r in result:
            for c in r.boxes.cls:
                classes.append(int(c))
        cv2.imwrite(result_filepath, result[0].plot())
        cache.add_data(source_filepath, result_filepath, classes)
    else:
        result_filepath = el.data
        classes = el.classes
    with open(result_filepath, "rb") as image:
        b64_response = base64.b64encode(image.read())
    classes = list(set(classes))
    json_data = {'classes': classes, 'media': b64_response.decode('utf-8')}
    response = Response(response=json.dumps(json_data), status=200, mimetype="application/json")
    return response


@app.route('/video-animal-detection', methods=['POST'])
def video_animal_detection():
    model = YOLOModelLoader()
    model.load_model('static/files/best.pt')
    classes = []
    data = request.data
    user_session = Session(request.remote_addr + ":" + str(request.environ.get('REMOTE_PORT')))
    source_filepath = str(user_session) + "/source.mp4"
    result_filepath = str(user_session) + "/predict/source.mp4"
    with open(source_filepath, "wb") as data_file:
        data_file.write(data)
    el = cache.check_cached(source_filepath)
    if not el:
        result = model.find_objects(data_to_predict=source_filepath, filepath=str(user_session) + "/")
        for r in result:
            for c in r.boxes.cls:
                classes.append(int(c))
        cache.add_data(source_filepath, result_filepath, classes)
    else:
        result_filepath = el.data
        classes = el.classes
    with open(result_filepath, "rb+") as video:
        b64_response = base64.b64encode(video.read())
    classes = list(set(classes))
    json_data = {'classes': classes, 'media': b64_response.decode('utf-8')}
    response = Response(response=json.dumps(json_data), status=200, mimetype="application/json")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

