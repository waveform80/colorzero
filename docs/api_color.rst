.. _api_color:

===
API
===

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

Instances of :class:`Color` can be used in format strings to output ANSI escape
sequences to color text. Format specifications can be used to modify the output
to support different terminal types. For example:

.. code-block:: pycon

    >>> red = Color('red')
    >>> green = Color('green')
    >>> blue = Color('#47b')
    >>> print(repr("{red}Red{red:0} Alert!".format(red=red)))
    '\\x1b[1;31mRed\\x1b[0m Alert!'
    >>> print(repr("The grass is {green:16m}greener{green:0}.".format(
    ... green=green)))
    'The grass is \\x1b[38;2;0;128;0mgreener\\x1b[0m.'
    >>> print(repr("{blue:b16m}Blue skies{blue:0}".format(blue=blue)))
    '\\x1b[48;2;68;119;187mBlue skies\\x1b[0m'

The format specification is an optional foreground / background specifier (the
letters "f" or "b") followed by an optional terminal type identifer, which is
one of:

* "8" - the default, indicating only the original 8 DOS colors are supported
  (technically, 16 foreground colors are supported via use of the "bold" style
  for "intense" colors)

* "256" - indicates the terminal supports 256 colors via `8-bit color ANSI
  codes`_

* "16m" - indicating the terminal supports ~16 million colors via `24-bit color
  ANSI codes`_

Alternately, "0" can be specified indicating that the style should be
reset. If specified with the optional foreground / background specifier,
"0" resets only the foreground / background color. If specified alone it
resets all styles. More formally:

.. code-block:: bnf

    <fore_back>   ::= "" | "f" | "b"
    <type>        ::= "" | "0" | "8" | "256" | "16m"
    <format_spec> ::= <fore_back> <type>

.. versionadded:: 1.1
    The ability to output ANSI codes via format strings, and the
    customization of :func:`repr` output.

.. _8-bit color ANSI codes: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
.. _24-bit color ANSI codes: https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit


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
