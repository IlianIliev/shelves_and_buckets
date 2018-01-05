class DoesNotExists(Exception):
    pass


class BucketDoesNotExists(DoesNotExists):
    pass


class UnknownDimension(DoesNotExists):
    pass


class IntervalsOverlap(Exception):
    pass


class IntervalsDoesNotConnect(Exception):
    pass
