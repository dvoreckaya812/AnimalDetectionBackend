from abc import ABC, abstractmethod


class AbstractModelLoader(ABC):

    @abstractmethod
    def load_model(self, model):
        pass

    @abstractmethod
    def find_objects(self, **data):
        pass
