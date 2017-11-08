from __future__ import print_function
import cdtime
import cdms2
import MV2
import numpy
import cdutil
import unittest

class CDUTIL(unittest.TestCase):

    def mk_time(self,offset=0,length=120,units="months since 1800"):
        t=cdms2.createAxis(numpy.arange(offset,offset+length))
        t.designateTime()
        t.id='time'
        t.units=units
        data= MV2.array(numpy.random.random((length)))
        data.setAxis(0,t)
        cdutil.setTimeBoundsMonthly(t)
        print("TCCCCCP:",data.getTime().asComponentTime())
        return data,t,t.asComponentTime()

    def check(self,offset=0,midunits="months since 1801",units="months since 1800"):
        data,t,tc=self.mk_time(offset,units=units)
        units = t.units
        t1,t2 = tc[0],tc[-1]
        dep = cdutil.times.ANNUALCYCLE.departures(data)
        tc = dep.getTime().asComponentTime()
        print(t1,t2,tc[0],tc[-1])
        self.assertEqual( tc[0], t1)
        self.assertEqual( tc[-1], t2)
        self.assertEqual( data.getTime().units, units)
        self.assertEqual( dep.getTime().units, units)

    def testDepartureBounds(self):
        self.check()
        self.check(-200)
        self.check(-60)
        self.check(10)



