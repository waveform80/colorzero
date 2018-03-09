# vim: set et sw=4 sts=4 fileencoding=utf-8:
#
# The colorzero color library
# Copyright (c) 2016-2018 Dave Jones <dave@waveform.org.uk>
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the
#       names of its contributors may be used to endorse or promote products
#       derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"Tests for the colorzero.conversions module"

from __future__ import (
    unicode_literals,
    print_function,
    division,
    absolute_import,
)

try:
    from math import isclose
except ImportError:
    from compat import isclose

# pylint: disable=wrong-import-order,import-error,missing-docstring
import pytest
from colorzero import conversions as cv


def frange(start, stop, step):
    i = 0
    while True:
        value = start + (i * step)
        if value > stop:
            break
        yield value
        i += 1

def verify_floats(color1, color2, abs_tol=1e-7):
    for elem1, elem2 in zip(color1, color2):
        assert isclose(elem1, elem2, abs_tol=abs_tol)


def verify_ints(color1, color2, abs_tol=1):
    for elem1, elem2 in zip(color1, color2):
        assert abs(elem1 - elem2) <= abs_tol


# Stop pylint warning about pytest fixtures
# pylint: disable=redefined-outer-name
@pytest.fixture(params=(
    (r, g, b)
    for r in frange(0.0, 1.0, 0.2)
    for g in frange(0.0, 1.0, 0.2)
    for b in frange(0.0, 1.0, 0.2)
))
def rgb(request):
    return request.param


@pytest.fixture(params=(
    (r, g, b)
    for r in range(0, 255, 64)
    for g in range(0, 255, 64)
    for b in range(0, 255, 64)
))
def rgb_bytes(request):
    return request.param


@pytest.fixture()
def html7(request, rgb_bytes):
    # pylint: disable=unused-argument
    return '#%02x%02x%02x' % rgb_bytes


@pytest.fixture(params=(
    (r, g, b)
    for r in range(0, 0xf, 0x4)
    for g in range(0, 0xf, 0x4)
    for b in range(0, 0xf, 0x4)
))
def html3(request):
    return '#%x%x%x' % request.param


def test_yiq_roundtrip(rgb):
    verify_floats(cv.yiq_to_rgb(*cv.rgb_to_yiq(*rgb)), rgb)


def test_yiq_knowns():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, yiq
        ((0.0, 0.0, 0.0), (0.0,   0.0,     0.0)),     # black
        ((0.0, 0.0, 1.0), (0.11, -0.3217,  0.3121)),  # blue
        ((0.0, 1.0, 0.0), (0.59, -0.2773, -0.5251)),  # green
        ((0.0, 1.0, 1.0), (0.7,  -0.599,  -0.213)),   # cyan
        ((1.0, 0.0, 0.0), (0.3,   0.599,   0.213)),   # red
        ((1.0, 0.0, 1.0), (0.41,  0.2773,  0.5251)),  # purple
        ((1.0, 1.0, 0.0), (0.89,  0.3217, -0.3121)),  # yellow
        ((1.0, 1.0, 1.0), (1.0,   0.0,     0.0)),     # white
        ((0.5, 0.5, 0.5), (0.5,   0.0,     0.0)),     # grey
    ]
    for rgb, yiq in values:
        verify_floats(cv.rgb_to_yiq(*rgb), yiq)
        verify_floats(cv.yiq_to_rgb(*yiq), rgb)


def test_hls_roundtrip(rgb):
    verify_floats(cv.hls_to_rgb(*cv.rgb_to_hls(*rgb)), rgb)


def test_hls_knowns(rgb):
    # pylint: disable=bad-whitespace
    values = [
        # rgb, hls
        ((0.0, 0.0, 0.0), (  0, 0.0, 0.0)),  # black
        ((0.0, 0.0, 1.0), (4/6, 0.5, 1.0)),  # blue
        ((0.0, 1.0, 0.0), (2/6, 0.5, 1.0)),  # green
        ((0.0, 1.0, 1.0), (3/6, 0.5, 1.0)),  # cyan
        ((1.0, 0.0, 0.0), (  0, 0.5, 1.0)),  # red
        ((1.0, 0.0, 1.0), (5/6, 0.5, 1.0)),  # purple
        ((1.0, 1.0, 0.0), (1/6, 0.5, 1.0)),  # yellow
        ((1.0, 1.0, 1.0), (  0, 1.0, 0.0)),  # white
        ((0.5, 0.5, 0.5), (  0, 0.5, 0.0)),  # grey
    ]
    for rgb, hls in values:
        verify_floats(cv.rgb_to_hls(*rgb), hls)
        verify_floats(cv.hls_to_rgb(*hls), rgb)


