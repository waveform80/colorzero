# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
#
# Copyright (c) 2018-2019 Dave Jones <dave@waveform.org.uk>
#
# SPDX-License-Identifier: BSD-3-Clause

"Tests for the colorzero.style module"

import pytest

from colorzero import *


@pytest.fixture
def styles(request):
    return {
        'info': Style('green'),
        'warn': Style('white', 'red'),
        'reset': None,
    }


def test_style_init():
    style = Style(Color('red'), Default)
    assert Style('red', Default) == style
    assert Style('red') == style


def test_styles_init(styles):
    styles = BaseStyles(styles)
    assert BaseStyles(
        info=Style('green'),
        warn=Style('white', 'red'),
        reset=Style(Default, Default)) == styles
    assert BaseStyles(
        info=Color('green'),
        warn=(Color('white'), Color('red')),
        reset=(Default, Default)) == styles
    assert BaseStyles(info='green', warn=('white', 'red'), reset=None) == styles
    with pytest.raises(ValueError):
        BaseStyles('foo')


def test_styles_reset(styles):
    styles = BaseStyles(styles)
    assert not styles.reset()
    styles._state = 'info'
    assert styles.reset()


def test_styles_assignment(styles):
    styles = BaseStyles(styles)
    styles['default'] = None
    with pytest.raises(ValueError):
        styles[0xf00] = None


def test_styles_deletion(styles):
    styles = BaseStyles(styles)
    del styles['info']
    assert 'info' not in styles
    with pytest.raises(KeyError):
        del styles['foo']


def test_styles_read(styles):
    styles = BaseStyles(styles)
    assert len(styles) == 3
    assert set(styles) == {'info', 'warn', 'reset'}


def test_styles_repr(styles):
    styles = BaseStyles(styles)
    s = repr(styles)
    assert s.startswith('BaseStyles({')
    assert s.endswith('})')
    assert "'warn': Style(fg=<Color html='#ffffff' rgb=(1, 1, 1)>, bg=<Color html='#ff0000' rgb=(1, 0, 0)>)" in s
    assert "'info': Style(fg=<Color html='#008000' rgb=(0, 0.501961, 0)>, bg=<Color Default>)" in s
    assert "'reset': Style(fg=<Color Default>, bg=<Color Default>)" in s


def test_strip_styles(styles):
    styles = StripStyles(styles)
    assert styles.reset() == ''
    assert '{styles:info}Hello!'.format(styles=styles) == 'Hello!'
    assert styles.reset() == ''


def test_html_reset(styles):
    styles = HTMLStyles(styles)
    assert styles.reset() == ''
    '{styles:info}Hello!'.format(styles=styles)
    assert styles.reset() == '</span>'


def test_html_tags(styles):
    styles = HTMLStyles(styles, tag='div')
    assert '{styles:info}Hello!{styles:reset}'.format(styles=styles) == (
        '<div class="info">Hello!</div>')


def test_html_escape_css():
    styles = HTMLStyles({
        '666': Color('#666'),
        '-666': Color('#666'),
        '--666': Color('#666'),
        '-foo-bar': Color('red'),
        'αβγ': Color('#f00'),
    })
    assert set(styles.stylesheet()) == {
        'span.\\36 66 { color: rgb(102, 102, 102); background-color: inherit; }',
        'span.-\\36 66 { color: rgb(102, 102, 102); background-color: inherit; }',
        'span.--666 { color: rgb(102, 102, 102); background-color: inherit; }',
        'span.-foo-bar { color: rgb(255, 0, 0); background-color: inherit; }',
        'span.αβγ { color: rgb(255, 0, 0); background-color: inherit; }',
    }


def test_html_assignment():
    styles = HTMLStyles()
    with pytest.raises(ValueError):
        styles[''] = None
    with pytest.raises(ValueError):
        styles['foo bar'] = Color('red')


def test_term_reset(styles):
    styles = TermStyles(styles)
    assert styles.reset() == ''
    '{styles:info}Hello!'.format(styles=styles)
    assert styles.reset() == '[0m'


def test_term_format(styles):
    styles = TermStyles(styles)
    assert '{styles:info}Status{styles:reset}: OK'.format(styles=styles) == (
        '[22;32m[49mStatus[0m: OK')
