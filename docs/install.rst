.. _install:

============
Installation
============

.. currentmodule:: lightwave


.. _raspbian_install:

Raspbian installation
=====================

On `Raspbian`_, it is best to obtain Lightwave via the ``apt-get`` utility:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install python-lightwave python3-lightwave

The usual apt upgrade method can be used to keep your installation up to date:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get upgrade

To remove your installation:

.. code-block:: console

    $ sudo apt-get remove python-lightwave python3-lightwave


.. _ubuntu_install:

Ubuntu installation
===================

If you are using `Ubuntu`_, it is probably easiest to obtain Lightwave from the
author's PPA:

.. code-block:: console

    $ sudo add-apt-repository ppa://waveform/ppa
    $ sudo apt-get update
    $ sudo apt-get install python-lightwave python3-lightwave

The usual apt upgrade method can be used to keep your installation up to date:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get upgrade

To remove your installation:

.. code-block:: console

    $ sudo apt-get remove python-lightwave python3-lightwave


.. _other_install:

Other platforms
===============

On other platforms, it is probably easiest to obtain Lightwave via the ``pip``
utility:

.. code-block:: console

    $ sudo pip install lightwave
    $ sudo pip3 install lightwave

To upgrade your installation:

.. code-block:: console

    $ sudo pip install -U lightwave
    $ sudo pip3 install -U lightwave

To remove your installation:

.. code-block:: console

    $ sudo pip remove lightwave
    $ sudo pip3 remove lightwave


.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/
.. _Ubuntu: https://ubuntu.com/
