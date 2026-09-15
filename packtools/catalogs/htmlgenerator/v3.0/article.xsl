<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="no" xml:space="preserve"/>

    <xsl:include href="config-vars.xsl"/>

    <xsl:variable name="article" select="./article"/>

    <xsl:include href="generic.xsl"/>

    <xsl:include href="config-labels.xsl"/>

    <xsl:include href="journal-meta.xsl"/>

    <xsl:include href="article-custom-meta-group.xsl"/>
    <xsl:include href="article-meta.xsl"/>
    <xsl:include href="article-meta-permissions.xsl"/>
    <xsl:include href="article-meta-contrib.xsl"/>
    <xsl:include href="article-meta-abstract.xsl"/>
    <xsl:include href="article-meta-product.xsl"/>
    <!--  -->
    <xsl:include href="article-meta-related-article.xsl"/>

    <xsl:include href="generic-history.xsl"/>
    <xsl:include href="generic-pub-date.xsl"/>

    <xsl:include href="article-text-position_index.xsl"/>
    <xsl:include href="article-text-xref.xsl"/>

    <xsl:include href="article-text.xsl"/>
    <xsl:include href="article-text-mathml.xsl"/>
    <xsl:include href="article-text-def-list.xsl"/>

    <xsl:include href="article-text-boxed-text.xsl"/>
    <xsl:include href="article-text-list.xsl"/>
    <xsl:include href="article-text-supplementary-material.xsl"/>
    <xsl:include href="article-text-section-data-availability.xsl"/>

    <xsl:include href="article-text-graphic.xsl"/>
    <xsl:include href="article-text-table.xsl"/>
    <xsl:include href="article-text-formula.xsl"/>
    <xsl:include href="article-text-fig.xsl"/>
    <xsl:include href="article-text-media.xsl"/>

    <xsl:include href="article-text-back.xsl"/>
    <xsl:include href="article-text-ref.xsl"/>
    <xsl:include href="article-text-fn.xsl"/>
    <xsl:include href="article-text-bio.xsl"/>

    <xsl:include href="article-text-sub-article.xsl"/>

    <xsl:include href="html-modals-graphics.xsl"/>
    <xsl:include href="html-modals.xsl"/>
    <xsl:include href="html-modals-contribs.xsl"/>
    <xsl:include href="html-modals-tables.xsl"/>
    <xsl:include href="html-modals-figs.xsl"/>
    <xsl:include href="html-modals-scheme.xsl"/>
    <xsl:include href="html-modals-how2cite.xsl"/>
    <xsl:include href="html-head.xsl"/>

    <xsl:include href="bottom-floating-menu.xsl"/>

    <xsl:variable name="ref" select="//ref"/>
    <xsl:variable name="fn" select="//*[name()!='table-wrap-foot']//fn"/>

    <!--xsl:variable name="prev"><xsl:apply-templates select="article/back/ref-list" mode="previous"/></xsl:variable>
    <xsl:variable name="next"><xsl:apply-templates select="article/back/ref-list" mode="next"/></xsl:variable-->

    <xsl:variable name="REFLIST_INDEX">
        <xsl:apply-templates select="article/back/*[title]" mode="index"/>
    </xsl:variable>

    <xsl:variable name="q_abstract_title">
        <xsl:apply-templates select="article" mode="count_abstract_title"/>
    </xsl:variable>
    <xsl:variable name="q_abstract">
        <xsl:apply-templates select="article" mode="count_abstracts"/>
    </xsl:variable>

    <xsl:template match="/">
        <xsl:choose>
            <xsl:when test="$output_style='website'">
                <xsl:apply-templates select="." mode="website"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="default"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="/" mode="default">
        <html class="no-js">
            <head>
                <meta charset="utf-8"/>
                <meta name="viewport" content="width=device-width, initial-scale=1"/>
                <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
                <xsl:apply-templates select="." mode="html-head-title"/>
                <xsl:apply-templates select="." mode="html-head-meta"/>
                <xsl:apply-templates select="." mode="css"/>
                <link rel="alternate" type="application/rss+xml" title="SciELO" href=""/>
            </head>
            <body class="journal article">
                <a name="top"/>
                <xsl:apply-templates select="." mode="website"/>
                <!--
                    isso não fará parte do site,
                    o site tem seus próprios
                -->
                <xsl:apply-templates select="." mode="graphic-elements-title"/>
                <xsl:apply-templates select="." mode="js"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="/" mode="website">
        <div id="standalonearticle">
            <!--
                este id='standalonearticle' é usado pelo opac para
                extrair o que interessa apresentar no site
            -->
            <xsl:apply-templates select="." mode="article"/>
            <xsl:apply-templates select="." mode="article-modals"/>
        </div>
    </xsl:template>
    <xsl:template match="/" mode="graphic-elements-title">
        <xsl:apply-templates select="." mode="bottom-floating-menu"/>
    </xsl:template>

    <xsl:template match="/" mode="css">
        <!--link rel="stylesheet" href="https://ds.scielo.org/css/bootstrap.css"/>
        <link rel="stylesheet" href="https://ds.scielo.org/css/article.css"/-->
        <link rel="stylesheet" href="{$CSS_PATH}/bootstrap.css?v=1.1.32"/>
        <link rel="stylesheet" href="{$CSS_PATH}/article.css?v=1.1.32"/>
        <xsl:apply-templates select="." mode="modal-contrib-group-css"/>
    </xsl:template>

    <xsl:template match="*" mode="modal-contrib-group-css">
        <style>
        <![CDATA[
     :root {
      --author-link: #0056b3;
      --author-link-hover: #003f82;
      --author-button-bg: #6c757d;
      --author-button-border: #6c757d;
      --author-button-hover: #5c636a;
      --author-focus: rgba(13, 110, 253, 0.32);
    }

    *,
    *::before,
    *::after {
      box-sizing: border-box;
    }

    .scielo__contribGroup {
      margin-top: 1.25rem;
      text-align: center;
    }

    .author-list,
    .author-list__hidden {
      display: inline;
      padding: 0;
      margin: 0;
      list-style: none;
    }

    .author-list > li,
    .author-list__hidden > li {
      display: inline;
    }

    /* A vírgula entre autores já é inserida via .author-separator no markup.
    .author-list > li:not(:last-child)::after,
    .author-list__hidden > li:not(:last-child)::after {
      content: ",";
      margin-right: 0.25rem;
      color: #212529;
    } */

    .author-link {
      display: inline-flex;
      align-items: center;
      gap: 0.25rem;
      color: var(--author-link);
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      text-decoration: none;
    }

    .author-link:hover {
      color: var(--author-link-hover);
      text-decoration: underline;
    }

    .author-link:focus-visible,
    .authors-collapse summary:focus-visible {
      outline: 0.2rem solid var(--author-focus);
      outline-offset: 0.15rem;
      border-radius: 0.2rem;
    }

    .author-corresponding-icon {
      width: 1rem;
      height: 1rem;
      flex: 0 0 auto;
      fill: currentColor;
      vertical-align: -0.125em;
    }

    /* O details participa da mesma linha dos autores. */
    .authors-collapse {
      display: inline;
    }

    /* Remove o contêiner visual da lista interna. Os autores continuam
       participando do fluxo de texto e quebram linha naturalmente. */
    .authors-collapse[open] .author-list__hidden {
      display: contents;
    }

    .authors-collapse summary {
      display: inline-block;
      margin: 0 0.25rem 0 0;
      padding: 0.25rem 0.5rem;
      border: 1px solid var(--author-button-border);
      border-radius: 0.25rem;
      color: #fff;
      background: var(--author-button-bg);
      font: inherit;
      font-size: 0.875rem;
      line-height: 1.5;
      vertical-align: baseline;
      white-space: nowrap;
      cursor: pointer;
      user-select: none;
      list-style: none;
    }

    .authors-collapse summary::-webkit-details-marker {
      display: none;
    }

    .authors-collapse summary::marker {
      content: "";
    }

    .authors-collapse summary:hover {
      background: var(--author-button-hover);
      border-color: var(--author-button-hover);
    }

    .authors-collapse__close {
      display: none;
    }

    .authors-collapse[open] .authors-collapse__open {
      display: none;
    }

    .authors-collapse[open] .authors-collapse__close {
      display: inline;
    }

    @media (prefers-reduced-motion: reduce) {
      *,
      *::before,
      *::after {
        scroll-behavior: auto !important;
      }
    }
        ]]>
        </style>
    </xsl:template>

    <xsl:template match="/" mode="js">
        <script src="{$JS_PATH}/scielo-bundle-min.js"></script>
        <script src="{$JS_PATH}/scielo-article-min.js"></script>

        <xsl:if test=".//tex-math or .//math or .//mml:math">
            <script>
            MathJax = {
              tex: {
                inlineMath: [['$', '$'], ['\\(', '\\)']]
              },
              svg: {
                fontCache: 'global'
              }
            };
            </script>
            <script type="text/javascript" id="MathJax-script" async="true"
              src="{$MATHJAX}">
            </script>
        </xsl:if>
        <xsl:if test="$CROSSMARK_POLICY_PAGE!=''">
            <script src="https://crossmark-cdn.crossref.org/widget/v2.0/widget.js"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article" mode="article">
        <!--
        <xsl:comment> LANG=<xsl:value-of select="$TEXT_LANG"/> </xsl:comment>
        -->
        <section class="articleCtt">
            <div class="container">
                <div class="articleTxt">
                    <xsl:apply-templates select="." mode="articleBadge-editionMeta-doi-copyLink"/>

                    <!--  -->
                    <xsl:apply-templates select="." mode="article-meta-related-article"/>
                    <xsl:apply-templates select="." mode="article-title"/>

                    <xsl:apply-templates select="." mode="article-meta-trans-title"/>
                    <div class="articleMeta">
                    </div>
                    <xsl:apply-templates select="." mode="article-meta-contrib"/>
                    <xsl:apply-templates select="." mode="article-or-abstract"/>
                </div>
            </div>
        </section>
    </xsl:template>

    <xsl:template match="article" mode="article-or-abstract">
        <xsl:variable name="navigation_text">
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">article_navigation</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <div class="row">
            <nav class="col-12 col-md-4 col-lg-3">
                <!-- 
                menu lateral esquerdo - seções do texto
                -->
                <ul class="articleMenu list-group mt-4">
                </ul>
            </nav>
            <div class="col-sm-12 col-md-8 col-lg-9">
                <xsl:choose>
                    <xsl:when test="$gs_abstract_lang">
                        <xsl:apply-templates select="." mode="div-abstract"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:apply-templates select="." mode="div-article"/>
                    </xsl:otherwise>
                </xsl:choose>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="article" mode="div-article">
        <article id="articleText">
            <xsl:apply-templates select="." mode="article-meta-product"/>
            <xsl:apply-templates select="." mode="article-meta-abstract"/>
            <xsl:apply-templates select="." mode="article-meta-no-abstract-keywords"/>
            <xsl:apply-templates select="." mode="text-body"/>
            <xsl:apply-templates select="." mode="text-back"/>
            <xsl:apply-templates select="." mode="text-fn"/>
            <xsl:apply-templates select="." mode="author-notes-as-sections"/>
            <xsl:apply-templates select="." mode="article-text-sub-articles"/>

            <xsl:apply-templates select="." mode="data-availability"/>

            <xsl:apply-templates select="front/article-meta" mode="generic-pub-date"/>
            <xsl:apply-templates select="front/article-meta" mode="generic-history"/>
            <section class="documentLicense">
                <div class="container-license">
                    <div class="row">
                        <xsl:apply-templates select="." mode="article-meta-permissions"></xsl:apply-templates>
                    </div>
                </div>
            </section>
            <xsl:apply-templates select=".//related-article[@related-article-type='preprint']" mode="hidden-box"/>
        </article>
    </xsl:template>

    <xsl:template match="article" mode="div-abstract">
        <article id="articleText">
            <xsl:apply-templates select="." mode="article-meta-abstract-gs"/>
        </article>
    </xsl:template>

    <xsl:template match="article" mode="articleBadge-editionMeta-doi-copyLink">
        <div class="articleBadge-editionMeta-doi-copyLink">
            <span class="_articleBadge"><xsl:apply-templates select="." mode="article-meta-subject"/></span>
            <span class="_separator"> • </span>
            <span class="_editionMeta">
                <xsl:apply-templates select="." mode="journal-meta-bibstrip-title"/>
                <xsl:text> </xsl:text>
                <xsl:apply-templates select="." mode="journal-meta-bibstrip-issue"/>
                <span class="_separator"> • </span>
                <xsl:apply-templates select="." mode="issue-meta-pub-dates"/>
            </span>
            <span class="_separator"> • </span>

            <span class="group-doi">
                <xsl:apply-templates select="." mode="article-meta-doi"/>
            </span>
            <xsl:if test="$CROSSMARK_POLICY_PAGE!=''">
                <a data-target="crossmark">
                    <img src="https://crossmark-cdn.crossref.org/widget/v2.0/logos/CROSSMARK_Color_horizontal.svg" width="150"/>
                </a>
            </xsl:if>
        </div>
    </xsl:template>

    <xsl:template match="article" mode="article-title">
        <h1 class="article-title">
            <img
                alt="Open-access"
                class="logo-open-access"
                data-bs-toggle="tooltip"
                >
                <xsl:attribute name="src">https://ds.scielo.org/img/logo-open-access.svg</xsl:attribute>
                <xsl:attribute name="data-original-title"><xsl:apply-templates select="." mode="article-meta-permissions-data-original-title"/></xsl:attribute>
            </img><xsl:text> <!-- espaço --></xsl:text>
            <xsl:apply-templates select="." mode="article-meta-title"/>
            <a id="shorten" href="#" class="short-link"><span class="sci-ico-link"/></a>
        </h1>
    </xsl:template>
</xsl:stylesheet>