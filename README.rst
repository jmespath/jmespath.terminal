=================
JMESPath Terminal
=================

JMESPath, in your terminal!  To use, you can install
via pip::

  $ pip install jmespath-term

Then run up the ``jpterm`` program::

  $ jpterm

You can also specify an initial JSON document to use
by specifying the JSON file as a positional argument::

  $ jpterm /tmp/somejsondoc.json

To quit the program, press ``F5``.
You can also clear the current expression by specifying
``Ctrl + ]``.

If you like to work on jmespath-terminal to add new features,
you can first create and activate a new virtual environment::

    $ virtualenv venv
    $ . venv/bin/activate

Then install the module::

    $ pip install -e .

You'll now be able to modify the ``jpterm.py`` module and see
your changes reflected when you run the ``jpterm`` command.

Beta Status
===========

Until jmespath-terminal reaches version 1.0, some of the command line options
and semantics may change.  There will be a CHANGELOG.rst that will outline any
changes that occur for each new version.
