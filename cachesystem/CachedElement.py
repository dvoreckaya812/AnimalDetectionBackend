import datetime


class CachedElement:

    def __init__(self, uid, data, classes):
        self._data = [_InnerCachedElement(uid, data, classes)]
        self._used = datetime.datetime.now()

    def add_data(self, uid, data, classes):
        self._data.append(_InnerCachedElement(uid, data, classes))

    def get_data(self):
        return self._data

    def used(self):
        return self._used

    def update_used_time(self):
        self._used = datetime.datetime.now()


class _InnerCachedElement:

    def __init__(self, uid, data, classes):
        self.key = uid
        self.data = data
        self.classes = classes
