.PHONY: conda-info conda-list setup-build setup-tests conda-rerender \
	conda-build conda-upload conda-dump-env \
	run-tests run-coveralls

SHELL = /bin/bash

os = $(shell uname)
pkg_name = cdutil

user ?= cdat
label ?= nightly

build_script = conda-recipes/build_tools/conda_build.py

test_pkgs = testsrunner coverage coveralls
last_stable ?= 8.2.1

conda_build_env ?= build-$(pkg_name)
conda_test_env ?= test-$(pkg_name)

workdir ?= $(PWD)/workspace
branch ?= $(shell git rev-parse --abbrev-ref HEAD)
extra_channels ?= cdat/label/nightly conda-forge
conda ?= $(or $(CONDA_EXE),$(shell find /opt/*conda*/bin $(HOME)/*conda* -type f -iname conda))
artifact_dir ?= $(PWD)/artifacts
conda_env_filename ?= spec-file

ifeq ($(coverage),1)
coverage_opt = -c tests/coverage.json --coverage-from-egg
endif

conda_recipes_branch ?= master

conda_base = $(patsubst %/bin/conda,%,$(conda))
conda_activate = $(conda_base)/bin/activate

conda_build_extra = --copy_conda_package $(artifact_dir)/

ifndef $(local_repo)
local_repo = $(dir $(realpath $(firstword $(MAKEFILE_LIST))))
endif

conda-info:
	source $(conda_activate) $(conda_test_env); conda info

conda-list:
	source $(conda_activate) $(conda_test_env); conda list

setup-build:
ifeq ($(wildcard $(workdir)/conda-recipes),)
	git clone -b $(conda_recipes_branch) https://github.com/CDAT/conda-recipes $(workdir)/conda-recipes
else
	cd $(workdir)/conda-recipes; git pull
endif

setup-tests:
	source $(conda_activate) base; conda create -y -n $(conda_test_env) --use-local \
		$(foreach x,$(extra_channels),-c $(x)) $(pkg_name) $(foreach x,$(test_pkgs),"$(x)") \
		$(foreach x,$(extra_pkgs),"$(x)")

conda-rerender: setup-build 
	python $(workdir)/$(build_script) -w $(workdir) -l $(last_stable) -B 0 -p $(pkg_name) \
		-b $(branch) --do_rerender --conda_env $(conda_build_env) --ignore_conda_missmatch \
		--conda_activate $(conda_activate)

conda-build:
	mkdir -p $(artifact_dir)

	python $(workdir)/$(build_script) -w $(workdir) -p $(pkg_name) --build_version noarch \
		--do_build --conda_env $(conda_build_env) --extra_channels $(extra_channels) \
		--conda_activate $(conda_activate) $(conda_build_extra)

conda-upload:
	source $(conda_activate) $(conda_build_env); \
		anaconda -t $(conda_upload_token) upload -u $(user) -l $(label) --force $(artifact_dir)/*.tar.bz2

conda-dump-env:
	mkdir -p $(artifact_dir)

	source $(conda_activate) $(conda_test_env); conda list --explicit > $(artifact_dir)/$(conda_env_filename).txt

run-tests:
	source $(conda_activate) $(conda_test_env); python run_tests.py -H -v2 $(coverage_opt)

run-coveralls:
	source $(conda_activate) $(conda_test_env); coveralls;
