import argparse


# Custom argparse type representing a bounded int
class IntRange:

    def __init__(self, imin=None, imax=None):
        self.imin = imin
        self.imax = imax

    def __call__(self, arg):
        try:
            value = int(arg)
        except ValueError:
            raise self.exception()
        if (self.imin is not None and value < self.imin) or \
            (self.imax is not None and value > self.imax):
            raise self.exception()
        return value

    def exception(self):
        if self.imin is not None and self.imax is not None:
            return argparse.ArgumentTypeError(
                "Must be an integer in the range [{}, {}]".format(
                    self.imin,self.imax
                )
            )
        elif self.imin is not None:
            return argparse.ArgumentTypeError(
                "Must be an integer >= {}".format(self.imin)
            )
        elif self.imax is not None:
            return argparse.ArgumentTypeError(
                "Must be an integer <= {}".format(self.imax)
            )
        else:
            return argparse.ArgumentTypeError("Must be an integer")
