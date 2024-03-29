# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
#
# Copyright (c) 2018-2019 Dave Jones <dave@waveform.org.uk>
#
# SPDX-License-Identifier: BSD-3-Clause

"Tests for the colorzero.color module"

from math import sqrt, isclose

import pytest

from colorzero import *


def verify_color(color1, color2, abs_tol=1e-7):
    for elem1, elem2 in zip(color1, color2):
        assert isclose(elem1, elem2, abs_tol=abs_tol)


def test_color_new():
    verify_color(Color(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color(1, 1, 1), (1.0, 1.0, 1.0))
    verify_color(Color(255, 255, 255), (1.0, 1.0, 1.0))
    verify_color(Color(r=1, g=0, b=0), (1.0, 0.0, 0.0))
    verify_color(Color(r=255, g=255, b=255), (1.0, 1.0, 1.0))
    verify_color(Color(red=1, green=0, blue=0.0), (1.0, 0.0, 0.0))
    verify_color(Color(red=255, green=255, blue=255), (1.0, 1.0, 1.0))
    verify_color(Color(y=1, u=0, v=0), (1.0, 1.0, 1.0))
    verify_color(Color(y=16, u=128, v=128), (0.0, 0.0, 0.0))
    verify_color(Color('red'), (1.0, 0.0, 0.0))
    verify_color(Color(b'red'), (1.0, 0.0, 0.0))
    verify_color(Color((1, 0, 0)), (1.0, 0.0, 0.0))
    verify_color(Color(RGB(1, 0, 0)), (1.0, 0.0, 0.0))
    verify_color(Color(0), (0.0, 0.0, 0.0))
    verify_color(Color(0xff), (1.0, 0.0, 0.0))
    verify_color(Color(0xff0000), (0.0, 0.0, 1.0))
    verify_color(Color(l=100, a=0, b=0), (1.0, 1.0, 1.0))
    verify_color(Color(l=100, u=0, v=0), (1.0, 1.0, 1.0))
    verify_color(Color(h=0, l=1, s=0), (1.0, 1.0, 1.0))
    verify_color(Color(hue=0, lightness=1, saturation=0), (1.0, 1.0, 1.0))
    verify_color(Color(h=0, s=0, v=1), (1.0, 1.0, 1.0))
    verify_color(Color(hue=0, saturation=0, value=1), (1.0, 1.0, 1.0))
    verify_color(Color(c=0, m=1, y=1), (1.0, 0.0, 0.0))
    verify_color(Color(cyan=0, magenta=1, yellow=1), (1.0, 0.0, 0.0))
    verify_color(Color(c=0, m=1, y=1, k=0), (1.0, 0.0, 0.0))
    verify_color(Color(cyan=0, magenta=1, yellow=1, black=0), (1.0, 0.0, 0.0))
    with pytest.raises(ValueError):
        Color()
    with pytest.raises(ValueError):
        Color(foo=1, bar=2)
    with pytest.raises(ValueError):
        Color((1, 0, 0, 0))
    with pytest.raises(ValueError):
        Color(0.1)


def test_color_from_rgb():
    verify_color(Color.from_rgb(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_rgb(1, 1, 1), (1.0, 1.0, 1.0))
    verify_color(Color.from_rgb(2, 1, 1), (1.0, 1.0, 1.0))
    verify_color(Color.from_rgb(1, -1, 1), (1.0, 0.0, 1.0))
    verify_color(Color.from_rgb(r=1, g=0, b=0), (1.0, 0.0, 0.0))


def test_color_from_rgb565():
    verify_color(Color.from_rgb565(0x0000), (0.0, 0.0, 0.0))
    verify_color(Color.from_rgb565(0xffff).rgb, (1.0, 1.0, 1.0))
    verify_color(Color.from_rgb565(1).rgb_bytes, (0, 0, 8))
    verify_color(Color.from_rgb565(1 << 5).rgb_bytes, (0, 4, 0))
    verify_color(Color.from_rgb565(1 << 11).rgb_bytes, (8, 0, 0))


def test_color_from_rgb_bytes():
    verify_color(Color.from_rgb_bytes(1, 1, 1).rgb_bytes, (1, 1, 1))
    verify_color(Color.from_rgb_bytes(255, 255, 255), (1.0, 1.0, 1.0))
    verify_color(Color.from_rgb_bytes(r=255, g=255, b=255), (1.0, 1.0, 1.0))


def test_color_from_yuv():
    verify_color(Color.from_yuv(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_yuv(1, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_yuv(-1, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_yuv(2, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_yuv(y=0.299, u=-0.14713769751693, v=0.615),
                 (1.0, 0.0, 0.0))


def test_color_from_yuv_bytes():
    verify_color(Color.from_yuv_bytes(16, 128, 128), (0.0, 0.0, 0.0))
    verify_color(Color.from_yuv_bytes(235, 128, 128), (1.0, 1.0, 1.0))
    verify_color(Color.from_yuv_bytes(-255, 128, 128), (0.0, 0.0, 0.0))
    verify_color(Color.from_yuv_bytes(512, 128, 128), (1.0, 1.0, 1.0))
    verify_color(Color.from_yuv_bytes(81, 90, 240), (1.0, 0.0, 0.0))


def test_color_from_yiq():
    verify_color(Color.from_yiq(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_yiq(1, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_yiq(2, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_yiq(-1, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_yiq(0.3, 0.599, 0.213), (1.0, 0.0, 0.0))


def test_color_from_xyz():
    verify_color(Color.from_xyz(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_xyz(0.95047, 1, 1.08883), (1.0, 1.0, 1.0))
    verify_color(Color.from_xyz(0.4124564, 0.2126729, 0.0193339),
                 (1.0, 0.0, 0.0), abs_tol=1e-5)


def test_color_from_lab():
    verify_color(Color.from_lab(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_lab(100, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_lab(53.24, 80.1, 67.2), (1.0, 0.0, 0.0),
                 abs_tol=1e-4)


def test_color_from_luv():
    verify_color(Color.from_luv(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_luv(100, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_luv(53.24079, 175.01503, 37.75643),
                 (1.0, 0.0, 0.0), abs_tol=1e-5)


def test_color_from_hls():
    verify_color(Color.from_hls(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_hls(0, -1, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_hls(0, 1, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_hls(0, 2, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_hls(0, 0.5, 1), (1.0, 0.0, 0.0))


def test_color_from_hsv():
    verify_color(Color.from_hsv(0, 0, 0), (0.0, 0.0, 0.0))
    verify_color(Color.from_hsv(0, 0, 1), (1.0, 1.0, 1.0))
    verify_color(Color.from_hsv(0, 0, 2), (1.0, 1.0, 1.0))
    verify_color(Color.from_hsv(0, 1, 1), (1.0, 0.0, 0.0))


def test_color_from_cmy():
    verify_color(Color.from_cmy(1, 1, 1), (0.0, 0.0, 0.0))
    verify_color(Color.from_cmy(2, 1, 1), (0.0, 0.0, 0.0))
    verify_color(Color.from_cmy(0, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_cmy(-1, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_cmy(0, 1, 1), (1.0, 0.0, 0.0))


def test_color_from_cmyk():
    verify_color(Color.from_cmyk(0, 0, 0, 1), (0.0, 0.0, 0.0))
    verify_color(Color.from_cmyk(0, 0, 0, 0), (1.0, 1.0, 1.0))
    verify_color(Color.from_cmyk(0, 1, 1, 0), (1.0, 0.0, 0.0))


def test_color_add():
    verify_color(Color('red') + Color('blue'), Color('magenta'))
    verify_color(Color('red') + Color('white'), Color('white'))
    verify_color(Color('red') + Red(1), Color('red'))
    verify_color(Color('red') + Green(1), Color('yellow'))
    verify_color(Color('red') + Blue(1), Color('magenta'))
    verify_color(Color('red') + Hue(0), Color('red'))
    verify_color(Color('red') + Lightness(0.5), Color('white'))
    verify_color(Color('red') + Saturation(1), Color('red'))
    verify_color(Color('red') + Luma(1), Color('white'))
    verify_color(Green(1) + Color('red'), Color('yellow'))
    with pytest.raises(TypeError):
        Color('red') + 1
    with pytest.raises(TypeError):
        1 + Color('red')


def test_color_sub():
    verify_color(Color('magenta') - Color('blue'), Color('red'))
    verify_color(Color('magenta') - Color('white'), Color('black'))
    verify_color(Color('magenta') - Red(1), Color('blue'))
    verify_color(Color('magenta') - Green(1), Color('magenta'))
    verify_color(Color('magenta') - Blue(1), Color('red'))
    verify_color(Color('magenta') - Hue(0), Color('magenta'))
    verify_color(Color('magenta') - Lightness(0.5), Color('black'))
    verify_color(Color('magenta') - Saturation(1), Color(0.5, 0.5, 0.5))
    verify_color(Color('magenta') - Luma(1), Color('black'))
    verify_color(Red(1) - Color('magenta'), Color(0, 0, 0))
    verify_color(Green(1) - Color('magenta'), Color(0, 1, 0))
    verify_color(Blue(1) - Color('magenta'), Color(0, 0, 0))
    with pytest.raises(TypeError):
        Color('magenta') - 1
    with pytest.raises(TypeError):
        1 - Color('magenta')


def test_color_mul():
    verify_color(Color('magenta') * Color('blue'), Color('blue'))
    verify_color(Color('magenta') * Color('white'), Color('magenta'))
    verify_color(Color('magenta') * Red(0.5), Color(0.5, 0, 1))
    verify_color(Color('magenta') * Green(0.5), Color('magenta'))
    verify_color(Color('magenta') * Blue(0.5), Color(1, 0, 0.5))
    verify_color(Color('magenta') * Hue(0), Color('red'))
    verify_color(Color('magenta') * Lightness(0.5), Color(0.5, 0.0, 0.5))
    verify_color(Color('magenta') * Saturation(0), Color(0.5, 0.5, 0.5))
    verify_color(Color('magenta') * Luma(1), Color('magenta'))
    verify_color(Red(0.5) * Color('magenta'), Color(0.5, 0, 1))
    with pytest.raises(TypeError):
        Color('magenta') * 1
    with pytest.raises(TypeError):
        1 * Color('magenta')


def test_color_repr():
    save_style = Color.repr_style
    try:
        Color.repr_style = 'default'
        assert repr(Color('red')) == "<Color html=%r rgb=(1, 0, 0)>" % '#ff0000'
        Color.repr_style = 'html'
        assert repr(Color('red')) == "Color(%r)" % '#ff0000'
        Color.repr_style = 'rgb'
        assert repr(Color('red')) == "Color(1, 0, 0)"
        Color.repr_style = 'term16m'
        assert repr(Color('red')) == "<Color \x1b[38;2;255;0;0m###\x1b[0m rgb=(1, 0, 0)>"
        Color.repr_style = 'term256'
        assert repr(Color('red')) == "<Color \x1b[38;5;9m###\x1b[0m rgb=(1, 0, 0)>"
        Color.repr_style = 'foo'
        with pytest.raises(ValueError):
            repr(Color('red'))
    finally:
        Color.repr_style = save_style


def test_color_str():
    assert str(Color('black')) == '#000000'
    assert str(Color('red')) == '#ff0000'
    assert str(Color('white')) == '#ffffff'


def test_color_html():
    assert Color('black').html == '#000000'
    assert Color('red').html == '#ff0000'
    assert Color('white').html == '#ffffff'


def test_color_rgb():
    assert Color('black').rgb == RGB(0, 0, 0)
    assert Color('red').rgb == RGB(1, 0, 0)
    assert Color('white').rgb == RGB(1, 1, 1)


def test_color_rgb565():
    assert Color('black').rgb565 == 0
    assert Color('red').rgb565 == 0x1f << 11
    assert Color('white').rgb565 == 0xffff


def test_color_rgb_bytes():
    assert Color('black').rgb_bytes == RGB(0, 0, 0)
    assert Color('red').rgb_bytes == RGB(255, 0, 0)
    assert Color('white').rgb_bytes == RGB(255, 255, 255)


def test_color_yuv():
    verify_color(Color('black').yuv, YUV(0, 0, 0))
    verify_color(Color('white').yuv, YUV(1, 0, 0))
    verify_color(Color('red').yuv, YUV(y=0.299, u=-0.14713, v=0.615),
                 abs_tol=1e-5)


def test_color_yuv_bytes():
    verify_color(Color('black').yuv_bytes, YUV(16, 128, 128))
    verify_color(Color('white').yuv_bytes, YUV(235, 128, 128))
    verify_color(Color('red').yuv_bytes, YUV(82, 90, 240))


def test_color_yiq():
    verify_color(Color('black').yiq, YIQ(0, 0, 0))
    verify_color(Color('white').yiq, YIQ(1, 0, 0))
    verify_color(Color('red').yiq, YIQ(0.3, 0.599, 0.213))


def test_color_hls():
    assert Color('black').hls == HLS(0, 0, 0)
    assert Color('white').hls == HLS(0, 1, 0)
    assert Color('red').hls == HLS(0, 0.5, 1)


def test_color_hsv():
    assert Color('black').hsv == HSV(0, 0, 0)
    assert Color('white').hsv == HSV(0, 0, 1)
    assert Color('red').hsv == HSV(0, 1, 1)


def test_color_cmy():
    assert Color('black').cmy == CMY(1, 1, 1)
    assert Color('white').cmy == CMY(0, 0, 0)
    assert Color('red').cmy == CMY(0, 1, 1)


def test_color_cmyk():
    assert Color('black').cmyk == CMYK(0, 0, 0, 1)
    assert Color('white').cmyk == CMYK(0, 0, 0, 0)
    assert Color('red').cmyk == CMYK(0, 1, 1, 0)


def test_color_xyz():
    verify_color(Color('black').xyz, XYZ(0, 0, 0))
    verify_color(Color('white').xyz, XYZ(0.95047, 1, 1.08883), abs_tol=1e-5)
    verify_color(Color('red').xyz, XYZ(0.41246, 0.21267, 0.01933),
                 abs_tol=1e-5)


def test_color_lab():
    verify_color(Color('black').lab, Lab(0, 0, 0))
    verify_color(Color('white').lab, Lab(100, 0, 0), abs_tol=1e-4)
    verify_color(Color('red').lab, Lab(53.24079, 80.09246, 67.2032),
                 abs_tol=1e-4)


def test_color_luv():
    verify_color(Color('black').luv, Luv(0, 0, 0))
    verify_color(Color('white').luv, Luv(100, 0, 0), abs_tol=1e-4)
    verify_color(Color('red').luv, Luv(53.24079, 175.01503, 37.75643),
                 abs_tol=1e-4)


def test_color_attr():
    assert Color('red').hue == Hue(0)
    assert Color('red').lightness == Lightness(0.5)
    assert Color('red').saturation == Saturation(1)
    assert Color('red').luma == Luma(0.299)


def test_color_diff():
    assert Color('black').difference(Color('black')) == 0.0
    assert Color('white').difference(Color('black')) == sqrt(3)
    assert Color('red').difference(Color('black')) == 1.0
    assert Color('black').difference(Color('black'), 'cie1976') == 0.0
    assert Color('black').difference(Color('black'), 'ciede2000') == 0.0
    with pytest.raises(ValueError):
        Color('red').difference(Color('black'), method='foo')
    with pytest.raises(ValueError):
        Color('red').difference(Color('black'), method=b'foo')


def test_color_format():
    black = Color('black')
    red = Color('red')
    blue = Color('#004')
    with pytest.warns(DeprecationWarning):
        assert '{:0}'.format(black) == '\x1b[0m'
    assert '{}{}{}'.format(black, red, blue) == '\x1b[22;30m\x1b[1;31m\x1b[22;34m'
    assert '{:b}{:b8}{:b8}'.format(black, red, blue) == '\x1b[40m\x1b[41m\x1b[44m'
    assert '{0:256}{0:b256}'.format(black) == '\x1b[38;5;0m\x1b[48;5;0m'
    assert '{0:256}{0:b256}'.format(red) == '\x1b[38;5;9m\x1b[48;5;9m'
    assert '{0:256}{0:b256}'.format(blue) == '\x1b[38;5;17m\x1b[48;5;17m'
    assert '{0:16m}{0:b16m}'.format(black) == '\x1b[38;2;0;0;0m\x1b[48;2;0;0;0m'
    assert '{0:16m}{0:b16m}'.format(red) == '\x1b[38;2;255;0;0m\x1b[48;2;255;0;0m'
    assert '{0:16m}{0:b16m}'.format(blue) == '\x1b[38;2;0;0;68m\x1b[48;2;0;0;68m'
    assert '{0:html}{1:html}'.format(red, blue) == '#ff0000#000044'
    assert '{0:css}'.format(red) == 'rgb(255, 0, 0)'
    assert '{0:cssrgb}'.format(blue) == 'rgb(0, 0, 68)'
    assert '{0:csshsl}'.format(blue) == 'hsl(240deg, 100%, 13.3333%)'
    with pytest.raises(ValueError):
        '{:foo}'.format(black)


def test_color_gradient():
    black = Color('black')
    white = Color('white')
    red = Color('red')
    assert list(black.gradient(white, 2)) == [black, white]
    assert list(black.gradient(white, 5)) == [
        black,
        Color(0.25, 0.25, 0.25),
        Color(0.5, 0.5, 0.5),
        Color(0.75, 0.75, 0.75),
        white,
    ]
    assert list(white.gradient(red, 5)) == [
        white,
        Color(1, 0.75, 0.75),
        Color(1, 0.5, 0.5),
        Color(1, 0.25, 0.25),
        red,
    ]
    with pytest.raises(ValueError):
        list(black.gradient(white, 1))


def test_default_repr():
    assert repr(Default) == '<Color Default>'


def test_default_formats():
    assert '{}'.format(Default) == '\x1b[0m'
    assert '{:f}'.format(Default) == '\x1b[39m'
    assert '{:b8}'.format(Default) == '\x1b[49m'
    assert '{:css}'.format(Default) == 'inherit'
    assert '{:html}'.format(Default) == ''
    with pytest.raises(ValueError):
        '{:foo}'.format(Default)
