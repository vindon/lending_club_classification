import pandas as pd
import numpy as np
import datetime
import re


def convert_to_float(val):
    return float(val)


def format_interest_rate(rate):
    if rate is not None:
        return float(re.sub('[%]', '', rate))
    else:
        raise ValueError("Got Null, value expected")


def trunc_member_id_to_int(member_id):
    if member_id is not None:
        return int(member_id)
    else:
        raise ValueError("Memeber ID is null")


def strip_non_numeric_and_parse(x):
    try:
        return float(re.sub(r'[^0-9\.]', '', x))
    except ValueError:
        return 0.0


def convert_less_than_yr_to_zero_or_num_otherwise(emp_years):
    if emp_years is not None:
        emp_years = emp_years.strip()
        m = re.search(r'(\< ?)(\d{1,2})\+? years?', emp_years)
        if m:
            if m.group(1).strip() == '<' and m.group(2) == '1':
                return 0
            return int(m.group(2))
        else:
            m = re.search(r'(\d{1,2})\+? years?', emp_years)
            if m:
                return int(m.group(1))

        raise ValueError("Invalid value for emp_years , got " + emp_years)


def parse_date(x, format='%Y-m-d'):
    d = datetime.strptime(x, format)


def parse_date_to_period(x):
    if x is not None:
        return pd.Period(x, 'M')
