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

  $ pip install jmespath-term

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


To quit the program, press ``F5``.
You can also clear the current expression by specifying
``Ctrl + ]``.

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
