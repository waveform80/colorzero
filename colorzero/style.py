# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
#
# Copyright (c) 2016-2021 Dave Jones <dave@waveform.org.uk>
#
# SPDX-License-Identifier: BSD-3-Clause

"Defines tuples and mappings to represent named styles."

import re
from string import Formatter
from collections import namedtuple
from collections.abc import Mapping, MutableMapping

from .color import Color


class Style(namedtuple('Style', ('fore', 'back'))):
    def __new__(cls, fore, back=None):
        return super().__new__(
            cls,
            fore if isinstance(fore, Color) else Color(fore),
            None if back is None else
            back if isinstance(back, Color) else Color(back)
        )

    _format_re = re.compile(
        r'^('
        r'(?P<dialect>html|css(rgb|hsl)?|8|256|16[mM])?'
        r')$')
    def __format__(self, format_spec):
        m = Style._format_re.match(format_spec)
        if not m:
            raise ValueError(
                'Invalid format {!r} for Style'.format(format_spec))
        dialect = m.group('dialect')
        if dialect == 'html':
            template = '<span style="{self:css}">'
        elif dialect.startswith('css'):
            template = 'color: {self.fore:{dialect}};'
            if self.back is not None:
                template += ' background-color: {self.back:{dialect}};'
        else:
            template = '{self.fore:f{dialect}}'
            if self.back is not None:
                template += '{self.back:b{dialect}}'
        return template.format(self=self, dialect=dialect)


class Default:
    def __format__(self, format_spec):
        m = Style._format_re.match(format_spec)
        if not m:
            raise ValueError(
                'Invalid format {!r} for Style'.format(format_spec))
        return ''


class Reset:
    def __format__(self, format_spec):
        m = Style._format_re.match(format_spec)
        if not m:
            raise ValueError(
                'Invalid format {!r} for Style'.format(format_spec))
        dialect = m.group('dialect')
        if dialect == 'html':
            return '</span>'
        elif dialect.startswith('css'):
            return 'color: inherit; background-color: inherit;'
        else:
            return '{color:0}'.format(color=Color(0, 0, 0))


class Styles(MutableMapping):
    def __init__(self, styles=None, *, format=None, default=None, **kwargs):
        if styles is None:
            styles = kwargs
        if not isinstance(styles, Mapping):
            raise ValueError('Initial styles must be provided as a mapping '
                             'or as keyword arguments')
        if not all(isinstance(value, (Default, Reset, Style))
                   for value in styles.values()):
            raise ValueError('All styles must be instances of Style, Reset, '
                             'or Default')
        self._styles = styles
        self.default = default
        self.format = format

    def __getitem__(self, key):
        return self._styles[key]

    def __setitem__(self, key, value):
        if not isinstance(value, Style):
            raise ValueError('value is not na instance of Style')
        self._styles[key] = value

    def __delitem__(self, key):
        del self._styles[key]

    def __len__(self):
        return len(self._styles)

    def __iter__(self):
        return iter(self._styles)

    def __repr__(self):
        return (
            '{self.__class__.__name__}(format={self.format!r}, '
            'styles={self._styles!r}'.format(self=self))

    def __format__(self, format_spec):
        if self.default is not None:
            style = self.get(format_spec, self.default)
        else:
            style = self[format_spec]
        return '{style:{self.format}}'.format(self=self, style=style)
