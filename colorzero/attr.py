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

"""
Defines the classes for manipulating the attributes of the :class:`Color`
class through the standard binary operators.
"""

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
)

from math import pi


class Red(float):
    """
    Represents the red component of a :class:`Color` for use in
    transformations. Instances of this class can be constructed directly with a
    float value, or by querying the :attr:`Color.red` attribute. Addition,
    subtraction, and multiplication are supported with :class:`Color`
    instances. For example::

        >>> Color.from_rgb(0, 0, 0) + Red(0.5)
        <Color "#7f0000">
        >>> Color('#f00') - Color('#900').red
        <Color "#660000">
        >>> (Red(0.1) * Color('red')).red
        Red(0.1)
    """

    def __repr__(self):
        return "Red(%s)" % self


class Green(float):
    """
    Represents the green component of a :class:`Color` for use in
    transformations.  Instances of this class can be constructed directly with
    a float value, or by querying the :attr:`Color.green` attribute. Addition,
    subtraction, and multiplication are supported with :class:`Color`
    instances. For example::

        >>> Color(0, 0, 0) + Green(0.1)
        <Color "#001900">
        >>> Color.from_yuv(1, -0.4, -0.6) - Green(1)
        <Color "#50002f">
        >>> (Green(0.5) * Color('white')).rgb
        (Red(1.0), Green(0.5), Blue(1.0))
    """

    def __repr__(self):
        return "Green(%s)" % self


class Blue(float):
    """
    Represents the blue component of a :class:`Color` for use in
    transformations.  Instances of this class can be constructed directly with
    a float value, or by querying the :attr:`Color.blue` attribute. Addition,
    subtraction, and multiplication are supported with :class:`Color`
    instances. For example::

        >>> Color(0, 0, 0) + Blue(0.2)
        <Color "#000033">
        >>> Color.from_hls(0.5, 0.5, 1.0) - Blue(1)
        <Color "#00fe00">
        >>> Blue(0.9) * Color('white')
        <Color "#ffffe5">
    """

    def __repr__(self):
        return "Blue(%s)" % self


class Hue(float):
    """
    Represents the hue of a :class:`Color` for use in transformations.
    Instances of this class can be constructed directly with a float value in
    the range [0.0, 1.0) representing an angle around the `HSL hue wheel`_. As
    this is a circular mapping, 0.0 and 1.0 effectively mean the same thing,
    i.e.  out of range values will be normalized into the range [0.0, 1.0).

    The class can also be constructed with the keyword arguments ``deg`` or
    ``rad`` if you wish to specify the hue value in degrees or radians instead,
    respectively. Instances can also be constructed by querying the
    :attr:`Color.hue` attribute.

    Addition, subtraction, and multiplication are supported with :class:`Color`
    instances. For example::

        >>> Color(1, 0, 0).hls
        (0.0, 0.5, 1.0)
        >>> (Color(1, 0, 0) + Hue(deg=180)).hls
        (0.5, 0.5, 1.0)

    Note that whilst multiplication by a :class:`Hue` doesn't make much sense,
    it is still supported. However, the circular nature of a hue value can lead
    to suprising effects. In particular, since 1.0 is equivalent to 0.0 the
    following may be observed::

        >>> (Hue(1.0) * Color.from_hls(0.5, 0.5, 1.0)).hls
        (0.0, 0.5, 1.0)

    .. _HSL hue wheel: https://en.wikipedia.org/wiki/Hue
    """

    def __new__(cls, n=None, deg=None, rad=None):
        if n is not None:
            return super(Hue, cls).__new__(cls, n % 1.0)
        elif deg is not None:
            return super(Hue, cls).__new__(cls, (deg / 360.0) % 1.0)
        elif rad is not None:
            return super(Hue, cls).__new__(cls, (rad / (2 * pi)) % 1.0)
        else:
            raise ValueError('You must specify a value, or deg or rad')

    def __repr__(self):
        return "Hue(deg=%s)" % self.deg

    @property
    def deg(self):
        """
        Returns the hue as a value in degrees with the range 0.0 <= n < 360.0.
        """
        return self * 360.0

    @property
    def rad(self):
        """
        Returns the hue as a value in radians with the range 0.0 <= n < 2π.
        """
        return self * 2 * pi


class Lightness(float):
    """
    Represents the lightness of a :class:`Color` for use in transformations.
    Instances of this class can be constructed directly with a float value, or
    by querying the :attr:`Color.lightness` attribute. Addition, subtraction,
    and multiplication are supported with :class:`Color` instances. For
    example::

        >>> Color(0, 0, 0) + Lightness(0.1)
        <Color "#191919">
        >>> Color.from_rgb_bytes(0x80, 0x80, 0) - Lightness(0.2)
        <Color "#191900">
        >>> Lightness(0.9) * Color('wheat')
        <Color "#f0cd8d">
    """

    def __repr__(self):
        return "Lightness(%s)" % self


class Saturation(float):
    """
    Represents the saturation of a :class:`Color` for use in transformations.
    Instances of this class can be constructed directly with a float value, or
    by querying the :attr:`Color.saturation` attribute. Addition, subtraction,
    and multiplication are supported with :class:`Color` instances. For
    example::

        >>> Color(0.9, 0.9, 0.6) + Saturation(0.1)
        <Color "#ebeb92">
        >>> Color('red') - Saturation(1)
        <Color "#7f7f7f">
        >>> Saturation(0.5) * Color('wheat')
        <Color "#e4d9c3">
    """

    def __repr__(self):
        return "Saturation(%s)" % self


class Luma(float):
    """
    Represents the luma of a :class:`Color` for use in transformations.
    Instances of this class can be constructed directly with a float value, or
    by querying the :attr:`Color.yuv.y` attribute. Addition, subtraction, and
    multiplication are supported with :class:`Color` instances. For example::

        >>> Color(0, 0, 0) + Luma(0.1)
    """

    def __repr__(self):
        return "Luma(%s)" % self
