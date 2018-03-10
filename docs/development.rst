===========
Development
===========

.. currentmodule:: colorzero

The main GitHub repository for the project can be found at:

    https://github.com/waveform80/colorzero

Anyone is more than welcome to open tickets to discuss bugs, new features, or
just to ask usage questions (I find this useful for gauging what questions
ought to feature in the FAQ, for example).

Even if you don’t feel up to hacking on the code, I’d love to hear suggestions
from people of what you’d like the API to look like (even if the code itself
isn’t particularly pythonic, the interface should be)!


.. _dev_install:

Development installation
========================

If you wish to develop colorzero itself, it is easiest to obtain the source by
cloning the GitHub repository and then use the "develop" target of the Makefile
which will install the package as a link to the cloned repository allowing
in-place development (it also builds a tags file for use with vim/emacs with
Exuberant’s ctags utility). The following example demonstrates this method
within a virtual Python environment:

.. code-block:: console

    $ sudo apt install lsb-release build-essential git git-core \
        exuberant-ctags virtualenvwrapper python-virtualenv python3-virtualenv
    $ cd
    $ mkvirtualenv -p /usr/bin/python3 colorzero
    $ workon colorzero
    (colorzero) $ git clone https://github.com/waveform80/colorzero.git
    (colorzero) $ cd colorzero
    (colorzero) $ make develop

To pull the latest changes from git into your clone and update your
installation:

.. code-block:: console

    $ workon colorzero
    (colorzero) $ cd ~/colorzero
    (colorzero) $ git pull
    (colorzero) $ make develop

To remove your installation, destroy the sandbox and the clone:

.. code-block:: console

    (colorzero) $ deactivate
    $ rmvirtualenv colorzero
    $ rm -fr ~/colorzero


Building the docs
=================

If you wish to build the docs, you'll need a few more dependencies. Inkscape
is used for conversion of SVGs to other formats, Graphviz is used for rendering
certain charts, and TeX Live is required for building PDF output. The following
command should install all required dependencies:

.. code-block:: console

    $ sudo apt install texlive-latex-recommended texlive-latex-extra \
        texlive-fonts-recommended graphviz inkscape

Once these are installed, you can use the "doc" target to build the
documentation:

.. code-block:: console

    $ workon colorzero
    (colorzero) $ cd ~/colorzero
    (colorzero) $ make doc

The HTML output is written to :file:`build/html` while the PDF output goes to
:file:`build/latex`.


Test suite
==========

If you wish to run the colorzero test suite, follow the instructions in
:ref:`dev_install` above and then make the "test" target within the sandbox:

.. code-block:: console

    $ workon colorzero
    (colorzero) $ cd ~/colorzero
    (colorzero) $ make test
