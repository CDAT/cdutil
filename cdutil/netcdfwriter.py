# Adapted for numpy/ma/cdms2 by convertcdms.py
"""writenetcdf
   see also dataset write method
"""
import cdms2


def writenetcdf(slab, filename, mode="a"):
    """
    writenetcdf(slab, filename, mode="a") writes slab to the file.
    :param mode: One of 'a' append, or 'w'  replace
    :type mode: str

    :param slab: Anything :py:func:`cdms2.asVariable` will accept
    :type: see :py:func:`cdms2.asVariable`
    """
    if mode == 'r':
        mode = 'w'
    slab = cdms2.asVariable(slab, 0)
    f = cdms2.openDataset(filename, mode)
    f.write(slab)
    f.close()


if __name__ == '__main__':
    from numpy.ma import allclose
    import pcmdi
    g = cdms2.openDataset('clt.nc', 'r')
    c = g.variables['clt']
    t = cdms2.asVariable([1., 2., 3.])
    t.id = 't'
    writenetcdf(c, 'test.nc', 'w')
    writenetcdf(t, 'test.nc', 'a')
    f = cdms2.open('test.nc')
    d = f.variables['clt']
    assert allclose(c, d)
    for name in ['clt', 't']:
        pcmdi.slabinfo(f.variables[name])
