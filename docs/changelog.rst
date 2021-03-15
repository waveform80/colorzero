==========
Change log
==========

.. currentmodule:: colorzero


Release 2.0 (2021-03-15)
========================

* Dropped Python 2.x support. Current Python support level is 3.5 and above.

* No other major changes within the library (all other changes have been to
  make packaging a bit easier, and update doc builds and CI integration to
  current practices)


Release 1.1 (2018-05-15)
========================

* Added ability to generate ANSI codes with :ref:`format`.

* Added :meth:`Color.gradient` method.

* Exposed the various difference functions in the API (:func:`euclid`,
  :func:`cie1976`, etc).

* Various doc fixes and enhancements.


Release 1.0 (2018-03-10)
========================

1.0 is the first release after breaking the library out of the `picamera`_
project. As this is a 1.x release, API stability will be maintained.


.. _picamera: https://github.com/waveform80/picamera
