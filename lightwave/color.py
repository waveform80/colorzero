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


from math import sqrt, atan2, degrees, radians, sin, cos, exp
from fractions import Fraction
from collections import namedtuple

from .types import RGB, HLS, HSV


class Color(RGB):
    """
    The Color class is a tuple which represents a color as linear red, green,
    and blue components.

    The class has a flexible constructor which allows you to create an instance
    from any registered color system (see :func:`color_conversion`). There are
    also explicit constructors for every registered system that can convert
    (directly or indirectly) to linear RGB. For example, an instance of
    :class:`Color` can be constructed in any of the following ways::

        >>> Color('#f00')
        <Color html="#ff0000" rgb=(1.0, 0.0, 0.0)>
        >>> Color('green')
        <Color html="#008000" rgb=(0.0, XXX, 0.0)>
        >>> Color(0, 0, 1)
        <Color html="#0000ff" rgb=(0.0, 0.0, 1.0)>
        >>> Color(h=0, s=1, v=0.5)
        <Color html="#7f0000">
        >>> Color(y=0.4, u=-0.05, v=0.615)
        <Color html="#ff0f4c">

    The specific forms that the default constructor will accept are enumerated
    below:

    +------------------------------+------------------------------------------+
    | Style                        | Description                              |
    +==============================+==========================================+
    | Single positional parameter  | Equivalent to calling                    |
    |                              | :meth:`Color.from_string`.               |
    +------------------------------+------------------------------------------+
    | Three positional parameters  | Equivalent to calling                    |
    |                              | :meth:`Color.from_rgb` if all three      |
    |                              | parameters are between 0.0 and 1.0, or   |
    |                              | :meth:`Color.from_rgb_bytes` otherwise.  |
    +------------------------------+                                          |
    | Three named parameters,      |                                          |
    | "r", "g", "b"                |                                          |
    +------------------------------+                                          |
    | Three named parameters,      |                                          |
    | "red", "green", "blue"       |                                          |
    +------------------------------+------------------------------------------+
    | Three named parameters,      | Equivalent to calling                    |
    | "y", "u", "v"                | :meth:`Color.from_yuv` if "y" is between |
    |                              | 0.0 and 1.0, "u" is between -0.436 and   |
    |                              | 0.436, and "v" is between -0.615 and     |
    |                              | 0.615, or :meth:`Color.from_yuv_bytes`   |
    |                              | otherwise.                               |
    +------------------------------+------------------------------------------+
    | Three named parameters,      | Equivalent to calling                    |
    | "y", "i", "q"                | :meth:`Color.from_yiq`.                  |
    +------------------------------+------------------------------------------+
    | Three named parameters,      | Equivalent to calling                    |
    | "h", "l", "s"                | :meth:`Color.from_hls`.                  |
    +------------------------------+                                          |
    | Three named parameters,      |                                          |
    | "hue", "lightness",          |                                          |
    | "saturation"                 |                                          |
    +------------------------------+------------------------------------------+
    | Three named parameters       | Equivalent to calling                    |
    | "h", "s", "v"                | :meth:`Color.from_hsv`                   |
    +------------------------------+                                          |
    | Three named parameters       |                                          |
    | "hue", "saturation", "value" |                                          |
    +------------------------------+------------------------------------------+
    | Three named parameters,      | Equivalent to calling                    |
    | "x", "y", "z"                | :meth:`Color.from_cie_xyz`               |
    +------------------------------+------------------------------------------+
    | Three named parameters,      | Equivalent to calling                    |
    | "l", "a", "b"                | :meth:`Color.from_cie_lab`               |
    +------------------------------+------------------------------------------+
    | Three named parameters,      | Equivalent to calling                    |
    | "l", "u", "v"                | :meth:`Color.from_cie_luv`               |
    +------------------------------+------------------------------------------+

    If the constructor parameters do not conform to any of the variants in the
    table above, a :exc:`ValueError` will be thrown.

    Internally, the color is *always* represented as 3 float values
    corresponding to the red, green, and blue components of the color. These
    values take a value from 0.0 to 1.0 (least to full intensity). The class
    provides several attributes which can be used to convert one color system
    into another::

        >>> Color('#f00').hls
        (0.0, 0.5, 1.0)
        >>> Color.from_string('green').hue
        Hue(deg=120.0)
        >>> Color.from_rgb_bytes(0, 0, 255).yuv
        (0.114, 0.435912, -0.099978)

    As :class:`Color` derives from tuple, instances are immutable. While this
    provides the advantage that they can be used as keys in a dict, it does
    mean that colors themselves cannot be directly manipulated (e.g. by
    reducing the red component).

    However, several auxilliary classes in the module provide the ability to
    perform simple transformations of colors via operators which produce a new
    :class:`Color` instance. For example::

        >>> Color('red') - Red(0.5)
        <Color "#7f0000">
        >>> Color('green') + Red(0.5)
        <Color "#7f8000">
        >>> Color.from_hls(0.5, 0.5, 1.0)
        <Color "#00feff">
        >>> Color.from_hls(0.5, 0.5, 1.0) * Lightness(0.8)
        <Color "#00cbcc">
        >>> (Color.from_hls(0.5, 0.5, 1.0) * Lightness(0.8)).hls
        (0.5, 0.4, 1.0)

    From the last example above one can see that even attributes not directly
    stored by the color (such as lightness) can be manipulated in this fashion.
    In this case a :class:`Color` instance is constructed from HLS (hue,
    lightness, saturation) values with a lightness of 0.5. This is multiplied
    by a :class:`Lightness` instance with a value of 0.8 which constructs a new
    :class:`Color` with the same hue and saturation, but a lightness of 0.5 *
    0.8 = 0.4.

    If an instance is converted to a string (with :func:`str`) it will return a
    string containing the 7-character HTML code for the color (e.g. "#ff0000"
    for red). As can be seen in the examples above, a similar representation is
    returned for :func:`repr`.

    .. _RGB: https://en.wikipedia.org/wiki/RGB_color_space
    .. _Y'UV: https://en.wikipedia.org/wiki/YUV
    .. _Y'IQ: https://en.wikipedia.org/wiki/YIQ
    .. _HLS: https://en.wikipedia.org/wiki/HSL_and_HSV
    .. _HSV: https://en.wikipedia.org/wiki/HSL_and_HSV
    """

    def __new__(cls, *args, **kwargs):
        def from_rgb(r, g, b):
            if 0.0 <= r <= 1.0 and 0.0 <= g <= 1.0 and 0.0 <= b <= 1.0:
                return cls.from_rgb(r, g, b)
            else:
                return cls.from_rgb_bytes(r, g, b)

        def from_yuv(y, u, v):
            if 0.0 <= y <= 1.0 and -0.436 <= u <= 0.436 and -0.615 <= v <= 0.615:
                return cls.from_yuv(y, u, v)
            else:
                return cls.from_yuv_bytes(y, u, v)

        if kwargs:
            try:
                return {
                    frozenset('rgb'):   from_rgb,
                    frozenset('yuv'):   from_yuv,
                    frozenset('yiq'):   cls.from_yiq,
                    frozenset('hls'):   cls.from_hls,
                    frozenset('hsv'):   cls.from_hsv,
                    frozenset('xyz'):   cls.from_cie_xyz,
                    frozenset('lab'):   cls.from_cie_lab,
                    frozenset('luv'):   cls.from_cie_luv,
                    frozenset(('red', 'green', 'blue')):
                        lambda red, green, blue: from_rgb(red, green, blue),
                    frozenset(('hue', 'lightness', 'saturation')):
                        lambda hue, lightness, saturation: cls.from_hls(hue, lightness, saturation),
                    frozenset(('hue', 'saturation', 'value')):
                        lambda hue, saturation, value: cls.from_hsv(hue, saturation, value),
                    }[frozenset(kwargs.keys())](**kwargs)
            except KeyError:
                pass
        else:
            if len(args) == 1:
                return cls.from_string(args[0])
            elif len(args) == 3:
                return from_rgb(*args)
        raise ValueError('Unable to construct Color from provided arguments')

    @classmethod
    def from_string(cls, s):
        """
        Construct a :class:`Color` from a 4 or 7 character CSS-like
        representation (e.g. "#f00" or "#ff0000" for red), or from one of the
        named colors (e.g. "green" or "wheat") from the `CSS standard`_. Any
        other string format will result in a :exc:`ValueError`.

        .. _CSS standard: http://www.w3.org/TR/css3-color/#svg-color
        """
        if isinstance(s, bytes):
            s = s.decode('ascii')
        if s.startswith('#'):
            if len(s) == 7:
                return cls.from_rgb_bytes(
                    int(s[1:3], base=16),
                    int(s[3:5], base=16),
                    int(s[5:7], base=16)
                    )
            elif len(s) == 4:
                return cls.from_rgb_bytes(
                    int(s[1:2], base=16) * 0x11,
                    int(s[2:3], base=16) * 0x11,
                    int(s[3:4], base=16) * 0x11
                    )
            raise ValueError('Unrecognized color format "%s"' % s)
        try:
            return cls.from_string(NAMED_COLORS[s.lower()])
        except KeyError:
            raise ValueError('Unrecognized color name "%s"' % s)

    def __add__(self, other):
        if isinstance(other, RGB):
            return Color(
                clamp_float(self.r + other.r),
                clamp_float(self.g + other.g),
                clamp_float(self.b + other.b))
        elif isinstance(other, HLS):
            self = self.hls
            return Color.from_hls(
                (self.h + other.h) % 1.0,
                clamp_float(self.l + other.l),
                clamp_float(self.s + other.s))
        elif isinstance(other, HSV):
            self = self.hsv
            return Color.from_hsv(
                (self.h + other.h) % 1.0,
                clamp_float(self.s + other.s),
                clamp_float(self.v + other.v))
        else:
            return NotImplemented

    def __radd__(self, other):
        # Addition is commutative
        if isinstance(other, (RGB, HLS, HSV)):
            return self.__add__(other)
        else:
            return NotImplemented

    def __sub__(self, other):
        if isinstance(other, RGB):
            return Color(
                clamp_float(self.r - other.r),
                clamp_float(self.g - other.g),
                clamp_float(self.b - other.b))
        elif isinstance(other, HLS):
            self = self.hls
            return Color.from_hls(
                (self.h - other.h) % 1.0,
                clamp_float(self.l - other.l),
                clamp_float(self.s - other.s))
        elif isinstance(other, HSV):
            self = self.hsv
            return Color.from_hsv(
                (self.h - other.h) % 1.0,
                clamp_float(self.s - other.s),
                clamp_float(self.v - other.v))
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, RGB):
            return Color(other.r - self.r, other.g - self.g, other.b - self.b)
        elif isinstance(other, HLS):
            self = self.hls
            return Color.from_hls((other.h - self.h) % 1.0, other.l - self.l, other.s - self.s)
        elif isinstance(other, HSV):
            self = self.hsv
            return Color.from_hsv((other.h - self.h) % 1.0, other.s - self.s, other.v - self.v)
        else:
            return NotImplemented

    def __mul__(self, other):
        if isinstance(other, RGB):
            return Color(self.r * other.r, self.g * other.g, self.b * other.b)
        elif isinstance(other, HLS):
            self = self.hls
            return Color.from_hls((self.h * other.h) % 1.0, self.l * other.l, self.s * other.s)
        elif isinstance(other, HSV):
            self = self.hsv
            return Color.from_hsv((self.h * other.h) % 1.0, self.s * other.s, self.v * other.v)
        else:
            return NotImplemented

    def __rmul__(self, other):
        # Multiplication is commutative
        if isinstance(other, (RGB, HLS, HSV)):
            return self.__mul__(other)

    def __str__(self):
        return self.html

    def __repr__(self):
        return '<Color html=%r rgb=(r=%g, g=%g, b=%g)' % (self.html, self.r, self.g, self.b)

    @property
    def rgb(self):
        return RGB(*self)

    def difference(self, other, method='euclid'):
        """
        Determines the difference between this color and *other* using the
        specified *method*. The *method* is specified as a string, and the
        following methods are valid:

        * 'euclid' - This is the default method. Calculate the `Euclidian
          distance`_. This is by far the fastest method, but also the least
          accurate in terms of human perception.
        * 'cie1976' - Use the `CIE 1976`_ formula for calculating the
          difference between two colors in CIE Lab space.
        * 'cie1994g' - Use the `CIE 1994`_ formula with the "graphic arts" bias
          for calculating the difference.
        * 'cie1994t' - Use the `CIE 1994`_ forumula with the "textiles" bias
          for calculating the difference.
        * 'cie2000' - Use the `CIEDE 2000`_ formula for calculating the
          difference.

        Note that the Euclidian distance will be significantly different to the
        other calculations; effectively this just measures the distance between
        the two colors by treating them as coordinates in a three dimensional
        Euclidian space. All other methods are means of calculating a `Delta
        E`_ value in which 2.3 is considered a `just-noticeable difference`_
        (JND).

        .. warning::

            This implementation has yet to receive any significant testing
            (constructor methods for CIELab need to be added before this can be
            done).

        .. _Delta E: https://en.wikipedia.org/wiki/Color_difference
        .. _just-noticeable difference: https://en.wikipedia.org/wiki/Just-noticeable_difference
        .. _Euclidian distance: https://en.wikipedia.org/wiki/Euclidean_distance
        .. _CIE 1976: https://en.wikipedia.org/wiki/Color_difference#CIE76
        .. _CIE 1994: https://en.wikipedia.org/wiki/Color_difference#CIE94
        .. _CIEDE 2000: https://en.wikipedia.org/wiki/Color_difference#CIEDE2000
        """
        if isinstance(method, bytes):
            method = method.decode('ascii')
        if method == 'euclid':
            return sqrt(sum((Cs - Co) ** 2 for Cs, Co in zip(self, other)))
        elif method == 'cie1976':
            return self._cie1976(other)
        elif method.startswith('cie1994'):
            return self._cie1994(other, method)
        elif method == 'ciede2000':
            return self._ciede2000(other)
        else:
            raise ValueError('invalid method: %s' % method)

    def _cie1976(self, other):
        return sqrt(sum((Cs - Co) ** 2 for Cs, Co in zip(self.cie_lab, other.cie_lab)))

    def _cie1994(self, other, method):
        L1, a1, b1 = self.cie_lab
        L2, a2, b2 = other.cie_lab
        dL = L1 - L2
        C1 = sqrt(a1 ** 2 + b1 ** 2)
        C2 = sqrt(a2 ** 2 + b2 ** 2)
        dC = C1 - C2
        # Don't bother with the sqrt here as due to limited float precision
        # we can wind up with a domain error (because the value is ever so
        # slightly negative - try it with black'n'white for an example)
        dH2 = (a1 - a2) ** 2 + (b1 - b2) ** 2 - dC ** 2
        kL, K1, K2 = {
            'cie1994g': (1, 0.045, 0.015),
            'cie1994t': (2, 0.048, 0.014),
            }[method]
        SC = 1 + K1 * C1
        SH = 1 + K2 * C1
        return sqrt((dL ** 2 / kL) + (dC ** 2 / SC) + (dH2 / SH))

    def _ciede2000(self, other):
        L1, a1, b1 = self.cie_lab
        L2, a2, b2 = other.cie_lab
        L_ = (L1 + L2) / 2
        dL = L2 - L1
        C1 = sqrt(a1 ** 2 + b1 ** 2)
        C2 = sqrt(a1 ** 2 + b1 ** 2)
        C_ = (C1 + C2) / 2
        dC = C2 - C1
        G = (1 - sqrt(C_ ** 7 / (C_ ** 7 + 25 ** 7))) / 2
        a1 = (1 + G) * a1
        a2 = (1 + G) * a2
        h1 = 0.0 if b1 == a1 == 0 else degrees(atan2(b1, a1)) % 360
        h2 = 0.0 if b2 == a2 == 0 else degrees(atan2(b2, a2)) % 360
        if C1 * C2 == 0.0:
            dh = 0.0
            h_ = h1 + h2
        elif abs(h1 - h2) <= 180:
            dh = h2 - h1
            h_ = (h1 + h2) / 2
        else:
            if h2 <= h1:
                dh = h2 - h1 + 360
            else:
                dh = h2 - h1 - 360
            if h1 + h2 >= 360:
                h_ = (h1 + h2 + 360) / 2
            else:
                h_ = (h1 + h2 - 360) / 2
        dH = 2 * sqrt(C1 * C2) * sin(radians(dh / 2))
        T = (
                1 -
                0.17 * cos(radians(h_ - 30)) +
                0.24 * cos(radians(2 * h_)) +
                0.32 * cos(radians(3 * h_ + 6)) -
                0.20 * cos(radians(4 * h_ - 63))
                )
        SL = 1 + (0.015 * (L_ - 50) ** 2) / sqrt(20 + (L_ - 50) ** 2)
        SC = 1 + 0.045 * C_
        SH = 1 + 0.015 * C_ * T
        RT = -2 * sqrt(C_ ** 7 / (C_ ** 7 + 25 ** 7)) * sin(radians(60 * exp(-(((h_ - 275) / 25) ** 2))))
        return sqrt((dL / SL) ** 2 + (dC / SC) ** 2 + (dH / SH) ** 2 + RT * (dC / SC) * (dH / SH))


