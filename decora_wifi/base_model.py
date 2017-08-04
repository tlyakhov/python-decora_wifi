
class BaseModel:
    """ This is the base class for all Leviton REST models """
    def __init__(self, session, model_id=None):
        """Set up fields..."""
        self._session = session
        self._id = model_id
        self.data = {}

    def __str__(self):
        """Output the wrapped data dictionary."""
        return str(self.data)
