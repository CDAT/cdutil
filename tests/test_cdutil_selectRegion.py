import cdutil
import cdat_info
import cdms2
import cdms2,cdutil,sys,MV2,numpy,os,cdat_info
import unittest
import numpy
import tempfile

class CDUTIL(unittest.TestCase):

    def testRegions(self):

        regionNA = cdutil.region.domain(latitude=(-50.,50.,'ccb'))
        f=cdms2.open(cdat_info.get_sampledata_path()+'/clt.nc')
        d=f('u', regionNA)

        # --------------------------------------------------------
        # makesure the warning has been displayed for the 3rd args
        # --------------------------------------------------------

        bounds = d.getLatitude().getBounds()
        self.assertTrue(numpy.allclose(bounds[0], numpy.array([-50., -49.19124603])))
        self.assertTrue(numpy.allclose(bounds[-1], numpy.array([49.19124603,  50.])))

if __name__ == "__main__":
    unittest.main()

