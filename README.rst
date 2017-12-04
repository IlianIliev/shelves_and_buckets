===================
Shelves and Buckets
===================


.. image:: https://img.shields.io/pypi/v/shelves_and_buckets.svg
        :target: https://pypi.python.org/pypi/shelves_and_buckets

.. image:: https://img.shields.io/travis/lifesum/shelves_and_buckets.svg
        :target: https://travis-ci.org/lifesum/shelves_and_buckets

.. image:: https://readthedocs.org/projects/shelves-and-buckets/badge/?version=latest
        :target: https://shelves-and-buckets.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status

.. image:: https://pyup.io/repos/github/lifesum/shelves_and_buckets/shield.svg
     :target: https://pyup.io/repos/github/lifesum/shelves_and_buckets/
     :alt: Updates


Shelves and buckets is a small package for easier work with grouped data or data ranges. It originates from the need to easily find data in multidimensional space using intervals. Lets look at the following examples:

* Free software: MIT license
* Documentation: https://shelves-and-buckets.readthedocs.io.


Features
--------

Interval shelves are using the intervals_ package

.. _intervals: https://pypi.python.org/pypi/intervals

 - IntIntervalShelf - interval boundaries are integers
 - NamedShelf - takes a dictionary as input and behaves similarly but could be combined with other shelves


Examples
--------

Consider the following data for physical state based on number of pushups a person can make

    +------------+------+-----------+-----------+
    + Pushup     + <20  | 21 - 40   | 41+       +
    +============+======+===========+===========+
    + Grade      + Poor | Average   | Excellent +
    +------------+------+-----------+-----------+


How to find in which group the user belongs based on their score::

    >>> from shelves_and_buckets import IntIntervalShelf
    >>> shelf = IntIntervalShelf([
            ('(, 20]', 'poor'),
            ('[21, 40]', 'average'),
            ('[41, )', 'excellent'),
        ])
    >>> shelf.get(5)
    'poor'
    >>> shelf.get(25)
    'average

Ok, let's take a look at a bit more complicated example, what if we have another dimension e.g. the age of the person.

    +-------------+-----------+---------------+---------+
    + Age / Grade + excellent + above average + average +
    +=============+===========+===============+=========+
    +  20-29      +  > 54     +  45-54        +  35-44  +
    +-------------+-----------+---------------+---------+
    +  30-39      +  > 44     +  35-44        +  24-34  +
    +-------------+-----------+---------------+---------+
    +  40-49      +  > 39     +  30-39        +  20-29  +
    +-------------+-----------+---------------+---------+

Example::

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

    >>> age_shelf.get_multi(24, 42)  # value are passed from the outer shelves in, in this case -> age, pushups
    'average'


Shelves also support usage with indexing for adding and getting buckets::

    shelf = IntIntervalShelf()
    shelf[[0, 10]] = 'Bucket A'
    shelf[[11, 20]] = 'Bucket B'
    >>> shelf[5]
    'Bucket A'


TODOs
-----

    - Add check for intervals overlap
    - Add option to avoid holes between intervals
    - Add option to pass directly Interval object when creating bucket
    - Consider using bisect for faster search in intervals http://www.ilian.io/working-with-intervals-in-python/

Credits
---------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage

This package uses Intervals_ by `Konsta Vesterinen`_

.. _`Konsta Vesterinen`: https://github.com/kvesteri
