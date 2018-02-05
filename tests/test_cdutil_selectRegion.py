import cdutil
import cdat_info
import cdms2
import cdms2,cdutil,sys,MV2,numpy,os,cdat_info
import unittest
import numpy
import tempfile

class CDUTIL(unittest.TestCase):

    def testRegions(self):

        # ------------------------------------------------------
        # Copy stdout and stderr file descriptor for cmor output
        # ------------------------------------------------------
        newstdout = os.dup(1)
        newstderr = os.dup(2)
        # --------------
        # Create tmpfile
        # --------------
        tmpfile = tempfile.mkstemp()

        os.dup2(tmpfile[0], 1)
        os.dup2(tmpfile[0], 2)
        os.close(tmpfile[0])
        regionNA = cdutil.region.domain(latitude=(-50.,50.,'ccb'))
        f=cdms2.open(cdat_info.get_sampledata_path()+'/clt.nc')
        d=f('u', regionNA)

        os.dup2(newstdout, 1)
        os.dup2(newstderr, 2)
        sys.stdout = os.fdopen(newstdout, 'w', 0)
        sys.stderr = os.fdopen(newstderr, 'w', 0)
        # --------------------------------------------------------
        # makesure the warning has been displayed for the 3rd args
        # --------------------------------------------------------
        f = open(tmpfile[1], 'r')
        lines = f.readlines()
        for line in lines:
            if line.find('warnings') != -1:
                break
        f.close()
        os.unlink(tmpfile[1])

        self.assertIn('warnings', line.strip())
        bounds = d.getLatitude().getBounds()
        self.assertTrue(numpy.allclose(bounds[0], numpy.array([-50., -49.19124603])))
        self.assertTrue(numpy.allclose(bounds[-1], numpy.array([49.19124603,  50.])))

if __name__ == "__main__":
    unittest.main()

