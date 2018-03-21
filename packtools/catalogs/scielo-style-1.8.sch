<?xml version="1.0" encoding="utf-8"?>
<!--
Copyright 2017 SciELO <scielo-dev@googlegroups.com>.
Licensed under the terms of the BSD license. Please see LICENSE in the source
code for more information.
-->
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        queryBinding="exslt"
        xml:lang="en">
  <ns uri="http://www.w3.org/1999/xlink" prefix="xlink"/>
  <ns uri="http://exslt.org/regular-expressions" prefix="regexp"/>

  <include href="common.sch"/>
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
  <phase id="phase.journal-id">
    <active pattern="journal-id_notempty"/>
    <active pattern="journal-id_has_publisher-id"/>
    <active pattern="journal-id_values"/>
  </phase>

  <phase id="phase.journal-title-group">
    <active pattern="has_journal-title_and_abbrev-journal-title"/>
    <active pattern="journal-title_notempty"/>
    <active pattern="abbrev-journal-title_notempty"/>
  </phase>

  <phase id="phase.publisher">
    <active pattern="publisher"/>
    <active pattern="publisher_notempty"/>
  </phase>

  <phase id="phase.article-categories">
    <active pattern="article_categories"/>
  </phase>

  <phase id="phase.fpage_or_elocation-id">
    <active pattern="fpage_or_elocation-id"/>
    <active pattern="fpage_notempty"/>
    <active pattern="elocation-id_notempty"/>
  </phase>

  <phase id="phase.issn">
    <active pattern="issn_pub_type_epub_or_ppub"/>
    <active pattern="issn_notempty"/>
  </phase>

  <phase id="phase.article-id">
    <active pattern="article-id_notempty"/>
    <active pattern="article-id_attributes"/>
    <active pattern="article-id_values"/>
  </phase>

  <phase id="phase.subj-group">
    <active pattern="subj_group"/>
    <active pattern="subj_group_subarticle_pt"/>
    <active pattern="subj_group_subarticle_es"/>
    <active pattern="subj_group_subarticle_en"/>
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
      <active pattern="counts_tables"/>
      <active pattern="counts_refs"/>
      <active pattern="counts_figs"/>
      <active pattern="counts_equations"/>
      <active pattern="counts_pages"/>
  </phase>

  <phase id="phase.pub-date">
    <active pattern="pub-date_pub_type"/>
  </phase>

  <phase id="phase.volume">
    <active pattern="volume_notempty"/>
  </phase>
  
  <phase id="phase.issue">
    <active pattern="issue_notempty"/>
    <active pattern="issue_cardinality"/>
  </phase>

  <phase id="phase.supplement">
    <active pattern="supplement"/>
  </phase>

  <phase id="phase.elocation-id">
    <active pattern="elocation-id"/>
  </phase>

  <phase id="phase.history">
    <active pattern="history"/>
  </phase>

  <phase id="phase.product">
    <active pattern="product"/>
    <active pattern="product_product-type_values"/>
  </phase>

  <phase id="phase.sectitle">
    <active pattern="sectitle"/>
  </phase>

  <phase id="phase.paragraph">
    <active pattern="paragraph"/>
  </phase>

  <phase id="phase.rid_integrity">
    <active pattern="xref-reftype-integrity-aff"/>
  </phase>

  <phase id="phase.caption">
    <active pattern="caption_title"/>
  </phase>

  <phase id="phase.license">
    <active pattern="license_attributes"/>
    <active pattern="license"/>
  </phase>

  <phase id="phase.ack">
    <active pattern="ack"/>
  </phase>

  <phase id="phase.element-citation">
    <active pattern="element-citation"/>
    <active pattern="element-citation_attributes"/>
    <active pattern="element-citation_publication-type-values"/>
  </phase>

  <phase id="phase.person-group">
    <active pattern="person-group"/>
    <active pattern="person-group-type_values"/>
  </phase>

  <phase id="phase.fn-group">
    <active pattern="fn"/>
    <active pattern="fn-group"/>
    <active pattern="fn_attributes"/>
  </phase>

  <phase id="phase.xhtml-table">
    <active pattern="xhtml-table"/>
  </phase>

  <phase id="phase.supplementary-material">
    <active pattern="supplementary-material_mimetype"/>
  </phase>

  <phase id="phase.xref_reftype_integrity">
    <active pattern="xref-reftype-values"/>
  </phase>

  <phase id="phase.article-attrs">
    <active pattern="article_attributes"/>
    <active pattern="article_article-type-values"/>
    <active pattern="article_specific-use-values"/>
  </phase>

  <phase id="phase.named-content_attrs">
    <active pattern="named-content_attributes"/>
    <active pattern="named-content_content-type-values"/>
  </phase>

  <phase id="phase.month">
    <active pattern="month"/>
    <active pattern="month_cardinality"/>
  </phase>

  <phase id="phase.size">
    <active pattern="size_attributes"/>
    <active pattern="size_units-values"/>
    <active pattern="size_cardinality"/>
  </phase>

  <phase id="phase.list">
    <active pattern="list_attributes"/>
    <active pattern="list_list-type-values"/>
  </phase>

  <phase id="phase.media_attributes">
    <active pattern="media_attributes"/>
  </phase>

  <phase id="phase.ext-link">
    <active pattern="ext-link_href_values"/>
    <active pattern="ext-link_attributes"/>
  </phase>

  <phase id="phase.sub-article-attrs">
    <active pattern="sub-article_attributes"/>
    <active pattern="sub-article_article-type-values"/>
  </phase>

  <phase id="phase.response-attrs">
    <active pattern="response_attributes"/>
    <active pattern="response_response-type-values"/>
  </phase>

  <phase id="phase.response-reply-type">
    <active pattern="response_related-article_attributes"/>
  </phase>

  <phase id="phase.related-article-attrs">
    <active pattern="related-article_attributes"/>
    <active pattern="related-article-type-values"/>
    <active pattern="related-article_ext-link-type-values"/>
    <active pattern="related-article_correction_attributes"/>
  </phase>

  <phase id="phase.correction">
    <active pattern="correction_related-article"/>
    <active pattern="correction_article-type"/>
  </phase>

  <phase id="phase.in-brief">
    <active pattern="inbrief_related-article"/>
    <active pattern="inbrief_article-type"/>
  </phase>

  <phase id="phase.funding-group">
    <active pattern="funding-group"/>
    <active pattern="funding-group_elements"/>
  </phase>

  <phase id="phase.aff_country">
    <active pattern="aff_country-attrs"/>
    <active pattern="aff_country"/>
  </phase>

  <phase id="phase.ref">
    <active pattern="ref"/>
    <active pattern="ref_notempty"/>
    <active pattern="element-citation_cardinality"/>
  </phase>

  <phase id="phase.contrib-id">
    <active pattern="contrib-id_attributes"/>
    <active pattern="contrib-id-type-values"/>
  </phase>

  <phase id="phase.source">
    <active pattern="source_cardinality"/>
  </phase>

  <phase id="phase.chapter-title">
    <active pattern="chapter-title_cardinality"/>
  </phase>

  <!--
   Patterns - sets of rules.
  -->
  <pattern id="journal-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/journal-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="journal-id_has_publisher-id">
    <title>
      There exists one journal-id[@journal-id-type='publisher-id'].
    </title>

    <rule context="article/front/journal-meta">
      <assert test="journal-id[@journal-id-type='publisher-id']">
        Element 'journal-meta': Missing element journal-id with journal-id-type="publisher-id".
      </assert>
    </rule>
  </pattern>

  <pattern id="journal-id_values">
    <rule context="article/front/journal-meta/journal-id[@journal-id-type]">
      <assert test="@journal-id-type = 'nlm-ta' or
                    @journal-id-type = 'publisher-id'">
        Element 'journal-id', attribute journal-id-type: Invalid value "<value-of select="@journal-id-type"/>".
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

  <pattern id="journal-title_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/journal-title-group/journal-title"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="abbrev-journal-title_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/journal-title-group/abbrev-journal-title"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="publisher">
    <rule context="article/front/journal-meta">
      <assert test="publisher">
        Element 'journal-meta': Missing element publisher.
      </assert>
    </rule>
  </pattern>

  <pattern id="publisher_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/publisher/publisher-name"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="article_categories">
    <rule context="article/front/article-meta">
      <assert test="article-categories">
        Element 'article-meta': Missing element article-categories.
      </assert>
    </rule>
  </pattern>

  <pattern id="fpage_or_elocation-id">
    <rule context="article/front/article-meta">
      <assert test="fpage or elocation-id">
        Element 'article-meta': Missing elements fpage or elocation-id.
      </assert>
    </rule>
  </pattern>

  <pattern id="fpage_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/fpage"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="elocation-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/elocation-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="issn_pub_type_epub_or_ppub">
    <rule context="article/front/journal-meta">
      <assert test="issn[@pub-type='epub'] or issn[@pub-type='ppub']">
        Element 'journal-meta': Missing element issn with pub-type=("epub" or "ppub").
      </assert>
    </rule>
  </pattern>

  <pattern id="issn_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/journal-meta/issn"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="article-id_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/article-id"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="article-id_attributes">
    <title>
      Mandatory attributes are present.
    </title>
    <rule context="article/front/article-meta">
      <assert test="article-id[@pub-id-type]">
        Element 'article-meta': Missing element article-id.
      </assert>
    </rule>
  </pattern>

  <pattern id="article-id_values">
    <title>
      Values are known.
    </title>
    <rule context="article/front/article-meta/article-id[@pub-id-type]">
      <assert test="@pub-id-type = 'doi' or 
                    @pub-id-type = 'other' or 
                    @pub-id-type = 'publisher-id'">
        Element 'article-id', attribute pub-id-type: Invalid value "<value-of select="@pub-id-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern abstract="true" id="subj_group_base">
    <title>
      Make sure only one heading is provided per language, in subj-group.
    </title>

    <rule context="$base_context">
      <assert test="count(subj-group[@subj-group-type='heading'] | subj-group//subj-group[@subj-group-type='heading']) = 1">
        Element '<name/>': There must be only one element subj-group with subj-group-type="heading".
      </assert>
    </rule>
  </pattern>

  <pattern is-a="subj_group_base" id="subj_group">
    <param name="base_context" value="article/front/article-meta/article-categories"/>
  </pattern>

  <pattern is-a="subj_group_base" id="subj_group_subarticle_pt">
    <param name="base_context" value="article/sub-article[@xml:lang='pt']/front-stub/article-categories"/>
  </pattern>
  <pattern is-a="subj_group_base" id="subj_group_subarticle_es">
    <param name="base_context" value="article/sub-article[@xml:lang='es']/front-stub/article-categories"/>
  </pattern>
  <pattern is-a="subj_group_base" id="subj_group_subarticle_en">
    <param name="base_context" value="article/sub-article[@xml:lang='en']/front-stub/article-categories"/>
  </pattern>
  <pattern is-a="subj_group_base" id="subj_group_subarticle_fr">
    <param name="base_context" value="article/sub-article[@xml:lang='fr']/front-stub/article-categories"/>
  </pattern>

  <pattern id="abstract">
    <rule context="article[@article-type='research-article'] | article[@article-type='review-article']">
      <assert test="count(front/article-meta/abstract | front/article-meta/trans-abstract) > 0">
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
    <rule context="article/front/article-meta/title-group/article-title | 
                   article/back/ref-list/ref/element-citation/article-title">
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
                    @content-type='normalized'">
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

  <pattern id="counts_tables">
    <title>
      Make sure the total number of tables are correct.
    </title>

    <rule context="article/front/article-meta/counts/table-count">
      <assert test="@count = count(//table-wrap)">
        Element 'table-count': Wrong value in table-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_refs">
    <title>
      Make sure the total number of refs are correct.
    </title>

    <rule context="article/front/article-meta/counts/ref-count">
      <assert test="@count = count(//ref)">
        Element 'ref-count': Wrong value in ref-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_figs">
    <title>
      Make sure the total number of figures are correct.
    </title>

    <rule context="article/front/article-meta/counts/fig-count">
      <assert test="@count = count(//fig)">
        Element 'fig-count': Wrong value in fig-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_equations">
    <title>
      Make sure the total number of equations are correct.
    </title>

    <rule context="article/front/article-meta/counts/equation-count">
      <assert test="@count = count(//disp-formula)">
        Element 'equation-count': Wrong value in equation-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="counts_pages">
    <title>
      Make sure the total number of pages are correct.
    </title>

    <rule context="article/front/article-meta/counts/page-count">
      <assert test="(/article/front/article-meta/lpage = 0 and
                     /article/front/article-meta/fpage = 0 and
                     @count = 0) or 
                     (regexp:test(/article/front/article-meta/fpage, '\D', 'i') or
                      regexp:test(/article/front/article-meta/lpage, '\D', 'i')) or
                     string-length(/article/front/article-meta/elocation-id) > 0 or
                     (@count = ((/article/front/article-meta/lpage - /article/front/article-meta/fpage) + 1))">
        Element 'page-count': Wrong value in page-count.
      </assert>
    </rule>
  </pattern>

  <pattern id="pub-date_pub_type">
    <title>
      Restrict the valid values of pub-date[@pub-type].
    </title>

    <rule context="article/front/article-meta/pub-date">
      <assert test="@pub-type = 'epub' or
                    @pub-type = 'epub-ppub' or
                    @pub-type = 'collection'">
        Element 'pub-date', attribute pub-type: Invalid value "<value-of select="@pub-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="volume_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/volume"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="issue_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/front/article-meta/issue"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="supplement">
    <title>
      Make sure the supplement is not present.
    </title>

    <rule context="article/front/article-meta">
      <assert test="not(supplement)">
        Element 'article-meta': Unexpected element supplement.
      </assert>
    </rule>
  </pattern>

  <pattern id="elocation-id">
    <title>
      Allow elocation-id to be present only when fpage is absent.
    </title>

    <rule context="article/front/article-meta/elocation-id | article/back/ref-list/ref/element-citation/elocation-id">
      <assert test="not(following-sibling::fpage)">
        Element 'article-meta': Unexpected element elocation-id.
      </assert>
    </rule>
  </pattern>

  <pattern id="history">
    <title>
      Restrict the valid values of history/date/[@date-type].
    </title>

    <rule context="article/front/article-meta/history/date">
      <assert test="@date-type = 'received' or 
                    @date-type = 'accepted' or
                    @date-type = 'corrected' or
                    @date-type = 'pub' or
                    @date-type = 'preprint' or
                    @date-type = 'retracted' or
                    @date-type = 'rev-request' or
                    @date-type = 'rev-recd'">
        Element 'date', attribute date-type: Invalid value "<value-of select="@date-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="product">
    <title>
      Allow product to be present only when article-type is book-review or product-review.
      Also, make sure product[@product-type='book'].
    </title>

    <rule context="article/front/article-meta/product">
      <assert test="/article[@article-type='book-review']">
        Element 'article-meta': Unexpected element product.
      </assert>
      <assert test="@product-type">
        Element 'product': Missing attribute product-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="product_product-type_values">
    <title>
      Make sure the supplied values are valid.
    </title>

    <rule context="article/front/article-meta/product[@product-type]">
      <assert test="@product-type = 'book' or
                    @product-type = 'article' or
                    @product-type = 'issue' or
                    @product-type = 'website' or
                    @product-type = 'film' or
                    @product-type = 'software' or
                    @product-type = 'hardware' or
                    @product-type = 'other'">
        Element 'product', attribute product-type: Invalid value "<value-of select="@product-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="sectitle">
    <title>
      Make sure all sections have a title element.
    </title>

    <rule context="article/body/sec">
      <assert test="string-length(title) > 0">
        Element 'sec': Missing element title.
      </assert>
    </rule>
  </pattern>

  <pattern id="paragraph">
    <title>
      Make sure paragraphs have no id attr.
    </title>

    <rule context="//p">
      <assert test="not(@id)">
        Element 'p': Unexpected attribute id.
      </assert>
    </rule>
  </pattern>

  <!-- start-block: xref @ref-type integrity -->
  <pattern abstract="true" id="xref-reftype-integrity-base">
    <title>
      Make sure all references to are reachable.
    </title>

    <rule context="//xref[@ref-type='$ref_type']">
      <assert test="@rid = $ref_elements">
        Element '<name/>', attribute rid: Mismatching id value '<value-of select="@rid"/>' of type '<value-of select="@ref-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-aff">
    <param name="ref_type" value="aff"/>
    <param name="ref_elements" value="//aff/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-app">
    <param name="ref_type" value="app"/>
    <param name="ref_elements" value="//app/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-author-notes">
    <param name="ref_type" value="author-notes"/>
    <param name="ref_elements" value="//author-notes/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-bibr">
    <param name="ref_type" value="bibr"/>
    <param name="ref_elements" value="//ref/@id | //element-citation/@id | //mixed-citation/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-contrib">
    <param name="ref_type" value="contrib"/>
    <param name="ref_elements" value="//contrib/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-corresp">
    <param name="ref_type" value="corresp"/>
    <param name="ref_elements" value="//corresp/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-disp-formula">
    <param name="ref_type" value="disp-formula"/>
    <param name="ref_elements" value="//disp-formula/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-fig">
    <param name="ref_type" value="fig"/>
    <param name="ref_elements" value="//fig/@id | //fig-group/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-fn">
    <param name="ref_type" value="fn"/>
    <param name="ref_elements" value="//fn/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-sec">
    <param name="ref_type" value="sec"/>
    <param name="ref_elements" value="//sec/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-supplementary-material">
    <param name="ref_type" value="supplementary-material"/>
    <param name="ref_elements" value="//supplementary-material/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-table">
    <param name="ref_type" value="table"/>
    <param name="ref_elements" value="//table-wrap/@id | //table-wrap-group/@id"/>
  </pattern>

  <pattern is-a="xref-reftype-integrity-base" id="xref-reftype-integrity-table-fn">
    <param name="ref_type" value="table-fn"/>
    <param name="ref_elements" value="//table-wrap-foot/fn/@id"/>
  </pattern>
  <!-- end-block -->

  <pattern id="xref-reftype-values">
    <title>
      Validate the ref-type value against a list.
    </title>

    <rule context="//xref[@ref-type]">
      <assert test="@ref-type = 'aff' or
                    @ref-type = 'app' or
                    @ref-type = 'author-notes' or
                    @ref-type = 'bibr' or 
                    @ref-type = 'contrib' or
                    @ref-type = 'corresp' or
                    @ref-type = 'disp-formula' or
                    @ref-type = 'fig' or 
                    @ref-type = 'fn' or
                    @ref-type = 'sec' or
                    @ref-type = 'supplementary-material' or
                    @ref-type = 'table' or
                    @ref-type = 'table-fn' or
                    @ref-type = 'boxed-text'">
        Element 'xref', attribute ref-type: Invalid value "<value-of select="@ref-type"/>".
      </assert>
    </rule>
  </pattern>

  <pattern id="caption_title">
    <title>
      Make sure all captions have a title element.
    </title>

    <rule context="//caption">
      <assert test="title and string-length(title) > 0">
        Element 'caption': Missing element title.
      </assert>
    </rule>
  </pattern>

  <pattern id="license_attributes">
    <title>
      Make sure all mandatory attributes are present
    </title>

    <rule context="article/front/article-meta/permissions/license">
      <assert test="@license-type">
        Element 'license': Missing attribute license-type.
      </assert>
      <assert test="@xlink:href">
        Element 'license': Missing attribute xlink:href.
      </assert>
      <assert test="@xml:lang">
        Element 'license': Missing attribute xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="license">
    <title>
      Make sure the document has a permissions element, and a valid
      license (represented as a known href).

      Valid licenses are:
        - http://creativecommons.org/licenses/by-nc/4.0/
        - http://creativecommons.org/licenses/by-nc/3.0/
        - http://creativecommons.org/licenses/by/4.0/
        - http://creativecommons.org/licenses/by/3.0/
        - http://creativecommons.org/licenses/by-nc-nd/4.0/
        - http://creativecommons.org/licenses/by-nc-nd/3.0/
    </title>

    <rule context="article/front/article-meta">
      <assert test="permissions">
        Element 'article-meta': Missing element permissions.
      </assert>
    </rule>

    <rule context="article/front/article-meta/permissions">
      <assert test="license">
        Element 'permissions': Missing element license.
      </assert>
    </rule>

    <rule context="article/front/article-meta/permissions/license[@license-type and @xlink:href]">
      <assert test="@license-type = 'open-access'">
        Element 'license', attribute license-type: Invalid value '<value-of select="@license-type"/>'.
      </assert>
      <assert test="regexp:test(@xlink:href, '^https?://creativecommons\.org/licenses/')">
        Element 'license', attribute xlink:href: Invalid value '<value-of select="@xlink:href"/>'.
      </assert>
      <assert test="@xml:lang = 'en' or @xml:lang = /article/@xml:lang">
        Element 'license', attribute xml:lang: Must be 'en' or match with article/@xml:lang.
      </assert>
    </rule>
  </pattern>

  <pattern id="ack">
    <title>
      Ack elements cannot be organized as sections (sec).
    </title>

    <rule context="article/back/ack">
      <assert test="not(sec)">
          Element 'ack': Unexpected element sec.
      </assert>
    </rule>
  </pattern>

  <pattern id="element-citation">
    <title>
      - Make sure name, etal and collab are not child of element-citation.
      - element-citation can be only child of ref elements.
    </title>

    <rule context="article/back/ref-list/ref/element-citation">
      <assert test="not(name)">
        Element 'element-citation': Unexpected element name.
      </assert>
      <assert test="not(etal)">
        Element 'element-citation': Unexpected element etal.
      </assert>
      <assert test="not(collab)">
        Element 'element-citation': Unexpected element collab.
      </assert>
    </rule>

    <rule context="//element-citation">
      <assert test="parent::ref">
        Unexpected element 'element-citation': Allowed only as child of ref elements.
      </assert>
    </rule>
  </pattern>

  <pattern id="person-group">
    <title>
      Make sure person-group-type is present.
    </title>

    <rule context="article/back/ref-list/ref/element-citation/person-group | 
                   article/front/article-meta/product/person-group">
      <assert test="@person-group-type">
        Element 'person-group': Missing attribute person-group-type.
      </assert>
      <assert test="string-length(normalize-space(text())) = 0">
        Element 'person-group': Unexpected text content. 
      </assert>
    </rule>
  </pattern>

  <pattern id="person-group-type_values">
    <title>
      person-group/@person-group-type value constraints.
    </title>

    <rule context="article/back/ref-list/ref/element-citation/person-group[@person-group-type] | 
                   article/front/article-meta/product/person-group[@person-group-type]">
      <assert test="@person-group-type = 'author' or
                    @person-group-type = 'compiler' or 
                    @person-group-type = 'editor' or
                    @person-group-type = 'translator'">
        Element 'person-group', attribute person-group-type: Invalid value '<value-of select="@person-group-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="fn_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article/front/article-meta/author-notes/fn | 
                   article/back/fn-group/fn">
      <assert test="@fn-type">
        Element 'fn': Missing attribute fn-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="fn">
    <title>
      Make sure fn-type is valid against a white list.
    </title>

    <rule context="article/back/fn-group/fn[@fn-type]">
      <assert test="@fn-type = 'abbr' or
                    @fn-type = 'com' or 
                    @fn-type = 'financial-disclosure' or
                    @fn-type = 'supported-by' or
                    @fn-type = 'presented-at' or
                    @fn-type = 'supplementary-material' or
                    @fn-type = 'other'">
        Element 'fn', attribute fn-type: Invalid value '<value-of select="@fn-type"/>'.
      </assert>
    </rule>
    <rule context="article/front/article-meta/author-notes/fn[@fn-type]">
      <assert test="@fn-type = 'author' or
                    @fn-type = 'con' or
                    @fn-type = 'conflict' or
                    @fn-type = 'corresp' or
                    @fn-type = 'current-aff' or
                    @fn-type = 'deceased' or
                    @fn-type = 'edited-by' or 
                    @fn-type = 'equal' or
                    @fn-type = 'on-leave' or
                    @fn-type = 'participating-researchers' or
                    @fn-type = 'present-address' or
                    @fn-type = 'previously-at' or
                    @fn-type = 'study-group-members' or
                    @fn-type = 'other' or
                    @fn-type = 'presented-at' or 
                    @fn-type = 'presented-by'">
        Element 'fn', attribute fn-type: Invalid value '<value-of select="@fn-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="fn-group">
    <rule context="article/back/fn-group">
      <assert test="count(title) &lt; 2">
        Element 'fn-group': There must be zero or one element title.
      </assert>
    </rule>
  </pattern>

  <pattern id="xhtml-table">
    <title>
      Tables should be fully tagged. tr elements are not supposed to be declared
      at toplevel.
    </title>

    <rule context="//table">
      <assert test="not(tr)">
        Element 'table': Unexpected element tr.
      </assert>
      <assert test="not(tbody//th)">
        Element 'table': Unexpected element th inside tbody.
      </assert>
      <assert test="not(thead//td)">
        Element 'table': Unexpected element td inside thead.
      </assert>
    </rule>
  </pattern>

  <pattern id="supplementary-material_mimetype">
    <title>
      The attributes mimetype and mime-subtype are required.
    </title>

    <rule context="article//supplementary-material">
      <assert test="@mimetype">
        Element 'supplementary-material': Missing attribute mimetype.
      </assert>
      <assert test="@mime-subtype">
        Element 'supplementary-material': Missing attribute mime-subtype.
      </assert>
    </rule>
  </pattern>

  <pattern id="article_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article">
      <assert test="@article-type">
        Element 'article': Missing attribute article-type.
      </assert>
      <assert test="@xml:lang">
        Element 'article': Missing attribute xml:lang.
      </assert>
      <assert test="@dtd-version">
        Element 'article': Missing attribute dtd-version.
      </assert>
      <assert test="@specific-use">
        Element 'article': Missing SPS version at the attribute specific-use.
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
            @article-type = 'clinical-trial' or
            @article-type = 'announcement' or
            @article-type = 'calendar' or
            @article-type = 'in-brief' or
            @article-type = 'book-received' or
            @article-type = 'news' or
            @article-type = 'reprint' or
            @article-type = 'meeting-report' or
            @article-type = 'abstract' or
            @article-type = 'product-review' or
            @article-type = 'dissertation' or
            @article-type = 'translation'">
        Element 'article', attribute article-type: Invalid value '<value-of select="@article-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="article_specific-use-values">
    <title>
      The SPS version must be declared in article/@specific-use 
    </title>

    <rule context="article[@specific-use]">
      <assert test="@specific-use = 'sps-1.8'">
        Element 'article', attribute specific-use: Invalid value '<value-of select="@specific-use"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="named-content_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article/front/article-meta/aff/addr-line/named-content">
      <assert test="@content-type">
        Element 'named-content': Missing attribute content-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="named-content_content-type-values">
    <title>
      Allowed values for named-content/@content-type
    </title>

    <rule context="article/front/article-meta/aff/addr-line/named-content[@content-type]">
      <assert test="@content-type = 'city' or
                    @content-type = 'state'">
        Element 'named-content', attribute content-type: Invalid value '<value-of select="@content-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="month">
    <title>
      Only integers between 1 and 12.
    </title>

    <rule context="//month">
      <assert test="regexp:test(current(), '^(0?[1-9]{1}|[10-12]{2})$')">
        Element 'month': Invalid value '<value-of select="current()"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="size_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article/front/article-meta/product/size | 
                   article/back/ref-list/ref/element-citation/size">
      <assert test="@units">
        Element 'size': Missing attribute units.
      </assert>
    </rule>
  </pattern>

  <pattern id="size_units-values">
    <title>
      Allowed values for size/@units
    </title>

    <rule context="article/front/article-meta/product/size[@units] | 
                   article/back/ref-list/ref/element-citation/size[@units]">
      <assert test="@units = 'pages'">
        Element 'size', attribute units: Invalid value '<value-of select="@units"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="list_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="//list">
      <assert test="@list-type">
        Element 'list': Missing attribute list-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="list_list-type-values">
    <title>
      Allowed values for list/@list-type
    </title>

    <rule context="//list[@list-type]">
      <assert test="@list-type = 'order' or
                    @list-type = 'bullet' or
                    @list-type = 'alpha-lower' or
                    @list-type = 'alpha-upper' or
                    @list-type = 'roman-lower' or
                    @list-type = 'roman-upper' or
                    @list-type = 'simple'">
        Element 'list', attribute list-type: Invalid value '<value-of select="@list-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="media_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="//media">
      <assert test="@mime-subtype">
        Element 'media': Missing attribute mime-subtype.
      </assert>
      <assert test="@mimetype">
        Element 'media': Missing attribute mimetype.
      </assert>
      <assert test="@xlink:href">
        Element 'media': Missing attribute xlink:href.
      </assert>
    </rule>
  </pattern>

  <pattern id="ext-link_attributes">
    <title>
      Make sure some attributes are present. Also, the value of 
      ext-link-type is validated against a white-list.
    </title>

    <rule context="//ext-link">
      <assert test="@ext-link-type">
        Element 'ext-link': Missing attribute ext-link-type.
      </assert>
      <assert test="@ext-link-type = 'uri' or
                    @ext-link-type = 'clinical-trial'">
        Element 'ext-link', attribute ext-link-type: Invalid value '<value-of select="@ext-link-type"/>'.
      </assert>
      <assert test="@xlink:href">
        Element 'ext-link': Missing attribute xlink:href.
      </assert>
    </rule>
  </pattern>

  <pattern id="ext-link_href_values">
    <title>
        All URIs are supported, except "file", because we dont want references 
        to local files.
    </title>

    <rule context="//ext-link[@ext-link-type='uri']">
      <assert test="regexp:test(@xlink:href, '^[a-zA-Z][a-zA-Z0-9+\.-]+:', 'i')">
        Element 'ext-link', attribute xlink:href: Missing URI scheme in '<value-of select="@xlink:href"/>'.
      </assert>

      <assert test="not(starts-with(@xlink:href, 'file:'))">
        Element 'ext-link', attribute xlink:href: Invalid URI scheme 'file'.
      </assert>
    </rule>
  </pattern>

  <pattern id="element-citation_attributes">
    <title>
      Make sure some attributes are present. 
    </title>

    <rule context="article/back/ref-list/ref/element-citation">
      <assert test="@publication-type">
        Element 'element-citation': Missing attribute publication-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="element-citation_publication-type-values">
    <title>
      Allowed values for element-citation/@publication-type
    </title>

    <rule context="article/back/ref-list/ref/element-citation[@publication-type]">
      <assert test="@publication-type = 'journal' or
                    @publication-type = 'book' or
                    @publication-type = 'webpage' or
                    @publication-type = 'thesis' or
                    @publication-type = 'confproc' or
                    @publication-type = 'patent' or
                    @publication-type = 'report' or
                    @publication-type = 'software' or
                    @publication-type = 'legal-doc' or
                    @publication-type = 'newspaper' or
                    @publication-type = 'other' or
                    @publication-type = 'database'">
        Element 'element-citation', attribute publication-type: Invalid value '<value-of select="@publication-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="sub-article_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article//sub-article">
      <assert test="@article-type">
        Element 'sub-article': Missing attribute article-type.
      </assert>
      <assert test="@xml:lang">
        Element 'sub-article': Missing attribute xml:lang.
      </assert>
      <assert test="@id">
        Element 'sub-article': Missing attribute id.
      </assert>
    </rule>
  </pattern>

  <pattern id="sub-article_article-type-values">
    <title>
      Allowed values for //sub-article/@article-type
    </title>

    <rule context="//sub-article[@article-type]">
      <assert test="@article-type = 'abstract' or 
                    @article-type = 'letter' or 
                    @article-type = 'reply' or 
                    @article-type = 'translation'">
        Element 'sub-article', attribute article-type: Invalid value '<value-of select="@article-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="response_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article//response">
      <assert test="@response-type">
        Element 'response': Missing attribute response-type.
      </assert>
      <assert test="@xml:lang">
        Element 'response': Missing attribute xml:lang.
      </assert>
      <assert test="@id">
        Element 'response': Missing attribute id.
      </assert>
    </rule>
  </pattern>

  <pattern id="response_response-type-values">
    <title>
      Allowed values for //response/@response-type
    </title>

    <rule context="//response[@response-type]">
      <assert test="@response-type = 'addendum' or 
                    @response-type = 'discussion' or 
                    @response-type = 'reply'">
        Element 'response', attribute response-type: Invalid value '<value-of select="@response-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="response_related-article_attributes">
    <title>
      Make sure some attributes are present

      @id is mandatory for all use cases, so it is not implemented in this 
      pattern.
    </title>

    <rule context="article//response[@response-type='reply']//related-article">
      <assert test="@related-article-type = 'commentary-article'">
        Element 'related-article': Missing attribute related-article-type of type 'commentary-article'.
      </assert>
      <assert test="@vol">
        Element 'related-article': Missing attribute vol.
      </assert>
      <assert test="@page or @elocation-id">
        Element 'related-article': Missing attribute page or elocation-id.
      </assert>
    </rule>
  </pattern>

  <pattern id="related-article_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article//related-article">
      <assert test="@related-article-type">
        Element 'related-article': Missing attribute related-article-type.
      </assert>
      <assert test="@id">
        Element 'related-article': Missing attribute id.
      </assert>
    </rule>
  </pattern>

  <pattern id="related-article_correction_attributes">
    <title>
      Make sure some attributes are present for corrections.
      http://docs.scielo.org/projects/scielo-publishing-schema/pt_BR/1.5-branch/narr/errata.html#errata
    </title>

    <rule context="article//related-article[@related-article-type = 'corrected-article']">
      <assert test="@ext-link-type">
        Element 'related-article': Missing attribute ext-link-type.
      </assert>
      <assert test="@xlink:href">
        Element 'related-article': Missing attribute xlink:href.
      </assert>
    </rule>
  </pattern>

  <pattern id="related-article-type-values">
    <title>
      Allowed values for //related-article/@related-article-type
    </title>

    <rule context="//related-article[@related-article-type]">
      <assert test="@related-article-type = 'corrected-article' or 
                    @related-article-type = 'commentary-article' or
                    @related-article-type = 'letter' or
                    @related-article-type = 'partial-retraction' or
                    @related-article-type = 'retracted-article'">
        Element 'related-article', attribute related-article-type: Invalid value '<value-of select="@related-article-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern id="correction_related-article">
    <title>
      Articles of type correction must specify the article it relates to.
    </title>

    <rule context="article[@article-type='correction']/front/article-meta">
      <assert test="related-article/@related-article-type = 'corrected-article'">
        Element 'article-meta': Missing element related-article with related-article-type='corrected-article'.
      </assert>
    </rule>
  </pattern>  

  <pattern id="correction_article-type">
    <title>
      Ensure related-article[@related-article-type='corrected-article' is 
      defined only for correction article types.
    </title>

    <rule context="article[@article-type != 'correction']/front/article-meta/related-article">
      <assert test="not(@related-article-type = 'corrected-article')">
        Element 'related-article', attribute related-article-type: Invalid value 'corrected-article' for article-type '<value-of select="/article/@article-type"/>'. 
      </assert>
    </rule>
  </pattern>

  <pattern id="inbrief_related-article">
    <title>
      Articles of type in-brief must specify the article it relates to.
    </title>

    <rule context="article[@article-type='in-brief']/front/article-meta">
      <assert test="related-article/@related-article-type = 'article-reference'">
        Element 'article-meta': Missing element related-article with related-article-type='article-reference'.
      </assert>
    </rule>
  </pattern>  

  <pattern id="inbrief_article-type">
    <title>
      Ensure related-article[@related-article-type='article-reference' is 
      defined only for in-brief article types.
    </title>

    <rule context="article[@article-type != 'in-brief']/front/article-meta/related-article">
      <assert test="not(@related-article-type = 'article-reference')">
        Element 'related-article', attribute related-article-type: Invalid value 'article-reference' for article-type '<value-of select="/article/@article-type"/>'. 
      </assert>
    </rule>
  </pattern>

  <pattern id="funding-group">
    <title></title>

    <rule context="article/back//fn[@fn-type='financial-disclosure']">
      <assert test="/article/front/article-meta/funding-group/funding-statement">
        Element 'fn': Missing element funding-statement.
      </assert>
    </rule>
  </pattern>

  <pattern id="funding-group_elements">
    <title>
      Make sure mandatory child elements are present.  
    </title>

    <rule context="article/front/article-meta/funding-group">
      <assert test="award-group">
        Element 'funding-group': Missing element award-group.
      </assert>
    </rule>
  </pattern>

  <pattern id="aff_country-attrs">
    <title>
      Ensure the attribute 'country' is present for all //aff/country elements.
    </title>

    <rule context="article/front/article-meta/aff/country">
      <assert test="@country">
        Element 'country': Missing attribute country.
      </assert>
    </rule>
  </pattern>

  <pattern id="aff_country">
    <title>
      //aff/country elements cannot be empty.
    </title>

    <rule context="article/front/article-meta/aff/country">
      <assert test="string-length(normalize-space(text())) > 0">
        Element 'country': Missing text content.
      </assert>
    </rule>
  </pattern>

  <pattern id="ref">
    <title>
      element-citation and mixed-citation are mandatory in ref.
    </title>

    <rule context="article/back/ref-list/ref">
      <assert test="mixed-citation">
        Element 'ref': Missing element mixed-citation.
      </assert>
      <assert test="element-citation">
        Element 'ref': Missing element element-citation.
      </assert>
    </rule>
  </pattern>

  <pattern id="ref_notempty" is-a="assert-not-empty">
    <param name="base_context" value="article/back/ref-list/ref/mixed-citation"/>
    <param name="assert_expr" value="text()"/>
    <param name="err_message" value="'Element cannot be empty.'"/>
  </pattern>

  <pattern id="contrib-id_attributes">
    <title>
      Make sure some attributes are present
    </title>

    <rule context="article//contrib-group/contrib-id">
      <assert test="@contrib-id-type">
        Element 'contrib-id': Missing attribute contrib-id-type.
      </assert>
    </rule>
  </pattern>

  <pattern id="contrib-id-type-values">
    <title>
      Allowed values for //contrib/contrib-id/@contrib-id-type
    </title>

    <rule context="article//contrib-group/contrib-id[@contrib-id-type]">
      <assert test="@contrib-id-type = 'lattes' or 
                    @contrib-id-type = 'orcid' or 
                    @contrib-id-type = 'researchid' or
                    @contrib-id-type = 'scopus'">
        Element 'contrib-id', attribute contrib-id-type: Invalid value '<value-of select="@contrib-id-type"/>'.
      </assert>
    </rule>
  </pattern>

  <pattern abstract="true" id="occurs_zero_or_once">
    <rule context="$base_context">
      <assert test="count($element) &lt; 2">
        Element '<name/>': There must be zero or one element <value-of select="name($element)"/>.
      </assert>
    </rule>
  </pattern>

  <pattern abstract="true" id="occurs_once">
    <rule context="$base_context">
      <assert test="count($element) = 1">
        Element '<name/>': There must be only one element <value-of select="name($element)"/>.
      </assert>
    </rule>
  </pattern>

  <pattern id="source_cardinality" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation | 
                                      article/front/article-meta/product"/>
    <param name="element" value="source"/>
  </pattern>

  <pattern id="size_cardinality" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation | 
                                      article/front/article-meta/product"/>
    <param name="element" value="size"/>
  </pattern>

  <pattern id="month_cardinality" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation"/>
    <param name="element" value="month"/>
  </pattern>

  <pattern id="issue_cardinality" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation"/>
    <param name="element" value="issue"/>
  </pattern>

  <pattern id="chapter-title_cardinality" is-a="occurs_zero_or_once">
    <param name="base_context" value="article/back/ref-list/ref/element-citation | 
                                      article/front/article-meta/product"/>
    <param name="element" value="chapter-title"/>
  </pattern>

  <pattern id="element-citation_cardinality" is-a="occurs_once">
    <param name="base_context" value="article/back/ref-list/ref"/>
    <param name="element" value="element-citation"/>
  </pattern>

  <pattern id="related-article_ext-link-type-values">
    <title>
      Allowed values for //related-article/@ext-link-type
    </title>

    <rule context="article/front/article-meta/related-article[@ext-link-type]">
      <assert test="@ext-link-type = 'doi' or 
                    @ext-link-type = 'scielo-pid' or 
                    @ext-link-type = 'scielo-aid'">
        Element 'related-article', attribute ext-link-type: Invalid value '<value-of select="@ext-link-type"/>'.
      </assert>
    </rule>
  </pattern>

</schema>

