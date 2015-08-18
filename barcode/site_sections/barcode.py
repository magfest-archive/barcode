from barcode import *
from barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode

# TODO: restrict to just admins for this stuff, probably.
@all_renderable(c.PEOPLE)
class Root:
    def allotments(self):
        badge_num = 3

        encrypted = generate_barcode_from_badge_num(
            badge_num=badge_num,
            event_id=config['secret']['barcode_event_id'],
            salt=config['secret']['barcode_salt'],
            key=bytes(config['secret']['barcode_key'],'ascii'))

        decrypted = get_badge_num_from_barcode(
            barcode_num=encrypted,
            event_id=config['secret']['barcode_event_id'],
            salt=config['secret']['barcode_salt'],
            key=bytes(config['secret']['barcode_key'],'ascii'))

        return "badge_num = " + decrypted
