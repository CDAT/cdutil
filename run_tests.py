#!/usr/bin/env python
import os
import sys
import cdat_info

test_suite_name = 'cdutil'

workdir = os.path.dirname(os.path.realpath(__file__))
runner = cdat_info.TestRunnerBase(test_suite_name, get_sample_data=True)
ret_code = runner.run(workdir)

sys.exit(ret_code)

