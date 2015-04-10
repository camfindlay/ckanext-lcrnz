from nose import tools as nosetools

from ckan.plugins import toolkit

import ckanext.lcrnz.logic.validators as validators


class TestDateValidators(object):

    def test_is_year(self):
        nosetools.assert_true(validators.is_year('2015'), '2015')

    def test_is_year_invalid_int(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year,
                                '215')

    def test_is_year_invalid_str(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year,
                                'YYYY')

    def test_is_year_invalid_date(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year,
                                '2015-12-30')

    def test_is_year_month(self):
        nosetools.assert_true(validators.is_year_month('2015-12'), '2015-12')

    def test_is_year_month_invalid_int(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month,
                                '215-1')

    def test_is_year_month_invalid_str(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month,
                                'YYYY-MM')

    def test_is_year_month_invalid_date(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month,
                                '2015-12-30')

    def test_is_year_month_day(self):
        nosetools.assert_true(validators.is_year_month_day('2015-12-29'),
                              '2015-12-29')

    def test_is_year_month_day_invalid_int(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month_day,
                                '215-1-0')

    def test_is_year_month_day_invalid_str(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month_day,
                                'YYYY-MM-DD')

    def test_is_year_month_day_invalid_date(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month_day,
                                '2015-29-12')

    def test_is_date_year(self):
        nosetools.assert_true(validators.is_date('2015'), '2015')

    def test_is_date_year_month(self):
        nosetools.assert_true(validators.is_date('2015-12'), '2015-12')

    def test_is_date_year_month_day(self):
        nosetools.assert_true(validators.is_date('2015-12-01'), '2015-12-01')

    def test_is_date_year_month_day_invalid_date(self):
        nosetools.assert_raises(toolkit.Invalid, validators.is_year_month_day,
                                '2015-29-12')
