<?xml version="1.0" encoding="utf-8"?>
<!--
Copyright 2016 SciELO <scielo-dev@googlegroups.com>.
Licensed under the terms of the BSD license. Please see LICENSE in the source
code for more information.
-->
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        queryBinding="exslt"
        xml:lang="en">
  <ns uri="http://www.w3.org/1999/xlink" prefix="xlink"/>
  <ns uri="http://exslt.org/regular-expressions" prefix="regexp"/>

  <p>
  *******************************************************************************
   THINGS TO BE SURE BEFORE EDITING THIS FILE!

   The spec used is ISO-Schematron. 
   
   Some useful info:
     - The query language used is the extended version of XPath specified in XSLT.
     - The rule context is interpreted according to the Production 1 of XSLT. 
       The rule context may be the root node, elements, attributes, comments and 
       processing instructions. 
     - The assertion test is interpreted according to Production 14 of XPath, as 
       returning a Boolean value.

   For more info, refer to the official ISO/IEC 19757-3:2006(E) standard.
  
   The implementation of the schematron patterns comes with the idea of SPS as a
   set of constraints on top of JATS' Publishing Tag Set v1.0 (JPTS)[1]. To keep
   consistency, please make sure:
  
     - DTD/XSD constraints are not duplicated here
     - There is an issue at http://git.io/5EcR4Q with status `Aprovada`
     - PMC-Style compatibility is desired[2]
  
   Always double-check the JPTS and PMC-Style before editing.
   [1] http://jats.nlm.nih.gov/publishing/tag-library/1.0/
   [2] https://www.ncbi.nlm.nih.gov/pmc/pmcdoc/tagging-guidelines/article/tags.html
  *******************************************************************************
  </p>

  <!--
   Phases - sets of patterns.
   These are being used to help on tests isolation.
  -->
  <phase id="phase.article-id">
    <active pattern="article-id_attributes"/>
  </phase>

  <phase id="phase.article-type-values">
    <active pattern="article_article-type-values"/>
  </phase>

  <phase id="phase.history">
    <active pattern="history"/>
  </phase>


  <!--
   Patterns - sets of rules.
  -->
  <pattern id="article-id_attributes">
    <title>
      Mandatory attributes are present.
    </title>

    <rule context="article/front/article-meta">
      <assert test="article-id[@pub-id-type='doi']">
        Element 'article-meta': Missing element article-id with pub-id-type="doi".
      </assert>
    </rule>
  </pattern>

  <pattern id="article_article-type-values">
    <title>
      Allowed values for article/@article-type
    </title>

    <rule context="article[@article-type]">
        <assert test="@article-type = 'addendum' or
            @article-type = 'research-article' or
            @article-type = 'review-article' or
            @article-type = 'letter' or
            @article-type = 'article-commentary' or
            @article-type = 'brief-report' or
            @article-type = 'rapid-communication' or
            @article-type = 'oration' or
            @article-type = 'discussion' or
            @article-type = 'editorial' or
            @article-type = 'interview' or
            @article-type = 'correction' or
            @article-type = 'guidelines' or
            @article-type = 'other' or
            @article-type = 'obituary' or
            @article-type = 'case-report' or
            @article-type = 'book-review' or
            @article-type = 'reply' or
            @article-type = 'retraction' or
            @article-type = 'partial-retraction' or
            @article-type = 'clinical-trial'">
        Element 'article', attribute article-type: Invalid value '<value-of select="@article-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="history">
    <title>
      Ensure elements day, month and year are present.
    </title>

    <rule context="article/front/article-meta/history/date">
      <assert test="string-length(day) > 0">
        Element 'date', Missing element day.
      </assert>
      <assert test="string-length(month) > 0">
        Element 'date', Missing element month.
      </assert>
      <assert test="string-length(year) > 0">
        Element 'date', Missing element year.
      </assert>
    </rule>
  </pattern>

</schema>

