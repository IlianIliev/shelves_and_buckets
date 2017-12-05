#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `shelves_and_buckets` package."""

import pytest


from shelves_and_buckets import IntervalShelf, IntIntervalShelf, NamedShelf, FloatIntervalShelf
from shelves_and_buckets.exceptions import BucketDoesNotExists, UnknownDimension


def test_interval_shelf():
    shelf = IntervalShelf([
        ([0, 10], 'Bucket 1'),
        ([11, 20], 'Bucket 2'),
        ([21, 30], 'Bucket 3'),
    ])

    assert shelf.get(0) == 'Bucket 1'
    assert shelf.get(5) == 'Bucket 1'
    assert shelf.get(10) == 'Bucket 1'
    assert shelf.get(11) == 'Bucket 2'
    assert shelf.get(20) == 'Bucket 2'

    with pytest.raises(BucketDoesNotExists):
        shelf.get(-10)


def test_add_to_shelf():
    shelf = IntervalShelf()

    shelf.add([0, 10], 'Bucket 1')


def test_int_interval_shelf():
    shelf = IntIntervalShelf([
        ([0, 10], 'Bucket 1'),
        ('(10, 20]', 'Bucket 2'),
        ('[30, )', 'Bucket 3'),
    ])

    assert shelf.get(0) == 'Bucket 1'
    assert shelf.get(10) == 'Bucket 1'
    assert shelf.get(20) == 'Bucket 2'
    assert shelf.get(10**10) == 'Bucket 3'

    with pytest.raises(BucketDoesNotExists):
        shelf.get(-10)


def test_named_shelf():
    shelf = NamedShelf([
        ('one', 'Bucket 1'),
        ('two', 'Bucket 2'),
        ('three', 'Bucket 3'),
    ])

    assert shelf.get('one') == 'Bucket 1'

    with pytest.raises(BucketDoesNotExists):
        shelf.get('four')

    shelf = NamedShelf()
    shelf.add('abc', 'ABC')


def test_named_shelf_from_dict():
    shelf = NamedShelf({
        'one': 'Bucket 1',
        'two': 'Bucket 2',
        'three': 'Bucket 3',
    })

    assert shelf.get('one') == 'Bucket 1'


def test_multi_dimensional_shelf():
    shelf_a = IntervalShelf([
        ([0, 10], 'Bucket A-1'),
        ([11, 20], 'Bucket A-2'),
    ])

    shelf_b = IntervalShelf([
        ([0, 10], 'Bucket B-1'),
        ([11, 20], 'Bucket B-2'),
    ])

    named_shelf = NamedShelf([
        ('shelf a', shelf_a),
        ('shelf b', shelf_b)
    ])

    assert named_shelf.get_multi('shelf a', 15) == 'Bucket A-2'
    assert named_shelf.get_multi('shelf b', 10) == 'Bucket B-1'

    with pytest.raises(UnknownDimension):
        named_shelf.get_multi('shelf b', 10, '1234')


def test_real_life_example():
    """
    Number of pushups per age (male).
    |-------------|-----------|---------------|---------|
    | Age / Grade | excellent | above average | average |
    |-------------|-----------|---------------|---------|
    |  20-29      |  > 54     |  45-54        |  35-44  |
    |-------------|-----------|---------------|---------|
    |  30-39      |  > 44     |  35-44        |  24-34  |
    |-------------|-----------|---------------|---------|
    |  40-49      |  > 39     |  30-39        |  20-29  |
    |-------------|-----------|---------------|---------|
    """

    male_20_29_shelf = IntIntervalShelf([
        ('[35, 44]', 'average'),
        ('[45, 54]', 'above average'),
        ('(54, )', 'excellent'),
    ])

    male_30_39_shelf = IntIntervalShelf([
        ('[24, 34]', 'average'),
        ('[35, 44]', 'above average'),
        ('(44, )', 'excellent'),
    ])

    age_shelf = IntIntervalShelf([
        ('[20, 29]', male_20_29_shelf),
        ('[30, 39]', male_30_39_shelf),
    ])

    pushups = NamedShelf()
    pushups.add('male', age_shelf)

    # male, 24 years old, 42 pushups
    assert pushups.get_multi('male', 24, 42) == 'average'


def test_int_shelf_with_indexing():
    shelf = IntIntervalShelf([
        ([0, 10], 'Bucket 1'),
        ('(10, 20]', 'Bucket 2'),
    ])

    shelf['[30, )'] = 'Bucket 3'

    assert shelf[5] == 'Bucket 1'
    assert shelf[35] == 'Bucket 3'
    with pytest.raises(BucketDoesNotExists):
        assert shelf[-5]


def test_named_shelf_with_indexing():
    shelf = NamedShelf([
        ('a', 'Bucket 1'),
        ('b', 'Bucket 2'),
    ])

    shelf['c'] = 'Bucket 3'

    assert shelf['a'] == 'Bucket 1'
    assert shelf['c'] == 'Bucket 3'
    with pytest.raises(BucketDoesNotExists):
        assert shelf['e']


def test_float_shelf():
    shelf = FloatIntervalShelf([
        ('[0, 4.5]', 'Bucket 1'),
        ('(4.5, 5.6]', 'Bucket 2'),
    ])

    assert shelf[2.3] == 'Bucket 1'
    assert shelf[4.8] == 'Bucket 2'
