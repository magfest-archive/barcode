from barcode import *
from barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode

@all_renderable(c.PEOPLE)
class Root:
    def test(self):
        badge_num = 3
        encrypted = generate_barcode_from_badge_num(badge_num=badge_num)
        decrypted = get_badge_num_from_barcode(barcode_num=encrypted)

        return "badge_num = " + str(decrypted['badge_num']) + ", event_id = " + str(decrypted['event_id'])
