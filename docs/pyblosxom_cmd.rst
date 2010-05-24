=============================
PyBlosxom on the command line
=============================

PyBlosxom comes with a command line tool called ``pyblosxom-cmd``.  It allows
you to create new blogs, verify your configuration, run static rendering, 
render single urls, and run command line functions implemented in plugins.

For help, do::

    pyblosxom-cmd --help

It'll list the commands and options available.

If you tell it where your config file is, then it'll list commands and
options available as well as those implemented in plugins you have installed.

For example::

    pyblosxom-cmd --config=/path/to/config.py --help

For more information on static rendering, see :ref:`static-rendering`.
