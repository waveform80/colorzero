# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
#
# Copyright (c) 2016-2021 Dave Jones <dave@waveform.org.uk>
#
# SPDX-License-Identifier: BSD-3-Clause

"Defines tuples and mappings to represent named styles."

import re
import sys
from collections import namedtuple
from collections.abc import Mapping, MutableMapping

from .color import Color, Default


class Style(namedtuple('Style', ('fg', 'bg'))):
    """
    Represents a named "style" with a foreground (:attr:`fg`) and background
    (:attr:`bg`) :class:`Color` (or :data:`Default`).

    If *fg* is an instance of :class:`Color` it is accepted verbatim.
    Otherwise, a :class:`Color` will be constructed with its value. Likewise
    for *bg*, which defaults to :data:`Default` if not specified.
    """
    def __new__(cls, fg, bg=Default):
        return super().__new__(
            cls,
            fg if isinstance(fg, (type(Default), Color)) else Color(fg),
            bg if isinstance(bg, (type(Default), Color)) else Color(bg)
        )


class BaseStyles(MutableMapping):
    """
    Represents a mapping of (arbitrary) names to :class:`Style` instances. This
    is an abstract base class; most users will be more interested in the
    concrete descendants: :class:`HTMLStyles` or :class:`TermStyles` which can
    be used with format strings to produce styled output.
    """
    def __init__(self, styles=None, **kwargs):
        if styles is None:
            styles = kwargs
        if not isinstance(styles, Mapping):
            raise ValueError('Initial styles must be provided as a mapping '
                             'or as keyword arguments')
        # This may seem inefficient, but causes every item to pass through
        # __setitem__, which descendants may override with additional rules
        # (see HTMLStyles for an example)
        self._styles = {}
        for name, entry in styles.items():
            self[name] = entry
        self._state = None

    def reset(self):
        """
        Reset the "current" style to one with :data:`Default` foreground and
        background.

        This is useful when one stylesheet is repeatedly used to format
        strings, and you wish to guarantee that the style is reset before the
        next formatting operation. For example:
        """
        if self._state:
            self._state = None
            return 'reset'
        else:
            return ''

    def __getitem__(self, key):
        return self._styles[key]

    def __setitem__(self, key, value):
        if not isinstance(key, str):
            raise ValueError('Style names must be strings')
        self._styles[key] = (
            value if isinstance(value, Style) else
            Style(value, Default) if isinstance(value, Color) else
            Style(*value) if isinstance(value, tuple) else
            Style(Default, Default) if value is None else
            Style(value)
        )

    def __delitem__(self, key):
        del self._styles[key]

    def __len__(self):
        return len(self._styles)

    def __iter__(self):
        return iter(self._styles)

    def __repr__(self):
        return (
            '{self.__class__.__name__}({self._styles!r})'.format(self=self))

    def __format__(self, spec):
        raise NotImplementedError


class StripStyles(BaseStyles):
    """
    A degenerate stylesheet class that always returns the empty string for
    all formatting operations, and the :meth:`reset` method.
    """
    # pylint: disable=too-many-ancestors

    def reset(self):
        super().reset()
        return ''

    def __format__(self, format_spec):
        return ''


