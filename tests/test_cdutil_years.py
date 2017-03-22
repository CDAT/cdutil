#!/usr/bin/env python
# Adapted for numpy/ma/cdms2 by convertcdms.py
import unittest
import cdms2,cdutil,sys,os,numpy,cdat_info
cdms2.setAutoBounds('on')

class CDUTIL(unittest.TestCase):
    def testYears(self):
        f = cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'th_yr.nc'))
        th=f('th',time=slice(-3,None,1))
        t=th.getTime()
        cdutil.setTimeBoundsYearly(t)

        self.assertEqual(th.shape,(3,64,128))
        self.assertTrue(numpy.equal(th.getTime().getBounds()[0],[1997.,1998.]).all())
        dep=cdutil.YEAR.departures(th,statusbar=None)
        self.assertEqual(dep.shape,(3, 64, 128))
