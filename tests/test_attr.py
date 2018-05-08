# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
# Copyright (c) 2016-2018 Dave Jones <dave@waveform.org.uk>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"Tests for the colorzero.attr module"

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
)

from math import pi

# pylint: disable=import-error,missing-docstring
import pytest
from colorzero import *


def test_hue_init():
    assert Hue(0.0) == 0.0
    assert Hue(1.0) == 0.0
    assert Hue(deg=0) == 0.0
    assert Hue(deg=360) == 0.0
    assert Hue(deg=720) == 0.0
    assert Hue(deg=-180) == 0.5
    assert Hue(deg=180) == 0.5
    assert Hue(rad=0) == 0.0
    assert Hue(rad=pi) == 0.5
    assert Hue(rad=2 * pi) == 0.0
    with pytest.raises(ValueError):
        Hue()


def test_red_repr():
    assert repr(Red(0.5)) == 'Red(0.5)'


def test_green_repr():
    assert repr(Green(1.0)) == 'Green(1)'


def test_blue_repr():
    assert repr(Blue(0.75)) == 'Blue(0.75)'


def test_hue_attr():
    assert Hue(0).deg == 0
    assert Hue(0.5).deg == 180
    assert Hue(1 / 3).deg == 120
    assert Hue(0).rad == 0
    assert Hue(0.5).rad == pi
    assert Hue(1 / 3).rad == (2 / 3) * pi


def test_hue_repr():
    assert repr(Hue(0)) == 'Hue(deg=0)'
    assert repr(Hue(0.5)) == 'Hue(deg=180)'
    assert repr(Hue(1/3)) == 'Hue(deg=120)'


def test_sat_repr():
    assert repr(Saturation(1.0)) == 'Saturation(1)'


def test_light_repr():
    assert repr(Lightness(0.25)) == 'Lightness(0.25)'


def test_luma_repr():
    assert repr(Luma(0.0)) == 'Luma(0)'
