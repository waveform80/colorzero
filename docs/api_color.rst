.. _api_color:

===
API
===

.. currentmodule:: colorzero

The colorzero library includes a comprehensive :class:`Color` class which
is capable of converting between numerous color representations and calculating
color differences. Various ancillary classes can be used to manipulate aspects
of a color.


Color
=====

This the primary class in the package, and often the only class you'll need or
want to interact with. It has an extremely flexible constructor, along with
numerous explicit constructors, and attributes for conversion to other color
systems.

.. autoclass:: Color


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
