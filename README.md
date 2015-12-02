# Python HOMER tools

[![](https://img.shields.io/travis/olgabot/pyhomer.svg)](https://travis-ci.org/olgabot/pyhomer)[![](https://img.shields.io/pypi/v/pyhomer.svg)](https://pypi.python.org/pypi/pyhomer)

## What is `Python HOMER tools`?

pyhomer contains utility scripts and functions to work with output from the HOMER motif finding program

* Free software: BSD license
* Documentation: https://olgabot.github.io/pyhomer

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
homer_flags = '-rna -len 4,5,6 -mset vertebrates -mis 0 -p {} -noweight'.format(n_processors)
command = pyhomer.construct_homer_command(pair.foreground.fn, pair.background.fn, 
    homer_flags)
```

And the value of `command` is:

```
findMotifsGenome.pl ... FILLMEIN
```

### Intersect with other bed files, and keep foreground/background

```python
conserved_pair = pair.intersect('primate_conserved.bed', 'primate')
```

### Get flanking introns, keeping foreground/background

```python
intron_pair = pair.flanking_intron('downstream', genome='hg19', nt=400)
```