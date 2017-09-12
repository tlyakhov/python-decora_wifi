
class BaseModel(object):
    """ This is the base class for all Leviton REST models """
    def __init__(self, session, model_id=None):
        """Set up fields..."""
        self.data = {}
        self._session = session
        self._id = model_id

    def __str__(self):
        """Output the wrapped data dictionary."""
        return str(self.data)

    def __getattribute__(self, name):
        """Forward all getters that have keys in self.data to the dict"""
        data = super(BaseModel, self).__getattribute__('data')
        if name == 'data':
            return data

        if name in data:
            return data[name]
        else:
            return super(BaseModel, self).__getattribute__(name)

    def __setattr__(self, key, value):
        """Forward all setters that have keys in self.data to the dict"""
        if key == 'data':
            super(BaseModel, self).__setattr__(key, value)
            return

        data = super(BaseModel, self).__getattribute__('data')
        if key in data:
            data[key] = value
        else:
            super(BaseModel, self).__setattr__(key, value)
