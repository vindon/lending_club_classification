import pytest

import lcdataformat.dataformats as dfmt


def test_rate_format():
    assert dfmt.parse_float_with_percent('15.5%') == 15.5


def test_rate_format_exception():
    with pytest.raises(ValueError):
        dfmt.parse_float_with_percent(None)


def test_member_id_truncate():
    assert dfmt.trunc_member_id_to_int(70681.0) == 70681


def test_member_id_exception():
    with pytest.raises(ValueError):
        dfmt.trunc_member_id_to_int(None)


def test_emp_length_format_0():
    assert dfmt.convert_less_than_yr_to_zero_or_num_otherwise('< 1 year') == 0


def test_emp_legnth_format_non0():
    assert dfmt.convert_less_than_yr_to_zero_or_num_otherwise('5 years') == 5


def test_emp_legnth_format_non1():
    assert dfmt.convert_less_than_yr_to_zero_or_num_otherwise('10+ years') == 10
