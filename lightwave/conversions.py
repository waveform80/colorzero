# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The lightwave color library
# Copyright (c) 2016 Dave Jones <dave@waveform.org.uk>
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
# Make Py2's zip equivalent to Py3's
try:
    from itertools import izip as zip
except ImportError:
    pass

# Make Py2's str and range equivalent to Py3's
str = type('')

import colorsys
from fractions import Fraction

from .names import NAMED_COLORS
from .types import RGB, YIQ, YUV, CMY, CMYK, HLS, HSV, XYZ, Luv, Lab
from .decorator import color_conversion


# Don't export anything
__all__ = []


# Utility functions
clamp_float = lambda v: max(0.0, min(1.0, v))
clamp_bytes = lambda v: max(0, min(255, v))

to_srgb = lambda c: 12.92 * c if c <= 0.0031308 else (1.055 * c ** (1/2.4) - 0.055)
from_srgb = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

D65 = XYZ(0.95047, 1.0, 1.08883)

U = lambda x, y, z: 4 * x / (x + 15 * y + 3 * z)
V = lambda x, y, z: 9 * y / (x + 15 * y + 3 * z)

indent = lambda text, prefix: ''.join(
    prefix + line if line.strip() else line
    for line in text.splitlines(True)
    )

matrix_mult = lambda m, n: (
        sum(mval * nval for mval, nval in zip(mrow, n))
        for mrow in m
        )


# Sources used in the production of the following conversions include:
#
# https://en.wikipedia.org/wiki/RGB_color_space
# https://en.wikipedia.org/wiki/SRGB
# https://en.wikipedia.org/wiki/YUV
# https://en.wikipedia.org/wiki/YIQ
# https://en.wikipedia.org/wiki/HSL_and_HSV
# https://en.wikipedia.org/wiki/CIE_1931_color_space
# http://www.poynton.com/notes/colour_and_gamma/ColorFAQ.html


@color_conversion(returns=YIQ)
def _rgb_to_yiq(r, g, b):
    return YIQ(*colorsys.rgb_to_yiq(r, g, b))

@color_conversion(returns=RGB)
def _yiq_to_rgb(y, i, q):
    return RGB(*colorsys.yiq_to_rgb(y, i, q))

@color_conversion(returns=HLS)
def _rgb_to_hls(r, g, b):
    return HLS(*colorsys.rgb_to_hls(r, g, b))

@color_conversion(returns=RGB)
def _hls_to_rgb(h, l, s):
    return RGB(*colorsys.hls_to_rgb(h, l, s))

@color_conversion(returns=HSV)
def _rgb_to_hsv(r, g, b):
    return HSV(*colorsys.rgb_to_hsv(r, g, b))

@color_conversion(returns=RGB)
def _hsv_to_rgb(h, s, v):
    return RGB(*colorsys.hsv_to_rgb(h, s, v))

@color_conversion(returns=RGB)
def _rgb_to_rgb_bytes(r, g, b):
    return RGB(int(r * 255), int(g * 255), int(b * 255))

@color_conversion(returns=RGB)
def _rgb_bytes_to_rgb(r, g, b):
    return RGB(r / 255, g / 255, b / 255)

@color_conversion(returns=str)
def _rgb_bytes_to_html(r, g, b):
    return '#%02x%02x%02x' % (r, g, b)

@color_conversion(returns=int)
def _rgb_bytes_to_rgb24(r, g, b):
    return (b << 16) | (g << 8) | r

@color_conversion(returns=RGB)
def _rgb24_to_rgb_bytes(n):
    return RGB(n & 0xFF, (n >> 8) & 0xFF, (n >> 16) & 0xFF)

@color_conversion(returns=RGB)
def _html_to_rgb_bytes(html):
    if html.startswith('#'):
        try:
            if len(html) == 7:
                return RGB(
                    int(html[1:3], base=16),
                    int(html[3:5], base=16),
                    int(html[5:7], base=16)
                    )
            elif len(html) == 4:
                return RGB(
                    int(html[1:2], base=16) * 0x11,
                    int(html[2:3], base=16) * 0x11,
                    int(html[3:4], base=16) * 0x11
                    )
        except ValueError:
            pass
    raise ValueError('%s is not a valid HTML color specification' % html)

@color_conversion(returns=str)
def _name_to_html(name):
    try:
        return NAMED_COLORS[name]
    except KeyError:
        raise ValueError('invalid color name %s' % name)

@color_conversion(returns=int)
def _rgb_to_rgb565(r, g, b):
    return (
        (int(r * 0xF800) & 0xF800) |
        (int(g * 0x07E0) & 0x07E0) |
        (int(b * 0x001F) & 0x001F)
        )

@color_conversion(returns=RGB)
def _rgb565_to_rgb(rgb565):
    r = (rgb565 & 0xF800) / 0xF800
    g = (rgb565 & 0x07E0) / 0x07E0
    b = (rgb565 & 0x001F) / 0x001F
    return RGB(r, g, b)

