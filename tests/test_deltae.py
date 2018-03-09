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

"Tests for the colorzero.deltae module"

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
from colorzero import Lab, deltae as de


def test_cie1976_known():
    # XXX Test values from current implementation; if anyone can point me at
    # a source of "known" test values for CIE1976 I'd be most grateful!
    # pylint: disable=bad-whitespace
    values = [
        # color1, color2, delta-e (graphics), delta-e (textiles)
        (Lab(50.0000,   2.6772, -79.7751), Lab(50.0000,   0.0000, -82.7485),  4.0011),
        (Lab(50.0000,   3.1571, -77.2803), Lab(50.0000,   0.0000, -82.7485),  6.3142),
        (Lab(50.0000,   2.8361, -74.0200), Lab(50.0000,   0.0000, -82.7485),  9.1777),
        (Lab(50.0000,  -1.3802, -84.2814), Lab(50.0000,   0.0000, -82.7485),  2.0627),
        (Lab(50.0000,  -1.1848, -84.8006), Lab(50.0000,   0.0000, -82.7485),  2.3696),
        (Lab(50.0000,  -0.9009, -85.5211), Lab(50.0000,   0.0000, -82.7485),  2.9153),
        (Lab(50.0000,   0.0000,   0.0000), Lab(50.0000,  -1.0000,   2.0000),  2.2361),
        (Lab(50.0000,  -1.0000,   2.0000), Lab(50.0000,   0.0000,   0.0000),  2.2361),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0009),  4.9800),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0010),  4.9800),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0011),  4.9800),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0012),  4.9800),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0009,  -2.4900),  4.9800),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0010,  -2.4900),  4.9800),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0011,  -2.4900),  4.9800),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   0.0000,  -2.5000),  3.5355),
        (Lab(50.0000,   2.5000,   0.0000), Lab(73.0000,  25.0000, -18.0000), 36.8680),
        (Lab(50.0000,   2.5000,   0.0000), Lab(61.0000,  -5.0000,  29.0000), 31.9100),
        (Lab(50.0000,   2.5000,   0.0000), Lab(56.0000, -27.0000,  -3.0000), 30.2531),
        (Lab(50.0000,   2.5000,   0.0000), Lab(58.0000,  24.0000,  15.0000), 27.4089),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.1736,   0.5854),  0.8924),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.2972,   0.0000),  0.7972),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   1.8634,   0.5757),  0.8583),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.2592,   0.3350),  0.8298),
        (Lab(60.2574, -34.0099,  36.2677), Lab(60.4626, -34.1751,  39.4387),  3.1819),
        (Lab(63.0109, -31.0961,  -5.8663), Lab(62.8187, -29.7946,  -4.0864),  2.2133),
        (Lab(61.2901,   3.7196,  -5.3901), Lab(61.4292,   2.2480,  -4.9620),  1.5389),
        (Lab(35.0831, -44.1164,   3.7933), Lab(35.0232, -40.0716,   1.5901),  4.6063),
        (Lab(22.7233,  20.0904, -46.6940), Lab(23.0331,  14.9730, -42.5619),  6.5847),
        (Lab(36.4612,  47.8580,  18.3852), Lab(36.2715,  50.5065,  21.2231),  3.8864),
        (Lab(90.8027,  -2.0831,   1.4410), Lab(91.1528,  -1.6435,   0.0447),  1.5051),
        (Lab(90.9257,  -0.5406,  -0.9208), Lab(88.6381,  -0.8985,  -0.7239),  2.3238),
        (Lab( 6.7747,  -0.2908,  -2.4247), Lab( 5.8714,  -0.0985,  -2.2286),  0.9441),
        (Lab( 2.0776,   0.0795,  -1.1350), Lab( 0.9033,  -0.0636,  -0.5514),  1.3191),
    ]
    for color1, color2, diff in values:
        assert isclose(de.cie1976(color1, color2), diff, abs_tol=1e-4)


