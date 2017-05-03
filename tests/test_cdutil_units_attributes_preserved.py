import cdms2
import cdutil
import unittest
import cdat_info
import os

class CDUTIL(unittest.TestCase):
    def testPreserveAttributes(self):
        f=cdms2.open(os.path.join(cdat_info.get_sampledata_path(),"clt.nc"))
        s=f("clt")
        s.Jill  = "Jill"
        AA = cdutil.region.AAZ()
        s2=s(AA)
        self.assertTrue(hasattr(s2,"units"))
        self.assertTrue(hasattr(s2,"Jill"))
        self.assertEqual(s.units,s2.units)
        self.assertEqual(s.Jill,s2.Jill)

