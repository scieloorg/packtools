<?xml version="1.0" encoding="utf-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        queryBinding="xslt"
        xml:lang="en">
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
     - PMC-Style compatibility is maintained[2]
  
   Always double-check the JPTS and PMC-Style before editing.
   [1] http://jats.nlm.nih.gov/publishing/tag-library/1.0/
   [2] https://www.ncbi.nlm.nih.gov/pmc/pmcdoc/tagging-guidelines/article/tags.html
  *******************************************************************************
  </p>

  <!--
   Phases - sets of patterns.
   These are being used to help on tests isolation.
  -->
  <phase id="phase.journal-id">
    <active pattern="journal-id_type_nlm-ta_or_publisher-id"/>
  </phase>

  <phase id="phase.journal-title-group">
    <active pattern="has_journal-title_and_abbrev-journal-title"/>
  </phase>

  <phase id="phase.publisher">
    <active pattern="publisher"/>
  </phase>

  <phase id="phase.article-categories">
    <active pattern="article_categories"/>
  </phase>

  <phase id="phase.fpage_or_elocation-id">
    <active pattern="fpage_or_elocation_id"/>
  </phase>

  <phase id="phase.issn">
    <active pattern="issn_pub_type_epub_or_ppub"/>
  </phase>

  <phase id="phase.article-id">
    <active pattern="has_article_id_type_doi_and_valid_values"/>
  </phase>

  <phase id="phase.subj-group">
    <active pattern="subj_group"/>
  </phase>

  <phase id="phase.abstract_lang">
    <active pattern="abstract"/>
  </phase>

  <phase id="phase.article-title_lang">
    <active pattern="article-title"/>
  </phase>

  <phase id="phase.aff_contenttypes">
    <active pattern="aff_contenttypes"/>
    <active pattern="aff_contenttypes_contribgroup"/>
  </phase>

  <phase id="phase.kwd-group_lang">
      <active pattern="kwdgroup_lang"/>
  </phase>

  <phase id="phase.counts">
      <active pattern="counts"/>
  </phase>


  <!--
   Patterns - sets of rules.
  -->
  <pattern id="journal-id_type_nlm-ta_or_publisher-id">
    <rule context="article/front/journal-meta">
      <assert test="journal-id[@journal-id-type='nlm-ta'] or journal-id[@journal-id-type='publisher-id']">
        Element 'journal-meta': Missing element journal-id with journal-id-type=("nlm-ta" or "publisher-id").
      </assert>
    </rule>
  </pattern>

  <pattern id="has_journal-title_and_abbrev-journal-title">
    <rule context="article/front/journal-meta">
      <assert test="journal-title-group">
        Element 'journal-meta': Missing element journal-title-group.
      </assert>
    </rule>

    <rule context="article/front/journal-meta/journal-title-group">
      <assert test="journal-title">
        Element 'journal-title-group': Missing element journal-title.
      </assert>
      <assert test="abbrev-journal-title[@abbrev-type='publisher']">
        Element 'journal-title-group': Missing element abbrev-journal-title with abbrev-type="publisher".
      </assert>
    </rule>
  </pattern>

  <pattern id="publisher">
    <rule context="article/front/journal-meta">
      <assert test="publisher">
        Element 'journal-meta': Missing element publisher.
      </assert>
    </rule>
  </pattern>

  <pattern id="article_categories">
    <rule context="article/front/article-meta">
      <assert test="article-categories">
        Element 'article-meta': Missing element article-categories.
      </assert>
    </rule>
  </pattern>

  <pattern id="fpage_or_elocation_id">
    <rule context="article/front/article-meta">
      <assert test="fpage or elocation-id">
        Element 'article-meta': Missing elements fpage or elocation-id.
      </assert>
    </rule>
  </pattern>

  <pattern id="issn_pub_type_epub_or_ppub">
    <rule context="article/front/journal-meta">
      <assert test="issn[@pub-type='epub'] or issn[@pub-type='ppub']">
        Element 'journal-meta': Missing element issn with pub-type=("epub" or "ppub").
      </assert>
    </rule>
  </pattern>

  <pattern id="has_article_id_type_doi_and_valid_values">
    <rule context="article/front/article-meta">
      <assert test="article-id">
        Element 'article-meta': Missing element article-id.
      </assert>
      <assert test="article-id[@pub-id-type='doi']">
        Element 'article-meta': Missing element article-id with pub-id-type="doi".
      </assert>
    </rule>

    <rule context="article/front/article-meta/article-id">
      <assert test="@pub-id-type='art-access-id' or
                    @pub-id-type='arxiv' or 
                    @pub-id-type='doaj' or 
                    @pub-id-type='doi' or 
                    @pub-id-type='isbn' or 
                    @pub-id-type='pmcid' or 
                    @pub-id-type='pmid' or 
                    @pub-id-type='publisher-id' or 
                    @pub-id-type='publisher-manuscript' or 
                    @pub-id-type='sici' or 
                    @pub-id-type='other'">
        Element 'article-id', attribute pub-id-type: Invalid value "<value-of select="@pub-id-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="subj_group">
    <rule context="article/front/article-meta/article-categories">
      <assert test="//subj-group[@subj-group-type='heading']">
        Element 'article-categories': Missing element subj-group with subj-group-type="heading".
      </assert>
      <assert test="count(//subj-group[@subj-group-type='heading']) = 1">
        Element 'article-categories': Many elements subj-group with subj-group-type="heading".
      </assert>
    </rule>
  </pattern>

  <pattern id="abstract">
    <rule context="article/front/article-meta">
      <assert test="abstract">
        Element 'article-meta': Missing element abstract.
      </assert>
    </rule>
    <rule context="article/front/article-meta/abstract">
      <assert test="not(@xml:lang)">
        Element 'abstract': Unexpected attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="article-title">
    <rule context="article/front/article-meta/title-group/article-title">
      <assert test="not(@xml:lang)">
        Element 'article-title': Unexpected attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern abstract="true" id="aff_contenttypes_base">
    <rule context="$base_context/aff/institution">
      <assert test="@content-type='original' or 
                    @content-type='orgname' or
                    @content-type='orgdiv1' or
                    @content-type='orgdiv2' or
                    @content-type='orgdiv3'">
        Element '<name/>', attribute content-type: Invalid value "<value-of select="@content-type"/>". 
      </assert>
    </rule>
    <rule context="$base_context/aff">
      <assert test="count(institution[@content-type='original']) = 1">
        Element '<name/>': Must have exactly one element institution with content-type="original".
      </assert>
    </rule>
  </pattern>

  <pattern is-a="aff_contenttypes_base" id="aff_contenttypes">
    <param name="base_context" value="article/front/article-meta"/>
  </pattern>

  <pattern is-a="aff_contenttypes_base" id="aff_contenttypes_contribgroup">
    <param name="base_context" value="article/front/article-meta/contrib-group"/>
  </pattern>

  <pattern id="kwdgroup_lang">
    <title>
      Make sure all kwd-group elements have xml:lang attribute.
    </title>

    <rule context="article/front/article-meta/kwd-group">
      <assert test="@xml:lang">
        Element 'kwd-group': Missing attribute xml:lang.
      </assert>  
    </rule>
  </pattern>

  <pattern id="counts">
    <title>
      Make sure the total number of tables, figures, equations and pages are present.
    </title>

    <rule context="article">
      <assert test="front/article-meta/counts/table-count/@count = count(//table)">
        Element 'counts': Missing element or wrong value in table-count.
      </assert>
      <assert test="front/article-meta/counts/ref-count/@count = count(//ref)">
        Element 'counts': Missing element or wrong value in ref-count.
      </assert>
      <assert test="front/article-meta/counts/fig-count/@count = count(//fig)">
        Element 'counts': Missing element or wrong value in fig-count.
      </assert>
      <assert test="front/article-meta/counts/equation-count/@count = count(//disp-formula)">
        Element 'counts': Missing element or wrong value in equation-count.
      </assert>
      <assert test="front/article-meta/counts/page-count/@count = front/article-meta/lpage - front/article-meta/fpage">
        Element 'counts': Missing element or wrong value in page-count.
      </assert>
    </rule>
  </pattern>

</schema>

