# @version: python == 2

__all__ = []

red = lambda s: "\x1b[31m%s\x1b[0m" % s

# Sometimes I start Python 2 by mistake when python == python2
print red("You're using Python 2!")
