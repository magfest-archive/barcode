import pytest
from barcode import *
from barcode_utils import generate_barcode_from_badge_num, get_badge_num_from_barcode


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
    assert 'badge_number is too high' in str(ex.value)

def test_fail_key_length(cfg, monkeypatch):
    monkeypatch.setitem(config['secret'], 'barcode_key', "X")
    with pytest.raises(ValueError) as ex:
        encrypted = generate_barcode_from_badge_num(badge_num=1)
    assert 'key length should be exactly' in str(ex.value)