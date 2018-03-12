===============
Getting started
===============

.. currentmodule:: colorzero

The :class:`Color` class is the main interface provided by colorzero. It can be
constructed in a large variety of ways including with red, green, and blue
components, "well known" color names (taken from CSS 3's `extended color
keywords`_), HTML color specifications, and more. A selection of valid
constructors is shown below::

    >>> from colorzero import *
    >>> Color('red')
    <Color html="#ff0000" rgb=(1.0, 0.0, 0.0)>
    >>> Color(1.0, 0.0, 0.0)
    <Color html="#ff0000" rgb=(1.0, 0.0, 0.0)>
    >>> Color(255, 0, 0)
    <Color html="#ff0000" rgb=(1.0, 0.0, 0.0)>
    >>> Color('#ff0000')
    <Color html="#ff0000" rgb=(1.0, 0.0, 0.0)>
    >>> Color('#f00')
    <Color html="#ff0000" rgb=(1.0, 0.0, 0.0)>

Internally, colorzero always represents colors as red, green, and blue values
between 0.0 and 1.0. :class:`Color` objects are tuple descendents. Crucially,
this means they are *immutable*. Attempting to change the red, green, or blue
attributes will fail::

    >>> c = Color('red')
    >>> c.red
    Red(1.0)
    >>> c.red = 0.5
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    AttributeError: can't set attribute

In order to manipulate a color, colorzero provides a simple series of classes
which represent attributes of a color: :class:`Red`, :class:`Green`,
:class:`Blue`, :class:`Hue`, :class:`Lightness`, :class:`Saturation` and so on.
You can use these classes in combination with Python's usual mathematical
operators (addition, subtraction, multiplication, etc.) to manipulate a color.
For example, continuing the example from above::

    >>> c + Green(0.1)
    <Color html='#ff1a00' rgb=(1, 0.1, 0)>
    >>> c = c + Green(0.5)
    >>> c
    <Color html='#ff8000' rgb=(1, 0.5, 0)>
    >>> c.lightness
    Lightness(0.5)
    >>> c = c * Lightness(0.5)
    >>> c
    <Color html='#804000' rgb=(0.5, 0.25, 0)>

Numerous attributes are provided to enable conversion of the RGB representation
to other systems::

    >>> c.rgb
    RGB(r=0.5, g=0.25, b=0.0)
    >>> c.rgb_bytes
    RGB(r=128, g=64, b=0)
    >>> c.rgb565
    31200
    >>> c.hls
    HLS(h=0.08333333333333333, l=0.25, s=1.0)
    >>> c.xyz
    XYZ(x=0.10647471144683732, y=0.0819048964489466, z=0.010202272707313633)
    >>> c.lab
    Lab(l=34.376494620040376, a=23.890819210881016, b=44.69197916172735)

Equivalent constructors exist for all these systems::

    >>> Color.from_rgb(0.5, 0.25, 0.0)
    <Color html='#804000' rgb=(0.5, 0.25, 0)>
    >>> Color.from_rgb_bytes(128, 64, 0)
    <Color html='#804000' rgb=(0.501961, 0.25098, 0)>
    >>> Color.from_rgb565(31200)
    <Color html='#7b3d00' rgb=(0.483871, 0.238095, 0)>
    >>> Color.from_hls(*c.hls)
    <Color html='#804000' rgb=(0.5, 0.25, 0)>
    >>> Color.from_xyz(*c.xyz)
    <Color html='#7f4000' rgb=(0.5, 0.25, 0)>
    >>> Color.from_lab(*c.lab)
    <Color html='#7f4000' rgb=(0.5, 0.25, 0)>

Note that some conversions lose a certain amount of precision.

Methods are also provided to compare colors for similarity. The simplest
algorithm (and the default) is "euclid" which calculates the difference as the
distance between them by treating the r, g, b components as coordinates in a
3-dimensional space. The same color will have a distance of 0.0, whilst the
largest possible difference is √3 (~1.732)::

    >>> c1 = Color('red')
    >>> c2 = Color('green')
    >>> c3 = c1 * Lightness(0.9)
    >>> c1.difference(c2, 'euclid')
    1.1189122525867927
    >>> c1.difference(c2)
    1.1189122525867927
    >>> c1.difference(c3)
    0.09999999999999998

Various `Delta-E`_ algorithms (CIE1976, CIE1994, and CIEDE2000) are also
provided. In these systems, 2.3 is considered a "just noticeable difference"::

    >>> c1.difference(c2, 'cie1976')
    133.10729836196307
    >>> c1.difference(c3, 'cie1976')
    9.60280542204272
    >>> c1.difference(c2, 'cie1994g')
    50.97596644678241
    >>> c1.difference(c3, 'cie1994g')
    5.484832836355026
    >>> c1.difference(c2, 'ciede2000')
    72.18229138962074
    >>> c1.difference(c3, 'ciede2000')
    5.490813507834904

.. _extended color keywords: https://www.w3.org/TR/css3-color/#svg-color
.. _Delta-E: https://en.wikipedia.org/wiki/Color_difference
