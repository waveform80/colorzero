# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
#
# Copyright (c) 2018 Dave Jones <dave@waveform.org.uk>
#
# SPDX-License-Identifier: BSD-3-Clause

"Tests for the colorzero.types module."

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
)

# pylint: disable=import-error,missing-docstring
import pytest
from colorzero import RGB, YUV, HLS, HSV, CMY, CMYK


def test_rgb():
    assert RGB(1, 1, 1)._replace(r=0) == RGB(0, 1, 1)
    with pytest.raises(TypeError):
        RGB(1, 1)
    with pytest.raises(ValueError):
        RGB(1, 1, 1)._replace(foo=1)
    v = RGB(1, 0.5, 0)
    assert v.r == v.red == 1
    assert v.g == v.green == 0.5
    assert v.b == v.blue == 0
    assert v.__getnewargs__() == (1, 0.5, 0)
    assert repr(v) == 'RGB(r=1, g=0.5, b=0)'


def test_hls():
    assert HLS(1, 1, 1)._replace(h=0) == HLS(0, 1, 1)
    with pytest.raises(TypeError):
        HLS(1, 1)
    with pytest.raises(ValueError):
        HLS(1, 1, 1)._replace(foo=1)
    v = HLS(0, 0.5, 1)
    assert v.h == v.hue == 0
    assert v.l == v.lightness == 0.5
    assert v.s == v.saturation == 1
    assert v.__getnewargs__() == (0, 0.5, 1)
    assert v._asdict() == {'h': 0, 'l': 0.5, 's': 1}
    assert repr(v) == 'HLS(h=0, l=0.5, s=1)'


def test_hsv():
    assert HSV(1, 1, 1)._replace(h=0) == HSV(0, 1, 1)
    with pytest.raises(TypeError):
        HSV(1, 1)
    with pytest.raises(ValueError):
        HSV(1, 1, 1)._replace(foo=1)
    v = HSV(0, 0.5, 1)
    assert v.h == v.hue == 0
    assert v.s == v.saturation == 0.5
    assert v.v == v.value == 1
    assert v.__getnewargs__() == (0, 0.5, 1)
    assert v._asdict() == {'h': 0, 's': 0.5, 'v': 1}
    assert repr(v) == 'HSV(h=0, s=0.5, v=1)'


def test_yuv():
    assert YUV(1, 1, 1)._replace(y=0) == YUV(0, 1, 1)
    with pytest.raises(TypeError):
        YUV(1, 1)
    with pytest.raises(ValueError):
        YUV(1, 1, 1)._replace(foo=1)
    v = YUV(0, 0.5, 1)
    assert v.y == v.luma == 0
    assert v.u == 0.5
    assert v.v == 1
    assert v.__getnewargs__() == (0, 0.5, 1)
    assert v._asdict() == {'y': 0, 'u': 0.5, 'v': 1}
    assert repr(v) == 'YUV(y=0, u=0.5, v=1)'


def test_cmy():
    v = CMY(0, 0.5, 1)
    assert v.cyan == 0
    assert v.magenta == 0.5
    assert v.yellow == 1


def test_cmyk():
    v = CMYK(0, 0.5, 1, 0.2)
    assert v.cyan == 0
    assert v.magenta == 0.5
    assert v.yellow == 1
    assert v.black == 0.2