def test_hsv_roundtrip(rgb):
    verify_floats(cv.hsv_to_rgb(*cv.rgb_to_hsv(*rgb)), rgb)


def test_hsv_knowns():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, hsv
        ((0.0, 0.0, 0.0), (  0, 0.0, 0.0)),  # black
        ((0.0, 0.0, 1.0), (4/6, 1.0, 1.0)),  # blue
        ((0.0, 1.0, 0.0), (2/6, 1.0, 1.0)),  # green
        ((0.0, 1.0, 1.0), (3/6, 1.0, 1.0)),  # cyan
        ((1.0, 0.0, 0.0), (  0, 1.0, 1.0)),  # red
        ((1.0, 0.0, 1.0), (5/6, 1.0, 1.0)),  # purple
        ((1.0, 1.0, 0.0), (1/6, 1.0, 1.0)),  # yellow
        ((1.0, 1.0, 1.0), (  0, 0.0, 1.0)),  # white
        ((0.5, 0.5, 0.5), (  0, 0.0, 0.5)),  # grey
    ]
    for rgb, hsv in values:
        verify_floats(cv.rgb_to_hsv(*rgb), hsv)
        verify_floats(cv.hsv_to_rgb(*hsv), rgb)


def test_rgb_bytes_roundtrip(rgb):
    verify_floats(cv.rgb_bytes_to_rgb(*cv.rgb_to_rgb_bytes(*rgb)), rgb)


def test_rgb_bytes_known():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, bytes
        ((0.0, 0.0, 0.0), (0,   0,   0)),    # black
        ((0.0, 0.0, 1.0), (0,   0,   255)),  # blue
        ((0.0, 1.0, 0.0), (0,   255, 0)),    # green
        ((0.0, 1.0, 1.0), (0,   255, 255)),  # cyan
        ((1.0, 0.0, 0.0), (255, 0,   0)),    # red
        ((1.0, 0.0, 1.0), (255, 0,   255)),  # purple
        ((1.0, 1.0, 0.0), (255, 255, 0)),    # yellow
        ((1.0, 1.0, 1.0), (255, 255, 255)),  # white
        ((0.4, 0.4, 0.4), (102, 102, 102)),  # grey
    ]
    for rgb, b in values:
        assert cv.rgb_to_rgb_bytes(*rgb) == b
        assert cv.rgb_bytes_to_rgb(*b) == rgb


def test_rgb24_roundtrip(rgb_bytes):
    assert cv.rgb24_to_rgb_bytes(cv.rgb_bytes_to_rgb24(*rgb_bytes)) == rgb_bytes


def test_rgb24_known():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, rgb24
        ((0,   0,   0),   0),         # black
        ((0,   0,   255), 0xff0000),  # blue
        ((0,   255, 0),   0xff00),    # green
        ((0,   255, 255), 0xffff00),  # cyan
        ((255, 0,   0),   0xff),      # red
        ((255, 0,   255), 0xff00ff),  # purple
        ((255, 255, 0),   0xffff),    # yellow
        ((255, 255, 255), 0xffffff),  # white
        ((102, 102, 102), 0x666666),  # grey
    ]
    for rgb, rgb24 in values:
        assert cv.rgb24_to_rgb_bytes(rgb24) == rgb
        assert cv.rgb_bytes_to_rgb24(*rgb) == rgb24


def test_rgb_html7_roundtrip(html7):
    assert cv.rgb_bytes_to_html(*cv.html_to_rgb_bytes(html7)) == html7


def test_rgb_html3_roundtrip(html3):
    v = '#' + html3[1] + html3[1] + html3[2] + html3[2] + html3[3] + html3[3]
    assert cv.rgb_bytes_to_html(*cv.html_to_rgb_bytes(html3)) == v


