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
