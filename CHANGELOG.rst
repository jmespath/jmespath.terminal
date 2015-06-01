0.2.0
=====

* Backwards incompatible: Ctrl-p has been changed to now
  be an output mode toggle.  The output mode tells jpterm
  what to print (if anything) when it exits.  You can now
  no longer save and print multiple expressions.
* You can now exit jpterm using ctrl-c in addition to
  F5.  This fixes issues for people that were unable to
  use F5 previously.

0.1.0
=====

* Add support for reading the input JSON document from stdin.
  This also changes the -i option to a positional argument.
* Rename main executable from jmespath-term to jpterm.
