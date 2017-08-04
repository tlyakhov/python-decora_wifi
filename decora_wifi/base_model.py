
class BaseModel:
    def __init__(self, session, model_id=None):
        self._session = session
        self._id = model_id
        self.data = {}

    def __str__(self):
        return str(self.data)
