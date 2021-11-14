.. The colorzero color library
..
.. Copyright (c) 2016-2019 Dave Jones <dave@waveform.org.uk>
..
.. SPDX-License-Identifier: BSD-3-Clause

.. _api_style:

============
API - Styles
============

.. currentmodule:: colorzero

The colorzero library also includes a series of classes which act a bit like
stylesheets for formatting large strings. Different classes are used to produce
different types of output, such as :class:`HTMLStyles` for HTML (and CSS)
output, or :class:`TermStyles` for ANSI terminal output.


Style Class
===========

.. autoclass:: Style


Stylesheets
===========

Stylesheets are constructed with an initial mapping of names to suitable style
values, or can be constructed with a set of keyword arguments which will be
used to create the initial mapping:

.. code-block:: pycon

    >>> style = TermStyles({
    ... 'info': Style(Color('blue'), Default),
    ... 'warn': Style(Color('white'), Color('red')),
    ... })

The style values can either be a :class:`Style` instance, or anything that
could be used to construct a :class:`Style` instance, including a
:class:`Color` instance, or valid arguments that could be used to construct a
:class:`Color` instance, or a tuple of two such values (representing the "fg"
and "bg" components respectively). The value :data:`None` can also be
specified, which will be converted to a :class:`Style` with :data:`Default` as
both foreground and background:

.. code-block:: pycon

    >>> style2 = TermStyles({
    ... 'info': 'blue',
    ... 'warn': ('white', 'red'),
    ... })
    >>> style == style2
    True

Style mappings are mutable (like an ordinary :class:`dict`), but keys must be
strings, and values will be converted in the same manner as during
construction:

.. code-block:: pycon

    >>> style['error'] = 'red'
    >>> style
    TermStyles({'info': Style(fg=<Color html='#0000ff' rgb=(0, 0, 1)>,
    bg=<Color Default>), 'warn': Style(fg=<Color html='#ffffff'
    rgb=(1, 1, 1)>, bg=<Color html='#ff0000' rgb=(1, 0, 0)>), 'error':
    Style(fg=<Color html='#ff0000' rgb=(1, 0, 0)>, bg=<Color Default>)})

Style mappings can be used with format strings to generate output in a variety
of styles. The format spec for each template must be the name of an entry
within the mapping. For example:

.. code-block:: pycon

    >>> from colorzero import *
    >>> s = TermStyles(warn='red', reset=None)
    >>> f'{s:warn}Warning{s:reset}: Do not push the button!'
    '\x1b[1;31m\x1b[49mWarning\x1b[0m: Do not push the button!'

It is important to bear in mind that the formatting behaviour is stateful.
In other words, as the styles are substituted into a string, the instance
is keeping track of the current style. This permits descendants like
:class:`HTMLStyles` to determine when tags need closing or for
:class:`TermStyles` to determine when to reset foreground or background
colors:

.. code-block:: pycon

    >>> s = HTMLStyles(warn='red', reset=None)
    >>> print(f'{s:warn}This is red ')
    <span class="warn">This is red
    >>> print('and this will still be red ')
    and this will still be red
    >>> print(f'because the span has not closed yet{s:reset}')
    because the span has not closed yet</span>

If the current foreground and background style is not :data:`Default` once
formatting is complete, you may need to call :meth:`reset` before
continuing to format the next string to ensure correct behaviour. The
:meth:`reset` method will return whatever string would be needed to reset the
current style to the default (if any):

.. code-block:: pycon

    >>> print(f'{s:warn}This is red')
    <span class="warn">This is red
    >>> print(s.reset())
    </span>


BaseStyles Class
================

.. autoclass:: BaseStyles


StripStyles Class
=================

.. autoclass:: StripStyles


HTMLStyles Class
================

.. autoclass:: HTMLStyles


TermStyles Class
================

.. autoclass:: TermStyles
