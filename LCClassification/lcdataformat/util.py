import os

import pandas as pd
import numpy as np
import datetime
import re
import logging
from time import time
from dateutil import relativedelta
from functools import wraps

try:
    import cpickle as pickle
except:
    import pickle


def convert_to_float(val):
    return float(val)


def parse_float_with_percent(rate):
    if pd.isnull(rate) == False:
        return float(re.sub('[%]', '', rate))
    else:
        return (float(0.0))


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
        if emp_years == 'n/a':
            return 0
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


def ret_string_len_if_str_zero_ifnot(x):
    if isinstance(x, str):
        return len(x)
    else:
        return 0


def convert_to_date(x):
    if isinstance(x, str):
        grps = x.split('-')
        mon = grps[0]
        year = grps[1]
        day = '01'
        date_str = day + '/' + mon + '/' + year
        my_date = datetime.datetime.strptime(day + '/' + mon + '/' + year, "%d/%b/%Y")
        return my_date


def find_length_diff_in_months(dt2, dt1):
    logging.debug(dt2)
    logging.debug(dt2)
    logging(type(dt1))
    logging(type(dt2))
    if pd.isnull(dt1) == False and pd.isnull(dt2) == False:
        return relativedelta.relativedelta(dt2, dt1).months


def timed(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        elapsed = time() - start
        logging.info("Time Taken for executing %s is %d sec " % (f.__name__, elapsed))
        return result

    return wrapper


def memoize(f):
    @wraps(f)
    def new_f(*args, **kwargs):
        compressed = ''
        if len(args) > 0:
            compressed = '_' + '_'.join([str(arg)[:10] for arg in args])
        if len(kwargs) > 0:
            compressed += '_' + '_'.join([(str(k) + str(v))[:10] for k, v in kwargs])

        filename = '%s%s.pickle' % (f.__name__, compressed)

        if os.path.exists(filename):
            pickled = open(filename, 'rb')
            result = pickle.load(pickled)
            pickled.close()
        else:
            result = f(*args, **kwargs)
            pickled = open(filename, 'wb')
            pickle.dump(result, pickled)
            pickled.close()

    new_f.__name__ = f.__name__
    new_f.__doc__ = f.__doc__

    return new_f
