History
=======

1.3.3 (2017-02-16)
------------------

* Fixes a bug that would cause invalid product types to be accepted on 
  ``article/front/article-meta/product/@product-type``.
* Fixes a bug that would cause invalid invalid values to be accepted on 
  ``article/front/article-meta/aff/institution/@content-type``.
* Clean up unused attributes from classes from the ``packtools.style_error`` 
  module. 
* Log messages are now omitted from the stderr by default. 
* Fixes a bug that would cause tests to fail on Python 3.6
  [https://github.com/scieloorg/packtools/issues/107].


1.3.2 (2016-11-22)
------------------

* Bugfix release
  [https://github.com/scieloorg/packtools/issues/101].


1.3.1 (2016-10-03)
------------------

* Bugfix release 
  [https://github.com/scieloorg/packtools/commit/36a0277e].


1.3 (2016-09-30)
----------------

* Added functions ``stylechecker.summarize`` and ``stylechecker.annotate``.
* Added zip-file validation capabilities.
* Initial support for SciELO PS 1.5.


1.2 (2016-04-04)
----------------

* Fixes a bug that would cause ``country`` elements to be mandatory on 
  sub-articles of type ``transation``. 
* HTMLGenerator().generate() method now handling undefined 
  ``article/@xml:lang`` attribute.


1.1 (2016-03-11)
----------------

* Initial support for SciELO PS 1.4.


1.0 (2016-02-23)
----------------

* Better debug information with ``stylechecker --sysinfo`` option.
* Added scripts to handle registration of local xml catalog in the super catalog.
* New domain specific exceptions.
* The module ``packtools.xray`` was removed.
* Added support for automatic generation of HTML documents through 
  ``HTMLGenerator``.
* Backwards incompatible change in ``XMLValidator`` init method signature.


0.8.1 (2015-09-03)
------------------

* Fixe some issues that would cause invalid sps-1.3 XMLs to be considered valid.


0.8.0 (2015-08-31)
------------------

* Minor refactoring to make possible for the XMLValidator to handle deprecated 
  versions of SciELO PS.
* Added basic support to SciELO PS 1.3.


0.7.6 (2015-07-08)
------------------

* Fixed bug that would cause empty mandatory elements to be valid.


0.7.5 (2015-07-03)
------------------

* Added feature to run the validation against an external schematron schema 
  [#55].
* stylechecker's ``--loglevel`` option accepts upper, lower or mixed case strings.
* stylechecker utility can read from stdin, so it can be a filter in unix 
  pipelines.
* Added ``--raw`` option to stylechecker. 
* Fixed bug that would raise UnicodeDecodeError in the presence 
  of any non-ascii character in the path to the file (Python 2 on Windows only).


0.7.4 (2015-06-19)
------------------

* Fixed bug that would cause page counts to be reported as error when 
  pagination is identified with elocation-id [#51].
* Added support for creative commons IGO licenses (sps-1.2 only). 
* Fixed bug that would cause funding-group validation to raise false positives.


0.7.3 (2015-05-18)
------------------

* Validating the minimum set of elements required for references of type 
  journal [http://git.io/vUSp6].
* Added validation of //aff/country/@country attributes for XMLs under 
  sps-1.2 spec.


0.7.2 (2015-04-30)
------------------

* Fixes a bug in which the occurrence of empty award-id, 
  fn[@fn-type="financial-disclosure"] or ack could lead stylechecker to crash.


0.7.1 (2015-04-29)
------------------

* Fixes a bug that report *page-count* as invalid when fpage or lpage values 
  are non-digit.
* Fixes a bug that mark as invalid XMLs containing use-licenses with 
  https scheme or missing trailing slashes.
* Changes the funding-group validation algorithm. 
* Checking for funding-statement when fn[fn-type="financial-disclosure"] is 
  present.


0.7 (2015-03-13)
----------------

* Added SciELO PS 1.2 support.
* Added the apparent sourceline of the element raising validation errors 
  (stylechecker).
* Added the option *--nocolors* to prevent stylechecker output from being 
  colorized by ANSI escape sequences.
* stylechecker now prints log messages to stdout. The option *--loglevel* 
  should be used to define the log level. Options are: DEBUG, INFO, WARNING, 
  ERROR or CRITICAL.
* SciELO PS 1.2 schematron uses EXSLT querybinding.
* Better error handling while analyzing multiple XML files with stylechecker.


0.6.4 (2015-02-03)
------------------

* Fixes a bug that causes malfunctioning on stylechecker
  while expanding wildcards on windows.
* Major semantic changes at *--assetsdir* options. Now it is always turned ON,
  and the option is used to set the lookup basedir. By default,
  the XML basedir is used.


0.6.3 (2015-02-02)
------------------

* stylechecker CLI utility overhaul:
  * The basic output is now presented as JSON structure. 
  * The option *--assetsdir* lookups, in the given dir, for each asset referenced in
      XML. The *--annotated* option now writes the output to a file. The
      utility now takes more than one XML a time.
  * *pygments*, if installed, will be used to display pretty JSON outputs.


0.6.2 (2015-01-23)
------------------

* Added method ``XMLValidator.lookup_assets``.
* Added property ``XMLValidator.assets``. 
* Fixed minor issue that would cause //element-citation[@publication-type="report"] 
  to be reported as invalid.
* Fixed minor issue that would erroneously identify an element-citation element 
  as not being child of element ref.


0.6.1 (2014-11-28)
------------------

* Minor fix to implement changes from SciELO PS 1.1.1.


0.6 (2014-10-28)
----------------

* Python 3 support.
* Project-wide code refactoring.
* ``packtools.__version__`` attribute to get the package version.
* Distinction between classes of error with the attribute ``StyleError.level``.


0.5 (2014-09-29)
----------------

* Basic implementation of XML style rules according to SciELO PS version 1.1.
* ``stylechecker`` and ``packbuilder`` console utilities.
* Major performance improvements on ``XMLValidator`` instantiation, when used
  with long-running processes (9.5x).

