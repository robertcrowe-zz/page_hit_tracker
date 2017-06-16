import time, datetime
from datetime import timedelta
from unittest import TestCase
from page_hit_tracker import HitTracker

class TestHitTracker(TestCase):
    """Unit testing for HitTracker
    
    Requirements: unittest, nose
    """

    def test_add_hit(self):
        """Add a hit and count it"""
        h1 = HitTracker().open()
        url = '/test_add_hit.py'
        h1.add_hit(url)
        self.assertTrue(h1.num_hits_last_mins(1, url) == 1)
        h1.close()
    
    def test_num_hits_last_mins(self):
        """Make sure that we only count hits of the right age"""
        h1 = HitTracker().open()
        url = '/test_num_hits_last_mins.py'

        ten_minutes_ago = datetime.datetime.now() - timedelta(minutes=10)
        for i in range(0, 5): # adding 5 hits from 10 minutes ago
            h1.add_hit(url, ts=ten_minutes_ago.timestamp())
        for i in range(0, 5): # adding 5 hits from now
            h1.add_hit(url)

        self.assertTrue(h1.num_hits_last_mins(5, url) == 5)
        h1.close()
    
    def test_no_hits(self):
        """Boundary condition"""
        h1 = HitTracker().open()
        url = '/test_no_hits.py'
        self.assertTrue(h1.num_hits_last_mins(10, url) == 0)
        h1.close()

    def test_hits_too_old(self):
        """Don't count hits that are older than the request"""
        h1 = HitTracker().open()
        url = '/test_hits_too_old.py'

        ten_minutes_ago = datetime.datetime.now() - timedelta(minutes=11)
        for i in range(0, 5): # adding 5 hits from 10 minutes ago
            h1.add_hit(url, ts=ten_minutes_ago.timestamp())

        self.assertTrue(h1.num_hits_last_mins(10, url) == 0)
        h1.close()
    
    def test_prune(self):
        """Make sure pruning works"""
        h1 = HitTracker(max_mins=1, prune_chunksize=5).open()
        url = '/test_prune.py'

        ten_minutes_ago = datetime.datetime.now() - timedelta(minutes=10)
        for i in range(0, 5): # adding 5 hits from 10 minutes ago
            h1.add_hit(url, ts=ten_minutes_ago.timestamp())
        for i in range(0, 5): # adding 5 hits from now
            h1.add_hit(url)

        hits_after_prune = h1.num_hits_last_mins(5, url)
        self.assertTrue(hits_after_prune == 5)
        h1.close()