class HTMLStyles(BaseStyles):
    """
    A stylesheet that outputs `HTML elements`_ when formatting strings.

    The name of the elements produced is specified by the *tag* argument,
    which defaults to "span". Style names must be valid CSS identifiers, or
    escapable to valid CSS identifiers (in practice, this means no spaces, and
    no empty strings). A :exc:`ValueError` will be raised if you attempt to
    assign such a key.

    The :meth:`stylesheet` method can be used to output a valid CSS stylesheet
    to be used with the generated HTML.

    .. _HTML elements: https://developer.mozilla.org/en-US/docs/Glossary/Element
    """
    # pylint: disable=too-many-ancestors

    def __init__(self, styles=None, *, tag='span', **kwargs):
        super().__init__(styles=styles, **kwargs)
        self.tag = tag

    def _open_tag(self, class_name):
        return '<{self.tag} class="{class_name}">'.format(
            self=self, class_name=class_name)

    def _close_tag(self):
        return '</{self.tag}>'.format(self=self)

    @staticmethod
    def _escape_css_name(name):
        # Based on information from the Token Railroad Diagrams in the working
        # draft of CSS Syntax Module Level 3 from:
        # https://drafts.csswg.org/css-syntax/#ident-token-diagram
        maxchar = chr(sys.maxunicode)
        unescaped_first = re.compile(
            '[a-zA-Z_\x7f-{maxchar}-]'.format(maxchar=maxchar))
        unescaped = re.compile(
            '[a-zA-Z0-9_\x7f-{maxchar}-]'.format(maxchar=maxchar))
        result = ''
        for i, char in enumerate(name):
            regex = (
                unescaped_first
                if i == 0 or (name[0] == '-' and i == 1) else
                unescaped)
            match = regex.match(char)
            if match:
                result += char
            else:
                result += '\\{n:x} '.format(n=ord(char))
        return result

    def reset(self):
        if super().reset():
            return self._close_tag()
        else:
            return ''

    def stylesheet(self, prefix=''):
        """
        A generator method that yields rules of a CSS stylesheet for all
        defined styles. The *prefix*, if given, specifies anything that should
        be output before each rule such as any parent `CSS selectors`_.

        For example::

            >>> from colorzero import *
            >>> styles = HTMLStyles(warn='red', info='blue', reset=None)
            >>> print('\\n'.join(styles.stylesheet('div.body ')))
            div.body span.warn { color: rgb(255, 0, 0); background-color: inherit; }
            div.body span.info { color: rgb(0, 0, 255); background-color: inherit; }
            div.body span.reset { color: inherit; background-color: inherit; }

        .. _CSS selectors: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Selectors
        """
        for name, style in self.items():
            yield (
                '{prefix}{tag}.{name} {{ '
                'color: {style.fg:css}; '
                'background-color: {style.bg:css}; '
                '}}'.format(
                    prefix=prefix, tag=self.tag,
                    name=self._escape_css_name(name), style=style))

    def __setitem__(self, key, value):
        if not key:
            raise ValueError('Style names for HTMLStyles cannot be empty')
        if ' ' in key:
            raise ValueError('Style names for HTMLStyles cannot contain space')
        super().__setitem__(key, value)

    def __format__(self, format_spec):
        new_state = self[format_spec]
        if new_state.fg == new_state.bg == Default:
            return self.reset()
        else:
            result = '' if self._state is None else self._close_tag()
            # NOTE: We don't test whether the actual mapped colors have changed
            # as a new span *should* be emitted anyway (the class may imply
            # more semantics than simply the element's color)
            self._state = new_state
            return result + self._open_tag(format_spec)


class TermStyles(BaseStyles):
    """
    A stylesheet that outputs `ANSI escape codes`_.

    The *term_colors* argument specifies the sorts of codes produced. This can
    be:

    * "8" - the default, indicating only the original 8 DOS colors (black, red,
      green, yellow, blue, magenta, cyan, and white) are supported.
      Technically, 16 foreground colors are supported via use of the "bold"
      style for "intense" colors, if the terminal supports this.

    * "256" - indicates the terminal supports 256 colors via `8-bit color ANSI
      codes`_

    * "16m" - indicating the terminal supports ~16 million colors via `24-bit
      color ANSI codes`_

    .. _ANSI escape codes: https://en.wikipedia.org/wiki/ANSI_escape_code
    .. _8-bit color ANSI codes: https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
    .. _24-bit color ANSI codes: https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
    """
    # pylint: disable=too-many-ancestors

    def __init__(self, styles=None, *, term_colors='8', **kwargs):
        super().__init__(styles=styles, **kwargs)
        self.term_colors = term_colors

    def reset(self):
        if super().reset():
            return '{}'.format(Default)
        else:
            return ''

    def __format__(self, format_spec):
        new_state = self[format_spec]
        if new_state.fg == new_state.bg == Default:
            return self.reset()
        else:
            # XXX Don't emit unnecessary sequences
            self._state = new_state
            return (
                '{new_state.fg:f{self.term_colors}}'
                '{new_state.bg:b{self.term_colors}}'.format(
                new_state=new_state, self=self))
