
class BaseModel:
    def __init__(self, session, model_id=None):
        self._session = session
        self._id = model_id
        self._data = {}

    def update_model_data(self, data):
        return self._data.update(data)

    def set_model_data(self, data):
        self._data = data
        return self._data

    def get_model_data(self):
        return self._data
