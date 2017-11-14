from uber.api import all_token_auth, AttendeeLookup
from uber.server import register_jsonrpc
from barcode import *
from barcode.barcode_utils import get_badge_num_from_barcode


@all_token_auth(c.API_READ)
class BarcodeLookup:
    def lookup_attendee_from_barcode(self, barcode_value):
        with Session() as session:
            badge_num = -1
            try:
                result = get_badge_num_from_barcode(barcode_value)
                badge_num = result['badge_num']
            except Exception as e:
                return {'error': 'Couldn\'t look up barcode value: ' + str(e)}

            # note: a descrypted barcode can yield to a valid badge#, but an attendee may not have that badge#

            attendee = session.query(Attendee).filter_by(badge_num=badge_num).first()
            if attendee:
                return attendee.to_dict(AttendeeLookup.fields)
            else:
                return {'error': 'Valid barcode, but no attendee found with Badge #{}'.format(badge_num)}

    def lookup_badge_number_from_barcode(self, barcode_value):
        with Session() as session:
            try:
                result = get_badge_num_from_barcode(barcode_value)
                return {'badge_num': result['badge_num']}
            except Exception as e:
                return {'error': 'Couldn\'t look up barcode value: ' + str(e)}


register_jsonrpc(BarcodeLookup(), 'barcode')
