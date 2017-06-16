import abc

class AbstractTracker(object):
    """Abstract Base Class Definition"""
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def open(self, parms):
        """Required method"""

    @abc.abstractmethod
    def close(self):
        """Required method"""

    @abc.abstractmethod
    def add_hit(self, url, ts):
        """Required method"""

    @abc.abstractmethod
    def num_hits_last_mins(self, minsback, url):
        """Required method"""
