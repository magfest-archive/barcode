from barcode import *


# TODO: restrict to just admins for this stuff, probably.
@all_renderable(c.PEOPLE)
class Root:
    def allotments(self):
        return "TEST"
