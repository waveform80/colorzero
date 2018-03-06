.. _quickstart:

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
    <Color html="#ff1900" rgb=(1.0, 0.1, 0.0)>
    >>> c = c + Green(0.1)
    >>> c
    <Color html="#ff1900" rgb=(1.0, 0.1, 0.0)>
    >>> c.lightness
    Lightness(0.5)
    >>> c = c * Lightness(0.5)
    >>> c
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>

Numerous attributes are provided to enable conversion of the RGB representation
to other systems::

    >>> c.rgb
    RGB(red=Red(0.5), green=Green(0.25), blue=Blue(0.0))
    >>> c.rgb_bytes
    RGB(red=127, green=63, blue=0)
    >>> c.rgb_565
    31200
    >>> c.hls
    HSV(hue=Hue(0.083333333333333), lightness=Lightness(0.25), saturation=Saturation(1.0))
    >>> c.cie_xyz
    XYZ(x=0.10647471144683732, y=0.0819048964489466, z=0.010202272707313633)
    >>> c.cie_lab
    Lab(L=34.376494620040376, a=23.890819210881016, b=44.69197916172735)

Equivalent constructors exist for all these systems::

    >>> Color.from_rgb(0.5, 0.25, 0.0)
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>
    >>> Color.from_rgb_bytes(127, 63, 0)
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>
    >>> Color.from_rgb_565(31200)
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>
    >>> Color.from_hls(*c.hls)
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>
    >>> Color.from_cie_xyz(*c.cie_xyz)
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>
    >>> Color.from_cie_lab(*c.cie_lab)
    <Color html="#7f3f00" rgb=(0.5, 0.25, 0.0)>

Finally, color differences can be examined by simple subtraction:

XXX TBC

.. _extended color keywords: https://www.w3.org/TR/css3-color/#svg-color

