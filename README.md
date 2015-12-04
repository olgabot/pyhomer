# Python HOMER tools

[![Build Status](https://travis-ci.org/olgabot/pyhomer.svg?branch=master)](https://travis-ci.org/olgabot/pyhomer)[![](https://img.shields.io/pypi/v/pyhomer.svg)](https://pypi.python.org/pypi/pyhomer)

## What is `Python HOMER tools`?

pyhomer contains utility scripts and functions to work with output from the HOMER motif finding program

* Free software: BSD license

## Installation

To install this code, clone this github repository and use `pip` to install

    git clone git@github.com:olgabot/pyhomer
    cd pyhomer
    pip install .  # The "." means "install *this*, the folder where I am now"


## Features

First, you'll want to create a `ForegroundBackgroundPair`


```python
import pyhomer

pair = pyhomer.ForegroundBackgroundPair('foreground.bed', 'background.bed')
```

### Create a `homer` command

```python
n_processors = 4
flags = '-rna -len 4,5,6 -mset vertebrates -mis 0 -p {} -noweight'.format(n_processors)
command = pair.homer(flags=flags, genome='hg19', out_dir='homer/', force=False)
```

And the value of `command` is:

```
findMotifsGenome.pl ... FILLMEIN
```

If the `out_dir` already exists, then `pair.homer()` will raise a `ValueError`.
To force creation of the command anyway, set `force=True`.

### Intersect with other bed files, and keep foreground/background

```python
conserved_pair = pair.intersect('primate_conserved.bed', 'primate')
```

### Get flanking introns, keeping foreground/background

```python
intron_pair = pair.flanking_intron('downstream', genome='hg19', nt=400)
```
