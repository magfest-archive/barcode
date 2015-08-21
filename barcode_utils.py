from barcode import *

import base64
import struct
import skip32
import code128
import os


# TODO: currently broken, need to rewrite in the context of uber
def generate_barcode_csv(filename):
    badge_types = self.badge_types['badge_types']

    # TODO: modify so we read the config directly from uber.
    lines = []
    for badge_type, ranges in badge_types.items():
        range_start = int(ranges['range_start'])
        range_end = int(ranges['range_end'])
        lines = lines + self.generate_barcode_nums(range_start, range_end)

    f = open(filename,'w')

    for line in lines:
        f.write(line + os.linesep)

    f.close()


# TODO: currently broken, need to rewrite in the context of uber
def generate_barcode_nums(range_start, range_end):
    generated_lines = []
    seen_barcodes = []
    for badge_num in range(range_start, range_end+1):
        barcode_num = generate_barcode_from_badge_num(
            badge_num=int(badge_num),
            event_id=self.event_id,
            salt=self.salt,
            key=self.secret_key
        )

        line = "{badge_num},{barcode_num}".format(
            badge_num=badge_num,
            barcode_num=barcode_num,
        )
        generated_lines.append(line)

        # ensure that we haven't seen this value before
        if barcode_num in seen_barcodes:
            raise ValueError('COLLISION: generated a badge# that\'s already been seen')
        else:
            seen_barcodes.append(barcode_num)

    return generated_lines


def generate_barcode_from_badge_num(badge_num, event_id=None, salt=None, key=None):
    event_id = config['secret']['barcode_event_id'] if not event_id else event_id
    salt = config['secret']['barcode_salt'] if not salt else salt
    key = bytes(config['secret']['barcode_key'],'ascii') if not key else key

    # packed data going to be encrypted is:
    # byte 1 - 8bit event ID, usually 1 char
    # byte 2,3,4 - 24bit badge number

    salted_val = badge_num + (0 if not salt else salt)

    if salted_val > 0xFFFFFF:
        raise ValueError("badge_number is too high " + str(badge_num))

    data_to_encrypt = struct.pack('>BI', event_id, salted_val)

    # remove the highest byte in that integer (2nd byte)
    data_to_encrypt = bytearray([data_to_encrypt[0], data_to_encrypt[2], data_to_encrypt[3], data_to_encrypt[4]])

    if len(data_to_encrypt) != 4:
        raise ValueError("data to encrypt should be 4 bytes")

    if len(key) != 10:
        raise ValueError("key length should be exactly 10 bytes")

    encrypted_string = _barcode_raw_encrypt(data_to_encrypt, key=key)

    # check to make sure it worked.
    decrypted = get_badge_num_from_barcode(encrypted_string, salt, key)
    if decrypted['badge_num'] != badge_num or decrypted['event_id'] != event_id:
        raise ValueError("didn't encode correctly")

    # check to make sure this barcode number is valid for Code 128 barcode
    verify_barcode_is_valid_code128(encrypted_string)

    return encrypted_string


def get_badge_num_from_barcode(barcode_num, salt=None, key=None):
    salt = config['secret']['barcode_salt'] if not salt else salt
    key = bytes(config['secret']['barcode_key'],'ascii') if not key else key

    decrypted = _barcode_raw_decrypt(barcode_num, key=key)

    result = dict()

    result['event_id'] = struct.unpack('>B', bytearray([decrypted[0]]))[0]

    badge_bytes = bytearray(bytes([0, decrypted[1], decrypted[2], decrypted[3]]))
    result['badge_num'] = struct.unpack('>I', badge_bytes)[0] - salt

    return result


def verify_barcode_is_valid_code128(encrypted_string):
    for c in encrypted_string:
        if c not in code128._charset_b:
            raise ValueError("contains a char not valid in a code128 barcode")


def _barcode_raw_encrypt(value, key):
    if len(value) != 4:
        raise ValueError("invalid barcode input: needs to be exactly 4 bytes")

    # skip32 generates 4 bytes output from 4 bytes input
    _encrypt = True
    skip32.skip32(key, value, _encrypt)

    # raw bytes aren't suitable for a Code 128 barcode though,
    # so convert it to base58 encoding
    # which is just some alphanumeric and numeric chars and is
    # designed to be vaguely human.  this takes our 4 bytes and turns it into 6 chars
    encrypted_value = base64.encodebytes(value).decode('ascii')

    # important note: because we are not an even multiple of 3 bytes, base64 needs to pad
    # the resulting string with equals signs.  we can strip them out knowing that our length is 4 bytes
    # IF YOU CHANGE THE LENGTH OF THE ENCRYPTED DATA FROM 4 BYTES, THIS WILL NO LONGER WORK.
    encrypted_value = encrypted_value.replace('==\n', '')

    if len(encrypted_value) != 6:
        raise ValueError("Barcode encryption failure: result should be 6 characters")

    return encrypted_value


def _barcode_raw_decrypt(value, key):
    # raw bytes aren't suitable for a Code 128 barcode though,
    # so convert it to base64 encoding
    # which is just some alphanumeric and numeric chars and is
    # designed to be vaguely human.  this takes our 4 bytes and turns it into 6ish bytes

    # important note: because we are not an even multiple of 3 bytes, base64 needs to pad
    # the resulting string with equals signs.  we can strip them out knowing that our length is 4 bytes
    # IF YOU CHANGE THE LENGTH OF THE ENCRYPTED DATA FROM 4 BYTES, THIS WILL NO LONGER WORK.

    if len(value) != 6:
        raise ValueError("Barcode decryption failure: result should be 6 characters")

    value += '==\n'

    decoded = base64.decodebytes(value.encode('ascii'))

    # skip32 generates 4 bytes output from 4 bytes input
    _encrypt = False
    decrytped = bytearray(decoded)
    skip32.skip32(key, decrytped, _encrypt)

    if len(decrytped) != 4:
        raise ValueError("invalid barcode input: needs to be exactly 4 bytes")

    return decrytped