def test_cie1994_known():
    # XXX Test values from current implementation; if anyone can point me at
    # a source of "known" test values for CIE1994 I'd be most grateful!
    # pylint: disable=bad-whitespace
    values = [
        # color1, color2, delta-e (graphics), delta-e (textiles)
        (Lab(50.0000,   2.6772, -79.7751), Lab(50.0000,   0.0000, -82.7485),  1.3950,  1.4230),
        (Lab(50.0000,   3.1571, -77.2803), Lab(50.0000,   0.0000, -82.7485),  1.9341,  1.9427),
        (Lab(50.0000,   2.8361, -74.0200), Lab(50.0000,   0.0000, -82.7485),  2.4543,  2.4066),
        (Lab(50.0000,  -1.3802, -84.2814), Lab(50.0000,   0.0000, -82.7485),  0.6845,  0.6980),
        (Lab(50.0000,  -1.1848, -84.8006), Lab(50.0000,   0.0000, -82.7485),  0.6696,  0.6719),
        (Lab(50.0000,  -0.9009, -85.5211), Lab(50.0000,   0.0000, -82.7485),  0.6919,  0.6772),
        (Lab(50.0000,   0.0000,   0.0000), Lab(50.0000,  -1.0000,   2.0000),  2.2361,  2.2361),
        (Lab(50.0000,  -1.0000,   2.0000), Lab(50.0000,   0.0000,   0.0000),  2.0316,  2.0193),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0009),  4.8007,  4.8122),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0010),  4.8007,  4.8122),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0011),  4.8007,  4.8122),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0012),  4.8007,  4.8122),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0009,  -2.4900),  4.8007,  4.8122),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0010,  -2.4900),  4.8007,  4.8122),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0011,  -2.4900),  4.8007,  4.8122),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   0.0000,  -2.5000),  3.4077,  3.4160),
        (Lab(50.0000,   2.5000,   0.0000), Lab(73.0000,  25.0000, -18.0000), 34.6892, 28.2503),
        (Lab(50.0000,   2.5000,   0.0000), Lab(61.0000,  -5.0000,  29.0000), 29.4414, 27.7308),
        (Lab(50.0000,   2.5000,   0.0000), Lab(56.0000, -27.0000,  -3.0000), 27.9141, 27.3286),
        (Lab(50.0000,   2.5000,   0.0000), Lab(58.0000,  24.0000,  15.0000), 24.9377, 23.8076),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.1736,   0.5854),  0.8221,  0.8194),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.2972,   0.0000),  0.7166,  0.7118),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   1.8634,   0.5757),  0.8049,  0.8041),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.2592,   0.3350),  0.7528,  0.7488),
        (Lab(60.2574, -34.0099,  36.2677), Lab(60.4626, -34.1751,  39.4387),  1.3910,  1.3897),
        (Lab(63.0109, -31.0961,  -5.8663), Lab(62.8187, -29.7946,  -4.0864),  1.2481,  1.2441),
        (Lab(61.2901,   3.7196,  -5.3901), Lab(61.4292,   2.2480,  -4.9620),  1.2980,  1.2884),
        (Lab(35.0831, -44.1164,   3.7933), Lab(35.0232, -40.0716,   1.5901),  1.8205,  1.7958),
        (Lab(22.7233,  20.0904, -46.6940), Lab(23.0331,  14.9730, -42.5619),  2.5561,  2.5310),
        (Lab(36.4612,  47.8580,  18.3852), Lab(36.2715,  50.5065,  21.2231),  1.4249,  1.3991),
        (Lab(90.8027,  -2.0831,   1.4410), Lab(91.1528,  -1.6435,   0.0447),  1.4195,  1.3858),
        (Lab(90.9257,  -0.5406,  -0.9208), Lab(88.6381,  -0.8985,  -0.7239),  2.3226,  1.2123),
        (Lab( 6.7747,  -0.2908,  -2.4247), Lab( 5.8714,  -0.0985,  -2.2286),  0.9385,  0.5182),
        (Lab( 2.0776,   0.0795,  -1.1350), Lab( 0.9033,  -0.0636,  -0.5514),  1.3065,  0.8191),
    ]
    for color1, color2, diffg, difft in values:
        assert isclose(de.cie1994g(color1, color2), diffg, abs_tol=1e-4)
        assert isclose(de.cie1994t(color1, color2), difft, abs_tol=1e-4)


