import datetime
import os
from cachesystem.CachedElement import CachedElement
import hashlib


class Cache:

    def __init__(self):
        self._cache = {}
        self._time_to_delete = datetime.timedelta(hours=3)

    def add_data(self, key_data, data, classes):
        with open(key_data, "rb") as file:
            _hash = hashlib.md5(file.read()).hexdigest()
        if _hash not in self._cache.keys():
            self._cache[_hash] = CachedElement(key_data, data, classes)
        else:
            for el in self._cache[_hash].get_data():
                cache_size = os.path.getsize(el.key)
                new_size = os.path.getsize(key_data)
                if cache_size != new_size:
                    self._cache[_hash].add_data(key_data, data, classes)
                    break
        self._recalculate()

    def _recalculate(self):
        now = datetime.datetime.now()
        for key in self._cache.keys():
            if now - self._cache[key].used() > self._time_to_delete:
                self._clear_cache_elem(self._cache[key])

    def clear_cache(self):
        for key in self._cache.keys():
            self._clear_cache_elem(self._cache[key])

    def _clear_cache_elem(self, cache_elem):
        os.remove(os.getcwd() + cache_elem)
        del cache_elem

    def check_cached(self, key):
        with open(key, "rb") as file:
            _hash = hashlib.md5(file.read()).hexdigest()
        try:
            for el in self._cache[_hash].get_data():
                cache_size = os.path.getsize(el.key)
                new_size = os.path.getsize(key)
                if cache_size == new_size:
                    self._cache[_hash].update_used_time()
                    return el
        except KeyError:
            return None