@color_conversion(returns=YUV)
def _rgb_to_yuv(r, g, b):
    y = 0.299 * r + 0.587 * g + 0.114 * b
    return YUV(y, 0.492 * (b - y), 0.877 * (r - y))

@color_conversion(returns=RGB)
def _yuv_to_rgb(y, u, v):
    return RGB(
        clamp_float(y + 1.14  * v),
        clamp_float(y - 0.395 * u - 0.581 * v),
        clamp_float(y + 2.033 * u),
        )

@color_conversion(returns=RGB)
def _yuv_bytes_to_rgb_bytes(y, u, v):
    c = y - 16
    d = u - 128
    e = v - 128
    return RGB(
        clamp_bytes((298 * c + 409 * e + 128) >> 8),
        clamp_bytes((298 * c - 100 * d - 208 * e + 128) >> 8),
        clamp_bytes((298 * c + 516 * d + 128) >> 8),
        )

@color_conversion(returns=YUV)
def _rgb_bytes_to_yuv_bytes(r, g, b):
    return YUV(
        (( 66 * r + 129 * g +  25 * b + 128) >> 8) + 16,
        ((-38 * r -  73 * g + 112 * b + 128) >> 8) + 128,
        ((112 * r -  94 * g -  18 * b + 128) >> 8) + 128,
        )

@color_conversion(returns=CMY)
def _rgb_to_cmy(r, g, b):
    return CMY(1 - r, 1 - g, 1 - b)

@color_conversion(returns=RGB)
def _cmy_to_rgb(c, m, y):
    return RGB(1 - c, 1 - m, 1 - y)

@color_conversion(returns=CMYK)
def _cmy_to_cmyk(c, m, y):
    k = min(c, m, y)
    if k == 1.0:
        return CMYK(0.0, 0.0, 0.0, 1.0)
    else:
        d = 1.0 - k
        return CMYK((c - k) / d, (m - k) / d, (y - k) / d, k)

@color_conversion(returns=CMY)
def _cmyk_to_cmy(c, m, y, k):
    n = 1 - k
    return CMY(c * n + k, m * n + k, y * n + k)

@color_conversion(returns=XYZ)
def _rgb_to_xyz(r, g, b):
    return XYZ(*matrix_mult(
        ((0.4124564, 0.3575761, 0.1804375),
         (0.2126729, 0.7151522, 0.0721750),
         (0.0193339, 0.1191920, 0.9503041)),
        (from_srgb(r), from_srgb(g), from_srgb(b))
        ))

@color_conversion(returns=RGB)
def _xyz_to_rgb(x, y, z):
    m = matrix_mult(
        (( 3.2404542, -1.5371385, -0.4985314),
         (-0.9692660,  1.8760108,  0.0415560),
         ( 0.0556434, -0.2040259,  1.0572252)),
        (x, y, z)
        )
    return RGB(*(to_srgb(c) for c in m))

@color_conversion(returns=XYZ)
def _luv_to_xyz(l, u, v):
    uw = U(*D65)
    vw = V(*D65)
    u_p = u / (13 * l) + uw
    v_p = v / (13 * l) + vw
    y = D65.Y * (l * Fraction(3, 29) ** 3 if l <= 8 else ((l + 16) / 116) ** 3)
    return XYZ(
        y * (9 * u_p) / (4 * v_p),
        y,
        y * (12 - 3 * u_p - 20 * v_p) / (4 * v_p),
        )

@color_conversion(returns=Luv)
def _xyz_to_luv(x, y, z):
    K = Fraction(29, 3) ** 3
    e = Fraction(6, 29) ** 3
    yr = y / D65.Y
    L = 116 * yr ** Fraction(1, 3) - 16 if yr > e else K * yr
    return Luv(
        L,
        13 * L * (U(x, y, z) - U(*D65)),
        13 * L * (V(x, y, z) - V(*D65)),
        )

@color_conversion(returns=XYZ)
def _lab_to_xyz(l, a, b):
    theta = Fraction(6, 29)
    fy = (l + 16) / 116
    fx = fy + a / 500
    fz = fy - b / 200
    xyz = (
        n ** 3 if n > theta else 3 * theta ** 2 * (n - Fraction(4, 29))
        for n in (fx, fy, fz)
        )
    return XYZ(*(n * m for n, m in zip(xyz, D65)))

@color_conversion(returns=Lab)
def _xyz_to_lab(x, y, z):
    K = Fraction(1, 3) * Fraction(29, 6) ** 2
    e = Fraction(6, 29) ** 3
    x, y, z = (n / m for n, m in zip((x, y, z), D65))
    fx, fy, fz = (
        n ** Fraction(1, 3) if n > e else K * n + Fraction(4, 29)
        for n in (x, y, z)
        )
    return Lab(116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))

