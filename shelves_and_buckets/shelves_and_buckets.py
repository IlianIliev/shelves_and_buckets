# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from intervals import Interval, IntInterval

from .exceptions import BucketDoesNotExists, UnknownDimension


class AbstractShelf(ABC):
    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def add(self, bounds, bucket):
        pass

    def get_multi(self, *args):
        shelf = self
        for arg in args:
            if not isinstance(shelf, AbstractShelf):
                raise UnknownDimension()

            shelf = shelf.get(arg)

        return shelf

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.add(key, value)


class IntervalShelf(AbstractShelf):
    interval_class = Interval

    def __init__(self, buckets=None):
        self.buckets = []

        if not buckets:
            return

        for bounds, bucket in buckets:
            self.add(bounds, bucket)

    def get(self, value):
        for interval, bucket in self.buckets:
            if value in interval:
                return bucket
        else:
            raise BucketDoesNotExists()

    def add(self, bounds, bucket):
        if isinstance(bounds, (list, tuple)):
            interval = self.interval_class(bounds)
        else:
            interval = self.interval_class.from_string(bounds)

        self.buckets.append((interval, bucket))


class IntIntervalShelf(IntervalShelf):
    interval_class = IntInterval


class NamedShelf(AbstractShelf):
    def __init__(self, data=None):
        self.buckets = {}
        if not data:
            return

        if isinstance(data, dict):
            self.buckets = data
        elif isinstance(data, (list, tuple)):
            self.buckets = dict(data)

    def get(self, key):
        try:
            return self.buckets[key]
        except KeyError:
            raise BucketDoesNotExists()

    def add(self, name, bucket):
        self.buckets[name] = bucket
