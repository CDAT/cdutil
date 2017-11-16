
import cdms2,cdutil,os,sys,numpy,cdat_info
import unittest

class CDUTIL(unittest.TestCase):
    def testDailyBounds(self):
        ## Test 6h data
        f=cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'psl_6h.nc'))
        s=f('psl')

        t=s.getTime()
        print('6 hourly data, before:')
        self.assertIsNone(t.getBounds())

        cdutil.times.setTimeBoundsDaily(t,4)
        print('6 hourly data, after:')
        self.assertTrue(numpy.allclose(t.getBounds()[:8],numpy.array([[  0.,   6.],
           [  6.,  12.],
            [ 12.,  18.],
             [ 18.,  24.],
              [ 24.,  30.],
               [ 30.,  36.],
                [ 36.,  42.],
                 [ 42.,  48.]])))

        ## test daily
        f=cdms2.open(os.path.join(cdat_info.get_sampledata_path(),'ts_da.nc'))
        s=f('ts')
        t=s.getTime()
        print('daily data, before:')
        self.assertIsNone(t.getBounds())

        cdutil.times.setTimeBoundsDaily(s,1)

        print('daily data, after:')
        self.assertTrue(numpy.allclose(t.getBounds()[:8],numpy.array([[ 7665.,  7666.],
           [ 7666.,  7667.],
            [ 7667.,  7668.],
             [ 7668.,  7669.],
              [ 7669.,  7670.],
               [ 7670.,  7671.],
                [ 7671.,  7672.],
                 [ 7672.,  7673.]])))

