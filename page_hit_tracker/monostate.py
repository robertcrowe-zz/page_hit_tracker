class MonoState(object):
    """Enforces a single state across multiple instances"""
    
    _state = {}

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        self.__dict__ = cls._state
        return self