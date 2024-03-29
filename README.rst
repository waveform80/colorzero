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
as keys in dictionaries (for simple `LUTs`_), or placed in sets.

Manipulation of ``Color`` instances is done by typical operations with other
classes the result of which is a new ``Color`` instance. For example:

.. code:: pycon

    >>> from colorzero import *
    >>> Color('red') + Color('blue')
    <Color html='#ff00ff' rgb=(1, 0, 1)>
    >>> Color('magenta') - Color('red')
    <Color html='#0000ff' rgb=(0, 0, 1)>
    >>> Color('red') - Red(0.5)
    <Color html='#800000' rgb=(0.5, 0, 0)>
    >>> Color('green') + Color('grey').red
    <Color html='#808000' rgb=(0.501961, 0.501961, 0)>
    >>> Color.from_hls(0.5, 0.5, 1.0)
    <Color html='#00ffff' rgb=(0, 1, 1)>
    >>> Color.from_hls(0.5, 0.5, 1.0) * Lightness(0.8)
    <Color html='#00cccc' rgb=(0, 0.8, 0.8)>
    >>> (Color.from_hls(0.5, 0.5, 1.0) * Lightness(0.8)).hls
    HLS(h=0.5, l=0.4, s=1.0)

Another interesting facility is the custom format strings that ``Color``
instances support, making them convenient for direct use in HTML or CSS
templating:

.. code:: pycon

    >>> red = Color('red')
    >>> black = Color('black')
    >>> stylesheet = f"""\
    .warning {{ color: {red:css}; }}
    .table {{ border: 1px solid {black:html}; }}
    """
    >>> print(stylesheet)
    .warning { color: rgb(255, 0, 0); }
    .table { border: 1px solid #000000; }

Or for in colorful terminal output:

.. code:: pycon

    >>> print(f'This is a {red:8}warning!{Default}')
    This is a warning!
    >>> f'This is a {red:8}warning!{Default}'
    'This is a \x1b[1;31mwarning!\x1b[0m'

(on supported terminals, the first line of output above will print "warning!"
in red)


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
.. _LUTs: https://en.wikipedia.org/wiki/Lookup_table#Lookup_tables_in_image_processing
