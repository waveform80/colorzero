.. The colorzero color library
..
.. Copyright (c) 2016-2019 Dave Jones <dave@waveform.org.uk>
..
.. SPDX-License-Identifier: BSD-3-Clause

.. _api_color:

===========
API - Color
===========

.. currentmodule:: colorzero

The colorzero library includes a comprehensive :class:`Color` class which
is capable of converting between numerous color representations and calculating
color differences. Various ancillary classes can be used to manipulate aspects
of a color.


Color Class
===========

This the primary class in the package, and often the only class you'll need or
want to interact with. It has an extremely flexible constructor, along with
numerous explicit constructors, and attributes for conversion to other color
systems.

.. autoclass:: Color


.. _format:

Format Strings
==============

Instances of :class:`Color` can be used in format strings to output various
representations of a color, including HTML sequences and ANSI escape sequences
to color terminal output. Format specifications can be used to modify the
output to support different terminal types. For example:

.. code-block:: pycon

    >>> red = Color('red')
    >>> green = Color('green')
    >>> blue = Color('#47b')
    >>> print(f"{red:html}")
    #ff0000
    >>> print(repr(f"{red}Red{red:0} Alert!"))
    '\\x1b[1;31mRed\\x1b[0m Alert!'
    >>> print(repr(f"The grass is {green:16m}greener{green:0}."))
    'The grass is \\x1b[38;2;0;128;0mgreener\\x1b[0m.'
    >>> print(repr(f"{blue:b16m}Blue skies{blue:0}"))
    '\\x1b[48;2;68;119;187mBlue skies\\x1b[0m'

The format specification is one of:

* "html" - the color will be output as the common 7-character HTML represention
  of #RRGGBB where RR, GG, and BB are the red, green and blue components
  expressed as a single hexidecimal byte

* "css" or "cssrgb" - the color will be output in CSS' functional notation
  rgb(*r*, *g*, *b*) where *r*, *g*, and *b* are decimal representations of the
  red, green, and blue components in the range 0 to 255

* "csshsl" - the color will be output in CSS' function notation hue(*h*\deg,
  *s*\%, *l*\%) where *h*, *s*, and *l* are the hue (expressed in degrees),
  saturation, and lightness (expressed as percentages)

* One of the ANSI format specifications which consist of an optional foreground
  / background specifier (the letters "f" or "b") followed by an optional
  terminal type identifer, which is one of:

  - "8" - the default, indicating only the original 8 DOS colors (black, red,
    green, yellow, blue, magenta, cyan, and white) are supported. Technically,
    16 foreground colors are supported via use of the "bold" style for
    "intense" colors, if the terminal supports this.

  - "256" - indicates the terminal supports 256 colors via `8-bit color ANSI
    codes`_

  - "16m" - indicating the terminal supports ~16 million colors via `24-bit
    color ANSI codes`_

"0" can also be specified to indicate that the style should be reset, but this
is deprecated. If specified with the optional foreground / background
specifier, "0" resets only the foreground / background color. If specified
alone it resets all styles. More formally:

.. code-block:: bnf

    <term_fore_back> ::= "" | "f" | "b"
    <term_type>      ::= "" | "0" | "8" | "256" | "16m"
    <term>           ::= <term_fore_back> <term_type>
    <html>           ::= "html"
    <css>            ::= "css" ("rgb" | "hsl")?
    <format_spec>    ::= <html> | <css> | <term>

.. versionadded:: 1.1
    The ability to output ANSI codes via format strings, and the
    customization of :func:`repr` output.

.. versionadded:: 1.2
    The ability to output HTML and CSS representations via format strings

.. deprecated:: 2.1
    Use of "0" as a reset indicator; use the new :data:`Default` singleton
   instead

.. _8-bit color ANSI codes: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
.. _24-bit color ANSI codes: https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit


Default Singleton
=================

The :data:`Default` singleton exists as a color which represents the "default"
for whatever environment it's rendered in. For example, when using in a format
string for CSS, it renders as "inherit" (which is the CSS keyword indicating
that a block should inherit its color from its enclosing parent, which is the
default). Alternatively, when used with the terminal format strings ("8",
"256", "16m") it outputs the ANSI sequence to reset colors to the terminal's
default (whatever that may be).

.. autodata:: Default


Manipulation Classes
====================

These manipulation classes are used in conjunction with the standard arithmetic
addition, subtraction, and multiplication operators to calculate new
:class:`Color` instances.

.. autoclass:: Red

.. autoclass:: Green

.. autoclass:: Blue

.. autoclass:: Hue

.. autoclass:: Saturation

.. autoclass:: Lightness

.. autoclass:: Luma


Difference Functions
====================

.. autofunction:: euclid

.. autofunction:: cie1976

.. autofunction:: cie1994g

.. autofunction:: cie1994t

.. autofunction:: ciede2000


Easing Functions
================

These functions can be used with the :meth:`Color.gradient` method to control
the progression of the fade between the two colors.

.. autofunction:: linear

.. autofunction:: ease_in

.. autofunction:: ease_out

.. autofunction:: ease_in_out
