class DoesNotExists(Exception):
    pass


class BucketDoesNotExists(DoesNotExists):
    pass


class UnknownDimension(DoesNotExists):
    pass
