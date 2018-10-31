from setuptools import setup, find_packages
from subprocess import Popen, PIPE


Version = "8.0"
p = Popen(
    ("git",
     "describe",
     "--tags"),
    stdin=PIPE,
    stdout=PIPE,
    stderr=PIPE)
try:
    descr = p.stdout.readlines()[0].strip().decode("utf-8")
    Version = "-".join(descr.split("-")[:-2])
    if Version == "":
        Version = descr
except:
    descr = Version

setup (name = "cdutil",
       author="AIMS Software Team",
       version=descr,
       description = "Utilities for climate data manipulation",
       url = "http://cdat.sourceforge.net",
       packages = find_packages(),
       data_files = [ ("share/cdutil",("data/sftbyrgn.nc","data/navy_land.nc","share/test_data_files.txt"))],
      )
    
