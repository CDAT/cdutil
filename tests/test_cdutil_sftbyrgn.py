# Adapted for numpy/ma/cdms2 by convertcdms.py
"""
This script converts a land sea mask to a stbyrgn mask
Input:
Land/sea mask
Original sftbyrgn
dctionary of values in sftbyrgn/type (ld or water)

Ouptput:
Newsftbyrgn
"""

import cdms2,cdutil,MV2,os,sys,cdat_info
import unittest
import numpy
numpy.set_printoptions(threshold='nan')
import pprint

class CDUTIL(unittest.TestCase):
    def testSftbyrgn(self):
        din=cdms2.open(os.path.join(cdat_info.get_sampledata_path(),"clt.nc"))("clt",slice(0,1))
        sftlf = cdutil.generateLandSeaMask(din)*100.
        newsftbyrgn,n=cdutil.generateSurfaceTypeByRegionMask(sftlf)

