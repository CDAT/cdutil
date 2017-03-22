#!/usr/bin/env python
# Adapted for numpy/ma/cdms2 by convertcdms.py

import cdtime,cdms2,os,cdat_info
import cdutil
import MV2
import unittest
import numpy

class CDUTIL(unittest.TestCase):
    def setUp(self):
        var='tas'
        cdms2.setAutoBounds('on')

        self.f   = cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'tas_mo.nc'))
        self.tas_mo = self.f(var)
        cdutil.times.setTimeBoundsMonthly(self.tas_mo)

    def tearDown(self):
        self.f.close()

    def testTimes(self):
        fsc = cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'tas_mo_clim.nc'))

        print "Step #0 : Reading data"
        s=self.f('tas',longitude=(0,360,'co'))

        acok=fsc('climseas',longitude=(0,360,'co'))

        print 'Test #1 : Test result'

        ac=cdutil.times.JAN.climatology(s)

        self.assertTrue(MV2.allclose(ac[0],acok[0]))

        fsc.close()

        a=cdtime.comptime(1980)
        b=cdtime.comptime(1980,5)

        f = cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'tas_6h.nc'))
        s=f('tas',time=(a,b,'co'),squeeze=1)

        print "Test #2 : 6hourly AND get"
        jans=cdutil.times.JAN(s)

        print "Test #3 : climatology 6h"
        JFMA=cdutil.times.Seasons('JFMA')
        jfma=JFMA.climatology(s)


        #Test reorder
        print "Test #4 : time not first axis"
        jfma=JFMA.climatology(s(order='x...'))
        print "Test 4b: Result ok ?"
        self.assertEqual(jfma.getOrder()[0], 'x')

    def testTimes2(self):

        a=MV2.masked_array(MV2.array([0,0,0,0,0,0,0,0,0,0,0,0]),[0,1,1,1,1,1,1,1,1,1,1,0])
        bounds=numpy.ma.array(
            [[0,31],
             [31,59],
             [59,90],
             [90,120],
             [120,151],
             [151,181],
             [181,212],
             [212,243],
             [243,273],
             [273,304],
             [304,334],
             [334,365]]
            )
        ax=a.getAxis(0)
        ax.setBounds(bounds)
        #print cdutil.times.centroid(a,[-10,30]) 
        print 'Centroid Normal:',cdutil.times.centroid(a,[0,365]) 
        print 'Centroid Cyclic:',cdutil.times.cyclicalcentroid(a,[0,365]) 


        djf=cdutil.DJF(self.tas_mo)
        djf=cdutil.DJF(self.tas_mo,criteriaarg=[.8,0.0001])
        djf=cdutil.ANNUALCYCLE.climatology(self.tas_mo)
        djf=cdutil.YEAR.departures(self.tas_mo)

    def testTimes3(self):
        
        tc=self.tas_mo.getTime().asComponentTime()

        print tc[0],tc[-1]

        ref=cdutil.ANNUALCYCLE.climatology(self.tas_mo(time=('1980','1985','co')))
        dep=cdutil.ANNUALCYCLE.departures(self.tas_mo)
        ref=ref(order='y...')
        dep=cdutil.ANNUALCYCLE.departures(self.tas_mo,ref=ref)
        # testing that an ma in worng order would fail
        try:
            dep=cdutil.ANNUALCYCLE.departures(self.tas_mo,ref=ref(order='t...').filled())
            raise RuntimeError( "Should have failed with ma passed as ref (not mv2)")
        except:
          pass
