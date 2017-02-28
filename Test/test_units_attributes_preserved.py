import cdms2
import cdutil
import vcs
vcs.download_sample_data_files
f=cdms2.open(vcs.sample_data+"/clt.nc")
s=f("clt")
s.Jill  = "Jill"
AA = cdutil.region.AAZ()
s2=s(AA)
print s.units
print s2.Jill
print s2.units

