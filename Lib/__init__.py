"""Module cdutil contains miscellaneous routines for manipulating variables.
"""
from . import region
#import continent_fill
from genutil.averager import averager, AveragerError, area_weights, getAxisWeight, getAxisWeightByName,__check_weightoptions
from .times import * 
from .retrieve import WeightsMaker,  WeightedGridMaker, VariableConditioner, VariablesMatcher
from .vertical import sigma2Pressure, reconstructPressureFromHybrid, logLinearInterpolation, linearInterpolation
from .create_landsea_mask import generateLandSeaMask
from .sftbyrgn import generateSurfaceTypeByRegionMask
import cdat_info
cdat_info.pingPCMDIdb("cdat","cdutil")
