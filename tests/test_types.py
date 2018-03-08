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

"Tests for the colorzero.types module."

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
)

# pylint: disable=import-error,missing-docstring
from colorzero import RGB, HLS, HSV, CMY, CMYK


def test_rgb():
    v = RGB(1, 0.5, 0)
    assert v.red == 1
    assert v.green == 0.5
    assert v.blue == 0


def test_hls():
    v = HLS(0, 0.5, 1)
    assert v.hue == 0
    assert v.lightness == 0.5
    assert v.saturation == 1


def test_hsv():
    v = HSV(0, 0.5, 1)
    assert v.hue == 0
    assert v.saturation == 0.5
    assert v.value == 1


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
