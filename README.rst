################
Page Hit Tracker
################

v0.1 Robert Crowe 16 June 2017

This is a very basic page hit tracker/reporter.  It really only does two things:

    * Add hits for specific URLs
    * Return the number of hits for specific URLs starting from X minutes ago until now

It uses a MonoState Singleton pattern to enforce a single state across multiple instances, and currently only 
persists data in memory. It should be thread-safe, and you probably want to instantiate from the main thread.
Singleton can be an anti-pattern, but in this case it seems to make sense.

The main class is HitTracker, which implements AbstractTracker.  More robust implementations should be able to
derive from AbstractTracker.

Requirements::
    Python 3

Installation::

    To install locally, clone the repo, move to the root directory of the package and run:
    >>> pip install -e .

Usage::

    >>> from page_hit_tracker import HitTracker
    >>> h1 = HitTracker(max_mins=10, prune_chunksize=100).open()
    >>> h1.add_hit('some_url')
    >>> num_hits = h1.num_hits_last_mins(5, 'some_url')

Testing::

    To run the unit tests, move to the root directory of the package and run:
    >>> python setup.py test
