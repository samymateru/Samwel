class PopDict:
    def __init__(self):
        self._store = {}

    def put(self, key, value):
        self._store[key] = value

    def get(self, key, default=None):
        # pop removes the key after returning value
        return self._store.pop(key, default)

    def __contains__(self, key):
        return key in self._store

    def __len__(self):
        return len(self._store)

    def __repr__(self):
        return f"{self._store}"