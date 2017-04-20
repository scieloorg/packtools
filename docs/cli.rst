.. _cli:

Command-line tools
==================

stylechecker
------------

The stylechecker utility performs structural validations on XML documents 
according to the `SciELO PS specification <https://docs.scielo.org/projects/scielo-publishing-schema/>`_.

Usage::

    stylechecker [-h] [--annotated | --raw] [--nonetwork]
                 [--assetsdir ASSETSDIR] [--version] [--loglevel LOGLEVEL]
                 [--nocolors] [--extrasch EXTRASCH] [--sysinfo]
                 [file [file ...]]


The stylechecker utility validates the contents of *file* or, by default, its
standard input, and prints the validation report, encoded in JSON format, 
to the standard output.

The options are as follows::

    -h, --help            show this help message and exit
    --annotated           reproduces the XML with notes at elements that have
                          errors
    --raw                 each result is encoded as json, without any
                          formatting, and written to stdout in a single line.
    --nonetwork           prevents the retrieval of the DTD through the network
    --assetsdir ASSETSDIR
                          lookup, at the given directory, for each asset
                          referenced by the XML. current working directory will
                          be used by default.
    --version             show program's version number and exit
    --loglevel LOGLEVEL
    --nocolors            prevents the output from being colorized by ANSI
                          escape sequences
    --extrasch EXTRASCH   runs an extra validation using an external schematron
                          schema. built-in schemas are available through the
                          prefix `@`: @scielo-br, @sps-1.1, @sps-1.2, @sps-1.3,
                          @sps-1.4, @sps-1.5.
    --sysinfo             show program's installation info and exit.


Exit status: The stylechecker utility exits 0 on success, and >0 if an error 
occurs.
