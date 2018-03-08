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

"Define the tuples used to represent various color systems."

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
)

from collections import namedtuple


YUV = namedtuple('YUV', ('y', 'u', 'v'))
YIQ = namedtuple('YIQ', ('y', 'i', 'q'))
XYZ = namedtuple('XYZ', ('x', 'y', 'z'))
Luv = namedtuple('Luv', ('l', 'u', 'v'))
Lab = namedtuple('Lab', ('l', 'a', 'b'))


class RGB(namedtuple('RGB', ('r', 'g', 'b'))):
    "Named tuple representing red, green, and blue."

    @property
    def red(self):
        # pylint: disable=missing-docstring
        return self.r

    @property
    def green(self):
        # pylint: disable=missing-docstring
        return self.g

    @property
    def blue(self):
        # pylint: disable=missing-docstring
        return self.b


class HLS(namedtuple('HLS', ('h', 'l', 's'))):
    "Named tuple representing hue, lightness, and saturation."

    @property
    def hue(self):
        # pylint: disable=missing-docstring
        return self.h

    @property
    def lightness(self):
        # pylint: disable=missing-docstring
        return self.l

    @property
    def saturation(self):
        # pylint: disable=missing-docstring
        return self.s


class HSV(namedtuple('HSV', ('h', 's', 'v'))):
    'Named tuple representing hue, saturation, and value ("brightness").'

    @property
    def hue(self):
        # pylint: disable=missing-docstring
        return self.h

    @property
    def saturation(self):
        # pylint: disable=missing-docstring
        return self.s

    @property
    def value(self):
        # pylint: disable=missing-docstring
        return self.v


class CMY(namedtuple('CMY', ('c', 'm', 'y'))):
    "Named tuple representing cyan, magenta, and yellow."

    @property
    def cyan(self):
        # pylint: disable=missing-docstring
        return self.c

    @property
    def magenta(self):
        # pylint: disable=missing-docstring
        return self.m

    @property
    def yellow(self):
        # pylint: disable=missing-docstring
        return self.y


class CMYK(namedtuple('CMYK', ('c', 'm', 'y', 'k'))):
    "Named tuple representing cyan, magenta, yellow, and black."

    @property
    def cyan(self):
        # pylint: disable=missing-docstring
        return self.c

    @property
    def magenta(self):
        # pylint: disable=missing-docstring
        return self.m

    @property
    def yellow(self):
        # pylint: disable=missing-docstring
        return self.y

    @property
    def black(self):
        # pylint: disable=missing-docstring
        return self.k
