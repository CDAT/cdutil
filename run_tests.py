import os
from cdat_info import TestRunnerBase


test_suite_name = 'cdutil'

workdir = os.getcwd()

runner = TestRunnerBase(test_suite_name, get_sample_data=True)
runner.run(workdir)