def test_html_known():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, html
        ((0,   0,   0),   '#000000'),  # black
        ((0,   0,   255), '#0000ff'),  # blue
        ((0,   255, 0),   '#00ff00'),  # green
        ((0,   255, 255), '#00ffff'),  # cyan
        ((255, 0,   0),   '#ff0000'),  # red
        ((255, 0,   255), '#ff00ff'),  # purple
        ((255, 255, 0),   '#ffff00'),  # yellow
        ((255, 255, 255), '#ffffff'),  # white
        ((102, 102, 102), '#666666'),  # grey
    ]
    for rgb, rgb24 in values:
        assert cv.html_to_rgb_bytes(rgb24) == rgb
        assert cv.rgb_bytes_to_html(*rgb) == rgb24


def test_cmy_roundtrip(rgb):
    verify_floats(cv.cmy_to_rgb(*cv.rgb_to_cmy(*rgb)), rgb)


def test_cmy_known():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, cmy
        ((0.0, 0.0, 0.0), (1.0, 1.0, 1.0)),  # black
        ((0.0, 0.0, 1.0), (1.0, 1.0, 0.0)),  # blue
        ((0.0, 1.0, 0.0), (1.0, 0.0, 1.0)),  # green
        ((0.0, 1.0, 1.0), (1.0, 0.0, 0.0)),  # cyan
        ((1.0, 0.0, 0.0), (0.0, 1.0, 1.0)),  # red
        ((1.0, 0.0, 1.0), (0.0, 1.0, 0.0)),  # purple
        ((1.0, 1.0, 0.0), (0.0, 0.0, 1.0)),  # yellow
        ((1.0, 1.0, 1.0), (0.0, 0.0, 0.0)),  # white
        ((0.5, 0.5, 0.5), (0.5, 0.5, 0.5)),  # grey
    ]
    for rgb, cmy in values:
        verify_floats(cv.rgb_to_cmy(*rgb), cmy)
        verify_floats(cv.cmy_to_rgb(*cmy), rgb)


def test_cmyk_roundtrip(rgb):
    verify_floats(
        cv.cmy_to_rgb(
            *cv.cmyk_to_cmy(
                *cv.cmy_to_cmyk(
                    *cv.rgb_to_cmy(*rgb)))), rgb)


def test_cmyk_known():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, cmyk
        ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0, 1.0)),  # black
        ((0.0, 0.0, 1.0), (1.0, 1.0, 0.0, 0.0)),  # blue
        ((0.0, 1.0, 0.0), (1.0, 0.0, 1.0, 0.0)),  # green
        ((0.0, 1.0, 1.0), (1.0, 0.0, 0.0, 0.0)),  # cyan
        ((1.0, 0.0, 0.0), (0.0, 1.0, 1.0, 0.0)),  # red
        ((1.0, 0.0, 1.0), (0.0, 1.0, 0.0, 0.0)),  # purple
        ((1.0, 1.0, 0.0), (0.0, 0.0, 1.0, 0.0)),  # yellow
        ((1.0, 1.0, 1.0), (0.0, 0.0, 0.0, 0.0)),  # white
        ((0.5, 0.5, 0.5), (0.0, 0.0, 0.0, 0.5)),  # grey
    ]
    for rgb, cmyk in values:
        verify_floats(cv.cmy_to_cmyk(*cv.rgb_to_cmy(*rgb)), cmyk)
        verify_floats(cv.cmy_to_rgb(*cv.cmyk_to_cmy(*cmyk)), rgb)


def test_yuv_roundtrip(rgb):
    verify_floats(cv.yuv_to_rgb(*cv.rgb_to_yuv(*rgb)), rgb)


def test_yuv_knowns():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, yuv
        ((0.0, 0.0, 0.0), (0.0,    0.0,      0.0)),      # black
        ((0.0, 0.0, 1.0), (0.114,  0.436,   -0.10001)),  # blue
        ((0.0, 1.0, 0.0), (0.587, -0.28886, -0.51498)),  # green
        ((0.0, 1.0, 1.0), (0.701,  0.14714, -0.615)),    # cyan
        ((1.0, 0.0, 0.0), (0.299, -0.14714,  0.615)),    # red
        ((1.0, 0.0, 1.0), (0.413,  0.28886,  0.51498)),  # purple
        ((1.0, 1.0, 0.0), (0.886, -0.436,    0.10001)),  # yellow
        ((1.0, 1.0, 1.0), (1.0,    0.0,      0.0)),      # white
        ((0.5, 0.5, 0.5), (0.5,    0.0,      0.0)),      # grey
    ]
    for rgb, yuv in values:
        verify_floats(cv.rgb_to_yuv(*rgb), yuv, abs_tol=1e-5)
        verify_floats(cv.yuv_to_rgb(*yuv), rgb, abs_tol=1e-5)


