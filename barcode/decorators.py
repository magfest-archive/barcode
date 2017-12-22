from barcode.barcode_utils import get_badge_num_from_barcode


def check_for_encrypted_badge_num(func):
    """
    On some pages, we pass a 'badge_num' parameter that might EITHER be a literal
    badge number or an encrypted value (i.e., from a barcode scanner). This
    decorator searches for a 'badge_num' parameter and decrypts it if necessary.
    """

    @wraps(func)
    def with_check(*args, **kwargs):
        if kwargs.get('badge_num', None):
            try:
                int(kwargs['badge_num'])
            except Exception:
                kwargs['badge_num'] = get_badge_num_from_barcode(barcode_num=badge_num)['badge_num']
        return func(*args, **kwargs)

    return with_check
