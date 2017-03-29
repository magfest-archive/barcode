import pytest
from barcode import *
from barcode.barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode, assert_is_valid_rams_barcode


@pytest.fixture
def cfg(monkeypatch):
    config['secret'] = dict()
    config['secret']['barcode_key'] = "ABCDEF1234"
    config['secret']['barcode_salt'] = 42
    config['secret']['barcode_event_id'] = 0xFF


def test_cfg_fixtures(cfg):
    assert config['secret']['barcode_salt'] <= 1000000
    assert len(config['secret']['barcode_key']) == 10
    assert config['secret']['barcode_event_id'] <= 0xFF
    assert config['secret']['barcode_event_id'] == 0xFF


def test_encrypt_decrypt(cfg):
    badge_num = 3
    encrypted = generate_barcode_from_badge_num(badge_num=badge_num)

    assert len(encrypted) == 6
    decrypted = get_badge_num_from_barcode(barcode_num=encrypted)

    assert decrypted['badge_num'] == badge_num
    assert decrypted['event_id'] == config['secret']['barcode_event_id']


def test_fail_too_high_badges(cfg):
    with pytest.raises(ValueError) as ex:
        encrypted = generate_barcode_from_badge_num(badge_num=0xFFFFFF+1)
    assert 'either badge_number or salt is too large' in str(ex.value)


def test_fail_key_length(cfg, monkeypatch):
    monkeypatch.setitem(config['secret'], 'barcode_key', "X")
    with pytest.raises(ValueError) as ex:
        encrypted = generate_barcode_from_badge_num(badge_num=1)
    assert 'key length should be exactly' in str(ex.value)


def test_fail_wrong_event_id(cfg, monkeypatch):
    with pytest.raises(ValueError) as ex:
        barcode = generate_barcode_from_badge_num(badge_num=1, event_id=1)
        get_badge_num_from_barcode(barcode_num=barcode, event_id=2)
    assert "doesn't match our event ID" in str(ex.value)


def test_dontfail_wrong_event_id(cfg):
    badge_num = 78946
    barcode = generate_barcode_from_badge_num(badge_num=badge_num)
    decrytped = get_badge_num_from_barcode(barcode_num=barcode, event_id=2, verify_event_id_matches=False)
    assert decrytped['badge_num'] == badge_num
    assert decrytped['event_id'] == config['secret']['barcode_event_id']


def test_barcode_character_validations(cfg):
    # some valid barcodes
    for s in ["jhgsd+", "ABMN45", "asfnb/", "912765", "++//00"]:
        assert_is_valid_rams_barcode(s)

    # some invalid barcodes
    for s in ["^^^^^^", "(}(*&4", "---2hg", "{}{<>?", "      ", "ABCDEFGH", "abcdefgh", "1234567"]:
        with pytest.raises(ValueError) as ex:
            assert_is_valid_rams_barcode(s)
        assert 'barcode validation error' in str(ex.value)
