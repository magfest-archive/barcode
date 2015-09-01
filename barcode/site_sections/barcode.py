from barcode import *
from barcode.barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode

@all_renderable(c.PEOPLE)
class Root:
    def index(self):
        return {}

    @ajax
    def get_badge_num_from_barcode(self, session, barcode):
        badge_num = -1
        msg = "Success."
        attendee = None
        try:
            # important note: a barcode encodes just a badge_number. however, that doesn't mean
            # that this badge# has been assigned to an attendee yet, so Attendee may come back as none
            # if they aren't checked in.
            badge_num = get_badge_num_from_barcode(barcode_num=barcode)['badge_num']
            attendee = session.attendee(badge_num=badge_num)
        except Exception as e:
            msg = "Failed: " + str(e)

        return {
            'message': msg,
            'badge_num': badge_num,
            'attendee_name': attendee.full_name if attendee else '',
            'attendee_id': attendee.id if attendee else -1,
        }
