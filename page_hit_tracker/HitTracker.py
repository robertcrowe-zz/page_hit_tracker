"""
HitTracker

v0.1 Robert Crowe 16 June 2017
See README for details
"""

from __future__ import division, absolute_import, print_function

import time
import datetime
from datetime import timedelta
from bisect import bisect_left

try: # different for local debug
    from .monostate import MonoState
    from .AbstractTracker import AbstractTracker
except:
    from monostate import MonoState
    from AbstractTracker import AbstractTracker

class TrackerException(Exception):
    """Thrown for errors"""
    def __init__(self, msg):
        self.message = msg

class HitTracker(MonoState, AbstractTracker):
    """A very simple in-memory hit tracker for web pages"""

    _data = None

    def __init__(self, max_mins=10, prune_chunksize=100):
        """Constructor

        Keyword arguments:
        max_mins -- The maximum number of minutes of history to track.  Older hits are pruned. (default 10)
        prune_chunksize -- Sets the frequency of pruning. Higher values prune less often (default 100)
        """
        if self._data is None:
            self._data = {} # a dictionary of lists using urls as keys seems to be all we need
        
        self._max_mins = abs(max_mins) # stay positive, even if they go negative
        self._prune_chunksize = prune_chunksize # to avoid pruning with every append
    
    def open(self):
        """Because other implementations may need this"""
        self._connected = True # To mimic a data store, so that clients are written correctly
        return self
    
    def close(self):
        """Close the connection and clean up"""
        if self._connected: # allow them to close again, so don't raise exception
            self._connected = False
            self._data = {}
    
    def _prune_history(self, url):
        """Private - Keeps the in-memory data from growing too big"""
        if not self._connected:
            raise TrackerException('HitTracker._prune_history: Tried to prune when not connected')
        
        if len(self._data[url]) > 0:
            oldest_allowed = datetime.datetime.now() - timedelta(minutes=self._max_mins)
            too_old = bisect_left(self._data[url], oldest_allowed.timestamp())
            if too_old >= self._prune_chunksize:
                self._data[url] = self._data[url][too_old:]
    
    def add_hit(self, url, ts=None):
        """Add a hit for a page

        Arguments:
        url -- (Required) The URL of the page that was hit.

        Keyword arguments:
        ts -- The timestamp of the hit.  (default now)
        """
        if url is None:
            raise TrackerException('HitTracker.add_hit: URL of page is required')
        
        if not self._connected:
            raise TrackerException('HitTracker.add_hit: Tried to add when not connected')
        
        if ts is None:
            ts = time.time()
        elif isinstance(ts, datetime.datetime):
            raise TrackerException('HitTracker.add_hit: You passed me a datetime instead of a timestamp')
        
        if url not in self._data.keys():
            self._data[url] = []
        else:
            self._prune_history(url)
        self._data[url].append(ts)
        return self
    
    def num_hits_last_mins(self, minsback, url):
        """Return the number of hits from now going back X minutes

        Arguments:
        minsback -- (Required) The number of minutes before now
        url -- (Required) The URL of the page to get the hits for
        """
        if not self._connected:
            raise TrackerException('HitTracker.num_hits_last_mins: Tried to query when not connected')
        if url is None:
            raise TrackerException('HitTracker.num_hits_last_mins: URL of page is required')
        
        if url not in self._data.keys():
            return 0
        
        print('Updated')
        first_hit = datetime.datetime.now() - timedelta(minutes=abs(minsback))
        startrange = bisect_left(self._data[url], first_hit.timestamp())
        return len(self._data[url]) - startrange