def test_ciede2000_known():
    # Test values from Sharma 2005:
    # http://www.ece.rochester.edu/~gsharma/ciede2000/ciede2000noteCRNA.pdf
    # pylint: disable=bad-whitespace
    values = [
        # color1, color2, delta-e
        (Lab(50.0000,   2.6772, -79.7751), Lab(50.0000,   0.0000, -82.7485),  2.0425),
        (Lab(50.0000,   3.1571, -77.2803), Lab(50.0000,   0.0000, -82.7485),  2.8615),
        (Lab(50.0000,   2.8361, -74.0200), Lab(50.0000,   0.0000, -82.7485),  3.4412),
        (Lab(50.0000,  -1.3802, -84.2814), Lab(50.0000,   0.0000, -82.7485),  1.0000),
        (Lab(50.0000,  -1.1848, -84.8006), Lab(50.0000,   0.0000, -82.7485),  1.0000),
        (Lab(50.0000,  -0.9009, -85.5211), Lab(50.0000,   0.0000, -82.7485),  1.0000),
        (Lab(50.0000,   0.0000,   0.0000), Lab(50.0000,  -1.0000,   2.0000),  2.3669),
        (Lab(50.0000,  -1.0000,   2.0000), Lab(50.0000,   0.0000,   0.0000),  2.3669),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0009),  7.1792),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0010),  7.1792),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0011),  7.2195),
        (Lab(50.0000,   2.4900,  -0.0010), Lab(50.0000,  -2.4900,   0.0012),  7.2195),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0009,  -2.4900),  4.8045),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0010,  -2.4900),  4.8045),
        (Lab(50.0000,  -0.0010,   2.4900), Lab(50.0000,   0.0011,  -2.4900),  4.7461),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   0.0000,  -2.5000),  4.3065),
        (Lab(50.0000,   2.5000,   0.0000), Lab(73.0000,  25.0000, -18.0000), 27.1492),
        (Lab(50.0000,   2.5000,   0.0000), Lab(61.0000,  -5.0000,  29.0000), 22.8977),
        (Lab(50.0000,   2.5000,   0.0000), Lab(56.0000, -27.0000,  -3.0000), 31.9030),
        (Lab(50.0000,   2.5000,   0.0000), Lab(58.0000,  24.0000,  15.0000), 19.4535),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.1736,   0.5854),  1.0000),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.2972,   0.0000),  1.0000),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   1.8634,   0.5757),  1.0000),
        (Lab(50.0000,   2.5000,   0.0000), Lab(50.0000,   3.2592,   0.3350),  1.0000),
        (Lab(60.2574, -34.0099,  36.2677), Lab(60.4626, -34.1751,  39.4387),  1.2644),
        (Lab(63.0109, -31.0961,  -5.8663), Lab(62.8187, -29.7946,  -4.0864),  1.2630),
        (Lab(61.2901,   3.7196,  -5.3901), Lab(61.4292,   2.2480,  -4.9620),  1.8731),
        (Lab(35.0831, -44.1164,   3.7933), Lab(35.0232, -40.0716,   1.5901),  1.8645),
        (Lab(22.7233,  20.0904, -46.6940), Lab(23.0331,  14.9730, -42.5619),  2.0373),
        (Lab(36.4612,  47.8580,  18.3852), Lab(36.2715,  50.5065,  21.2231),  1.4146),
        (Lab(90.8027,  -2.0831,   1.4410), Lab(91.1528,  -1.6435,   0.0447),  1.4441),
        (Lab(90.9257,  -0.5406,  -0.9208), Lab(88.6381,  -0.8985,  -0.7239),  1.5381),
        (Lab( 6.7747,  -0.2908,  -2.4247), Lab( 5.8714,  -0.0985,  -2.2286),  0.6377),
        (Lab( 2.0776,   0.0795,  -1.1350), Lab( 0.9033,  -0.0636,  -0.5514),  0.9082),
    ]
    for color1, color2, diff in values:
        assert isclose(de.ciede2000(color1, color2), diff, abs_tol=1e-4)
