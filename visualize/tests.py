from django.test import TestCase
from .models import County, State, GuardianCounted, Item, Crime


class CountyTestCase(TestCase):
    def setup(self):
        pass

    def test_counties_have_attributes(self):
        cali = County(county_name='Orange County',
                      state='California',
                      FIPS='06059',
                      pop_est_2015=9999999,
                      pop_est_2014=8888888,
                      pop_est_2013=7777777,
                      pop_est_2012=6666666,
                      pop_est_2011=5555555,
                      pop_est_2010=4444444,
                      pop_est_2009=3333333,
                      pop_est_2008=2222222,
                      pop_est_2007=1111111,
                      pop_est_2006=999999,
                      pop_est_2005=888888,
                      pop_est_2004=777777,
                      pop_est_2003=666666,
                      pop_est_2002=555555,
                      pop_est_2001=444444,
                      pop_est_2000=333333,
                      google_county_name='Orange County')
        carolina = County(county_name='Orange County',
                          state='North Carolina',
                          FIPS='37135',
                          pop_est_2015=9999999,
                          pop_est_2014=8888888,
                          pop_est_2013=7777777,
                          pop_est_2012=6666666,
                          pop_est_2011=5555555,
                          pop_est_2010=4444444,
                          pop_est_2009=3333333,
                          pop_est_2008=2222222,
                          pop_est_2007=1111111,
                          pop_est_2006=999999,
                          pop_est_2005=888888,
                          pop_est_2004=777777,
                          pop_est_2003=666666,
                          pop_est_2002=555555,
                          pop_est_2001=444444,
                          pop_est_2000=333333,
                          google_county_name='Orange County')
        cali.save()
        carolina.save()
        the_oc = County.objects.get(state='California', county_name='Orange County')
        chapel_hill = County.objects.get(state='North Carolina', google_county_name='Orange_County')
        self.assertEqual(the_oc.FIPS, '06059')
        self.assertEqual(chapel_hill.pop_est_2014, 8888888)
