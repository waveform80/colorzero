.. _install:

============
Installation
============

.. currentmodule:: colorzero


.. _raspbian_install:

Raspbian installation
=====================

On `Raspbian`_, it is best to obtain colorzero via the ``apt-get`` utility:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install python-colorzero python3-colorzero

The usual apt upgrade method can be used to keep your installation up to date:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get upgrade

To remove your installation:

.. code-block:: console

    $ sudo apt-get remove python-colorzero python3-colorzero


.. _ubuntu_install:

Ubuntu installation
===================

If you are using `Ubuntu`_, it is probably easiest to obtain colorzero from the
author's PPA:

.. code-block:: console

    $ sudo add-apt-repository ppa://waveform/ppa
    $ sudo apt-get update
    $ sudo apt-get install python-colorzero python3-colorzero

The usual apt upgrade method can be used to keep your installation up to date:

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get upgrade

To remove your installation:

.. code-block:: console

    $ sudo apt-get remove python-colorzero python3-colorzero


.. _other_install:

Other platforms
===============

On other platforms, it is probably easiest to obtain colorzero via the ``pip``
utility:

.. code-block:: console

    $ sudo pip install colorzero
    $ sudo pip3 install colorzero

To upgrade your installation:

.. code-block:: console

    $ sudo pip install -U colorzero
    $ sudo pip3 install -U colorzero

To remove your installation:

.. code-block:: console

    $ sudo pip remove colorzero
    $ sudo pip3 remove colorzero


.. _Raspbian: https://www.raspberrypi.org/downloads/raspbian/
.. _Ubuntu: https://ubuntu.com/
