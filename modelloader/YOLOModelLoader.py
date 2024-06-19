from modelloader.ModelLoader import AbstractModelLoader
from ultralytics import YOLO


class YOLOModelLoader(AbstractModelLoader):

    def __init__(self):
        self._model = None

    def load_model(self, model):
        self._model = YOLO(model)

    def find_objects(self, **data):
        self._model.fuse()
        _data = data['data_to_predict']
        try:
            filepath = data['filepath']
            return self._model.predict(_data, project=filepath, save=True, stream=True)
        except KeyError:
            return self._model.predict(_data)
