# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
#
# Copyright (c) 2018 Dave Jones <dave@waveform.org.uk>
#
# SPDX-License-Identifier: BSD-3-Clause

"Tests for the colorzero.easings module"

import pytest
from colorzero.easings import *


def test_linear():
    assert list(linear(2)) == [0, 1]
    assert list(linear(5)) == [0, 1/4, 1/2, 3/4, 1]


def test_ease_in():
    assert list(ease_in(2)) == [0, 1]
    assert list(ease_in(5)) == [0, 1/16, 4/16, 9/16, 1]


def test_ease_out():
    assert list(ease_out(2)) == [0, 1]
    assert list(ease_out(5)) == [0, 7/16, 12/16, 15/16, 1]


def test_ease_in_out():
    assert list(ease_in_out(2)) == [0, 1]
    assert list(ease_in_out(5)) == [0, 2/16, 8/16, 14/16, 1]
