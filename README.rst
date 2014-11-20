=================
JMESPath Terminal
=================

JMESPath, in your terminal!  To use, you can install
via pip::

  $ pip install jmespath-term

Then run up the jmespath-term program::

  $ jmespath-term

You can also specify an initial JSON document to use::

  $ jmespath-term -i /tmp/somejsondoc.json

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
your changes reflected when you run the ``jmespath-term`` command.
