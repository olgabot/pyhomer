#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pyhomer
----------------------------------

Tests for `pyhomer` module.
"""

import os

import pytest
import pybedtools

@pytest.fixture
def foreground_filename():
    dirname = os.path.dirname(__file__)
    return  '{}/foreground.bed'.format(dirname)


@pytest.fixture(params=['BedTool', 'filename'])
def foreground(request, foreground_filename):
    if request.param == 'filename':
        return foreground_filename
    elif request.param == 'BedTool':
        return pybedtools.BedTool(foreground_filename)

@pytest.fixture
def background_filename():
    dirname = os.path.dirname(__file__)
    return  '{}/background.bed'.format(dirname)


@pytest.fixture(params=['BedTool', 'filename'])
def background(request, background_filename):
    if request.param == 'filename':
        return background_filename
    elif request.param == 'BedTool':
        return pybedtools.BedTool(background_filename)

@pytest.fixture(params=[None, "doesn't exist", "already exists"])
def out_dir(request):
    if request.param is None:
        return None
    elif request.param == "doesn't exist":
        return 'homer/'
    elif request.param == "already exists":
        return './'


@pytest.fixture(params=[None, '-rna -len 4,5,6 -mset vertebrates -mis 0 -p 4 '
                              '-noweight'])
def flags(request):
    return request.param


@pytest.fixture(params=[None, '~/bin/findMotifsGenome.pl'])
def findMotifsGenome(request):
    return request.param


@pytest.fixture(params=[True, False])
def force(request):
    return request.param


@pytest.fixture(params=[None, 'mm10'])
def genome(request):
    return request.param


def test_construct_homer_command(foreground_filename, background_filename,
                                 flags, findMotifsGenome, out_dir, force,
                                 genome):
    import pyhomer

    kwargs = dict(flags=flags, findMotifsGenome=findMotifsGenome,
                  out_dir=out_dir, force=force, genome=genome)
    kwargs = dict(filter(lambda x: x[1] is not None, kwargs.items()))

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename, **kwargs)
    assert False
