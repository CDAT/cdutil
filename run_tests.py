import sys
import os
import argparse
import multiprocessing

#                                                                                                                                    
# TEMPORARY -- REVISIT                                                                                                               
#                                                                                                                                    
#sys.path.append("/Users/muryanto1/repos/cdat_info/Lib")

from cdat_info.Util import *
from cdat_info.Const import *

import cdat_info.TestRunnerBase

test_suite_name = 'cdutil'

parser = argparse.ArgumentParser(description="Run {n} tests".format(n=test_suite_name),
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

valid_options = 0x00000000
valid_options |= OPT_GENERATE_HTML
valid_options |= OPT_PACKAGE_RESULT
valid_options |= OPT_FAILED_ONLY
valid_options |= OPT_VERBOSITY
valid_options |= OPT_NCPUS
add_arguments(parser, valid_options)

args = parser.parse_args()
workdir = os.getcwd()
get_sample_data = True

runner = TestRunnerBase.TestRunnerBase(test_suite_name, valid_options, args, get_sample_data)
runner.run(workdir, args.tests)




