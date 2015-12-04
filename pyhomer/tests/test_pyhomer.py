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


@pytest.fixture(params=["doesn't exist",
                        pytest.mark.xfail("already exists")])
def out_dir(request):
    if request.param == "doesn't exist":
        return 'homer/'
    elif request.param == "already exists":
        return './'


@pytest.fixture()
def flags(request):
    return '-rna -len 4,5,6 -mset vertebrates -mis 0 -p 4 -noweight'


@pytest.fixture()
def findMotifsGenome():
    return '~/bin/findMotifsGenome.pl'


@pytest.fixture(params=[True, pytest.mark.xfail(False)])
def force(request):
    return request.param


@pytest.fixture()
def genome():
    return 'mm10'


def test_construct_homer_command_vanilla(foreground_filename,
                                         background_filename):
    import pyhomer

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename)

    true = 'findMotifsGenome.pl /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground.bed hg19 /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground -bg /Users/olga/workspace-git/pyhomer/pyhomer/tests/background.bed'  # noqa
    assert test == true


def test_construct_homer_command_flags(foreground_filename,
                                       background_filename, flags):
    import pyhomer

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename, flags=flags)

    true = 'findMotifsGenome.pl /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground.bed hg19 /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground -bg /Users/olga/workspace-git/pyhomer/pyhomer/tests/background.bed -rna -len 4,5,6 -mset vertebrates -mis 0 -p 4 -noweight'# noqa
    assert test == true


def test_construct_homer_command_findMotifsGenome(
        foreground_filename, background_filename, findMotifsGenome):
    import pyhomer

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename,
        findMotifsGenome=findMotifsGenome)

    true = '~/bin/findMotifsGenome.pl /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground.bed hg19 /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground -bg /Users/olga/workspace-git/pyhomer/pyhomer/tests/background.bed'  # noqa
    assert test == true


def test_construct_homer_command_out_dir(
        foreground_filename, background_filename, out_dir):
    """If out_dir already exists, then this xfails"""
    import pyhomer

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename,
        out_dir=out_dir)

    true = 'findMotifsGenome.pl /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground.bed hg19 homer/ -bg /Users/olga/workspace-git/pyhomer/pyhomer/tests/background.bed'  # noqa
    assert test == true


def test_construct_homer_command_force(
        foreground_filename, background_filename, force):
    """Test that force=False when the directory exists raises an error
    but no error when force=True"""
    import pyhomer

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename,
        out_dir='./', force=force)

    true = 'findMotifsGenome.pl /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground.bed hg19 ./ -bg /Users/olga/workspace-git/pyhomer/pyhomer/tests/background.bed'  # noqa
    assert test == true

def test_construct_homer_command_genome(foreground_filename,
                                        background_filename, genome):
    import pyhomer

    test = pyhomer.construct_homer_command(
        foreground_filename, background_filename, genome=genome)

    true = 'findMotifsGenome.pl /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground.bed mm10 /Users/olga/workspace-git/pyhomer/pyhomer/tests/foreground -bg /Users/olga/workspace-git/pyhomer/pyhomer/tests/background.bed'  # noqa
    assert test == true
