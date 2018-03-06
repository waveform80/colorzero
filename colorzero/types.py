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

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
    )

from collections import namedtuple


YUV = namedtuple('YUV', ('y', 'u', 'v'))
YIQ = namedtuple('YIQ', ('y', 'i', 'q'))
XYZ = namedtuple('XYZ', ('X', 'Y', 'Z'))
Luv = namedtuple('Luv', ('L', 'u', 'v'))
Lab = namedtuple('Lab', ('L', 'a', 'b'))


class RGB(namedtuple('RGB', ('r', 'g', 'b'))):
    @property
    def red(self):
        return self.r

    @property
    def green(self):
        return self.g

    @property
    def blue(self):
        return self.b


class HLS(namedtuple('HLS', ('h', 'l', 's'))):
    @property
    def hue(self):
        return self.h

    @property
    def lightness(self):
        return self.l

    @property
    def saturation(self):
        return self.s


class HSV(namedtuple('HSV', ('h', 's', 'v'))):
    @property
    def hue(self):
        return self.h

    @property
    def saturation(self):
        return self.s

    @property
    def value(self):
        return self.v


class CMY(namedtuple('CMY', ('c', 'm', 'y'))):
    @property
    def cyan(self):
        return self.c

    @property
    def magenta(self):
        return self.m

    @property
    def yellow(self):
        return self.y


class CMYK(namedtuple('CMYK', ('c', 'm', 'y', 'k'))):
    @property
    def cyan(self):
        return self.c

    @property
    def magenta(self):
        return self.m

    @property
    def yellow(self):
        return self.y

    @property
    def black(self):
        return self.k

