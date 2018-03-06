.. -*- rst -*-

=========
colorzero
=========

colorzero is a color manipulation library for Python (yes, *another* one) which
aims to be reasonably simple to use and "pythonic" in nature.

It does *not* aim to be as comprehensive, powerful, or that matter as *correct*
as, say, `colormath`_.  colorzero originally grew out of work on my `picamera`_
project, hence it's intended to be sufficiently simple that school children can
use it without having to explain color spaces and illuminants. However, it does
aim to be useful to a wide range of skills, hence it does include basic
facilities for `CIE Lab`_ representations, and `Delta-E`_ calculations should
you need them.

The major difference between colorzero and other libraries (`grapefruit`_,
`colormath`_, etc.) is that its ``Color`` class is a ``namedtuple`` descendent.
This means it is immutable; you cannot *directly* change the attributes of a
``Color`` instance. The major advantage of this is that instances can be used
as keys in dictionaries, or placed in sets.

Manipulation of ``Color`` instances is done by typical operations with other
classes the result of which is a new ``Color`` instance. For example::

    >>> from colorzero import Color, Red
    >>> c = Color('green')
    >>> c
    <Color html="#008000" rgb=(0.0, 0.5, 0.5)>
    >>> c + Red(0.1)
    <Color html="#198000" rgb=(0.1, 0.5, 0.0)>
    >>> c += Red(0.1)
    >>> c.hue
    Hue(deg=108.046875)
    >>> c.saturation
    Saturation(1.0)
    >>> c * Saturation(0.0)
    <Color html="#404040" rgb=(0.25098, 0.25098, 0.25098)>

Links
=====

* The code is licensed under the `BSD license`_
* The `source code`_ can be obtained from GitHub, which also hosts the `bug
  tracker`_
* The `documentation`_ (which includes installation, quick-start examples, and
  lots of code recipes) can be read on ReadTheDocs
* Packages can be downloaded from `PyPI`_, but reading the installation
  instructions is more likely to be useful


.. _picamera: https://picamera.readthedocs.io/
.. _colormath: https://python-colormath.readthedocs.io/
.. _grapefruit: https://grapefruit.readthedocs.io/
.. _CIE Lab: https://en.wikipedia.org/wiki/Lab_color_space
.. _Delta-E: https://en.wikipedia.org/wiki/Color_difference
.. _PyPI: http://pypi.python.org/pypi/colorzero/
.. _documentation: http://colorzero.readthedocs.io/
.. _source code: https://github.com/waveform80/colorzero
.. _bug tracker: https://github.com/waveform80/colorzero/issues
.. _BSD license: http://opensource.org/licenses/BSD-3-Clause

