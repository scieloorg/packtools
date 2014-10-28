History
=======

0.6 (2014-10-28)
----------------

* Python 3 support.
* Project-wide code refactoring.
* `packtools.__version__` attribute to get the package version.
* Distinction between classes of error with the attribute `StyleError.level`.


0.5 (2014-09-29)
----------------

* Basic implementation of XML style rules according to SciELO PS version 1.1.
* `stylechecker` and `packbuilder` console utilities.
* Major performance improvements on `XMLValidator` instantiation, when used
  with long-running processes (9.5x).

