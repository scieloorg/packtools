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
        <link rel="stylesheet" href="{$CSS_PATH}/bootstrap.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/article.css"/>
    </xsl:template>

    <xsl:template match="/" mode="js">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js"></script>
        <script src="https://ds.scielo.org/js/bootstrap.bundle.min.js"></script>
        <script src="https://ds.scielo.org/js/scielo/scielo-ds-min.js"></script>

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
        <nav role="navigation" aria-label="{$navigation_text}">
            <ul class="-articleMenu list-group mt-4">
            <!-- item do menu lateral esquerdo -->
            </ul>
        </nav>
        <xsl:choose>
            <xsl:when test="$gs_abstract_lang">
                <xsl:apply-templates select="." mode="div-abstract"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="div-article"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="article" mode="div-article">
        <article id="articleText"
            class="col-sm-12 col-lg-10 offset-lg-2">
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
        <article id="articleText"
            class="col-md-10 col-md-offset-2 col-sm-12 col-sm-offset-0">
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