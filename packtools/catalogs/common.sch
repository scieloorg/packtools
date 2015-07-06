<?xml version="1.0" encoding="utf-8"?>
<!--
Copyright 2013 SciELO <scielo-dev@googlegroups.com>.
Licensed under the terms of the BSD license. Please see LICENSE in the source
code for more information.
-->

<pattern id="assert-not-empty" abstract="true" 
         xmlns="http://purl.oclc.org/dsdl/schematron">
  <title>
    Check if the element's text is at least one character long.
  </title>
  
  <rule context="$base_context">
    <assert test="string-length(normalize-space($assert_expr)) != 0">
      Element '<name/>': <value-of select="$err_message"/>
    </assert>
  </rule>
</pattern>