def test_yuv_bytes_roundtrip(rgb_bytes):
    # Tolerance of 2 here to allow for accumulated error in the roundtrip
    verify_ints(
        cv.yuv_bytes_to_rgb_bytes(*cv.rgb_bytes_to_yuv_bytes(*rgb_bytes)),
        rgb_bytes, abs_tol=2)


def test_yuv_bytes_knowns():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, yuv
        ((0,   0,   0),   (16,  128, 128)),  # black
        ((0,   0,   255), (41,  240, 110)),  # blue
        ((0,   255, 0),   (144, 54,  34)),   # green
        ((0,   255, 255), (169, 166, 16)),   # cyan
        ((255, 0,   0),   (82,  90,  240)),  # red
        ((255, 0,   255), (107, 202, 222)),  # purple
        ((255, 255, 0),   (210, 16,  146)),  # yellow
        ((255, 255, 255), (235, 128, 128)),  # white
        ((102, 102, 102), (104, 128, 128)),  # grey
    ]
    for rgb, yuv in values:
        verify_ints(cv.rgb_bytes_to_yuv_bytes(*rgb), yuv)
        verify_ints(cv.yuv_bytes_to_rgb_bytes(*yuv), rgb)


def test_yuv_coefficients():
    with pytest.raises(TypeError):
        cv.YUVCoefficients()


def test_xyz_roundtrip(rgb):
    # XYZ is a more complex conversion and tends to lose more precision during
    # the round-trip
    verify_floats(cv.xyz_to_rgb(*cv.rgb_to_xyz(*rgb)), rgb, abs_tol=1e-5)


def test_xyz_known():
    # pylint: disable=bad-whitespace
    values = [
        # rgb, xyz
        ((0.0, 0.0, 0.0), (0.0,    0.0,      0.0)),      # black
        ((0.0, 0.0, 1.0), (0.18043, 0.07217, 0.95030)),  # blue
        ((0.0, 1.0, 0.0), (0.35758, 0.71515, 0.11919)),  # green
        ((0.0, 1.0, 1.0), (0.53801, 0.78733, 1.06950)),  # cyan
        ((1.0, 0.0, 0.0), (0.41246, 0.21267, 0.01933)),  # red
        ((1.0, 0.0, 1.0), (0.59289, 0.28485, 0.96964)),  # purple
        ((1.0, 1.0, 0.0), (0.77003, 0.92782, 0.13852)),  # yellow
        ((1.0, 1.0, 1.0), (0.95047, 1.00000, 1.08883)),  # white
        ((0.5, 0.5, 0.5), (0.20344, 0.21404, 0.23305)),  # grey
    ]
    for rgb, xyz in values:
        verify_floats(cv.rgb_to_xyz(*rgb), xyz, abs_tol=1e-5)
        # The XYZ values above are very rough approximations, hence the huge
        # tolerance here
        verify_floats(cv.xyz_to_rgb(*xyz), rgb, abs_tol=1e-3)


def test_lab_roundtrip(rgb):
    verify_floats(
        cv.xyz_to_rgb(
            *cv.lab_to_xyz(
                *cv.xyz_to_lab(
                    *cv.rgb_to_xyz(*rgb)))), rgb, abs_tol=1e-5)


def test_luv_roundtrip(rgb):
    verify_floats(
        cv.xyz_to_rgb(
            *cv.luv_to_xyz(
                *cv.xyz_to_luv(
                    *cv.rgb_to_xyz(*rgb)))), rgb, abs_tol=1e-5)


def test_bad_html():
    with pytest.raises(ValueError):
        cv.html_to_rgb_bytes('foo')
    with pytest.raises(ValueError):
        cv.html_to_rgb_bytes('#foo')


def test_bad_name():
    with pytest.raises(ValueError):
        cv.name_to_html('foo')
