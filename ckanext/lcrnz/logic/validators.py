import sys
import datetime

from ckan.plugins.toolkit import Invalid


def is_year(value):
    '''Validates value is the date format YYYY'''
    try:
        datetime.datetime.strptime(value, '%Y')
    except ValueError:
        raise Invalid("Year must be in the format YYYY, e.g. 2015")
    return value


def is_year_month(value):
    '''Validates value is in the date format YYYY-MM'''
    try:
        datetime.datetime.strptime(value, '%Y-%m')
    except ValueError:
        raise Invalid("Date must be in the format YYYY-MM, e.g. 2015-01")
    return value


def is_year_month_day(value):
    '''Validates value is in the date format YYYY-MM-DD'''
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
    except ValueError:
        raise Invalid("Date must be in the format YYYY-MM-DD, e.g. 2015-01-29")
    return value


def is_date(value):
    '''Validates value is in one of three various formats'''
    for m in ['is_year', 'is_year_month', 'is_year_month_day']:
        try:
            getattr(sys.modules[__name__], m)(value)
        except Invalid:
            pass
        else:
            return value

    raise Invalid("Date must be in the format YYYY-MM-DD, YYYY-MM, or YYYY")
