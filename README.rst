=================
JMESPath Terminal
=================

JMESPath, in your terminal!

.. image:: https://cloud.githubusercontent.com/assets/368057/5158769/6546e58a-72fe-11e4-8ceb-ba866777983e.gif


Overview
========

JMESPath is an expression language for manipulating JSON documents.  If you've
never heard of JMESPath before, you write a JMESPath expression that when
applied to an input JSON document will produces an output JSON document based
on the expression you've provided.

You can check out the `JMESPath site
<http://jmespath.org>`__ for more information.

One of the best ways to learn the JMESPath language is to experiment
by creating your own JMESPath expressions.  The JMESPath Terminal
makes it easy to see the results of your JMESPath expressions immediately
as you type.


Getting Started
===============

You can install the JMESPath Terminal via pip::

  $ pip install jmespath-terminal

There will then be a ``jpterm`` program you can run::

  $ jpterm

With no arguments specified, a sample JSON document is used as
input.

You can also specify an initial JSON document to use
by specifying the JSON file as a positional argument::

  $ jpterm /tmp/somejsondoc.json

You can also pipe an input JSON document into the
``jpterm`` command:

.. image:: https://cloud.githubusercontent.com/assets/368057/5158770/6a6afb6e-72fe-11e4-8be3-893edf21920e.gif

Keyboard Shortcuts
__________________
``F5``
    | Quit the program.
``Ctrl + p``
    | Save the current expression so that it is output on quit.
    | (Multiple expressions can be saved and each is output on its own line.
``Ctrl + ]``
    | Clear the current expression.

Mouse Clicks
____________
NOTE: These features are dependent on terminal support. (The Terminal.app
included in Mac OS X does not support this, but `iTerm2 <http://iterm2.com/>`_
does.)

One feature of the Urwid Python package (which jmespath-terminal is built on)
is that mouse clicks are recognized. This allows you to click to switch focus
on either the Input or Result window (and of course back to the Expression) and
scroll it.

This can make it difficult to select text for copying/pasting. Many Linux
terminals will allow you to select the text with a ``Shift + click/drag`` and
copy it with ``Shift + Ctrl + c``. In iTerm2 selections can be made with
``Opt/Alt + click/drag``.

Working on JMESPath Terminal
============================

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
