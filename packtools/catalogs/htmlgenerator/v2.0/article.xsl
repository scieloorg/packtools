<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">


    <xsl:output method="html" indent="yes"  encoding="UTF-8" omit-xml-declaration="no"  xml:space="default" />

    <xsl:include href="config-vars.xsl"/>

    <xsl:variable name="article" select="./article"/>

    <xsl:include href="generic.xsl"/>

    <xsl:include href="config-labels.xsl"/>

    <xsl:include href="journal-meta.xsl"/>

    <xsl:include href="article-meta.xsl"/>
    <xsl:include href="article-meta-contrib.xsl"/>
    <xsl:include href="article-meta-abstract.xsl"/>
    <xsl:include href="article-meta-product.xsl"/>

    <xsl:include href="generic-history.xsl"/>

    <xsl:include href="article-text-xref.xsl"/>

    <xsl:include href="article-text.xsl"/>
    <xsl:include href="article-text-alternatives.xsl"/>

    <xsl:include href="article-text-boxed-text.xsl"/>
    <xsl:include href="article-text-list.xsl"/>
    <xsl:include href="article-text-supplementary-material.xsl"/>

    <xsl:include href="article-text-graphic.xsl"/>
    <xsl:include href="article-text-table.xsl"/>
    <xsl:include href="article-text-formula.xsl"/>
    <xsl:include href="article-text-fig.xsl"/>

    <xsl:include href="article-text-back.xsl"/>
    <xsl:include href="article-text-ref.xsl"/>
    <xsl:include href="article-text-fn.xsl"/>
    <xsl:include href="article-text-bio.xsl"/>

    <xsl:include href="article-text-sub-article.xsl"/>

    <xsl:include href="html-modals.xsl"/>
    <xsl:include href="html-modals-contribs.xsl"/>
    <xsl:include href="html-modals-tables.xsl"/>
    <xsl:include href="html-modals-figs.xsl"/>
    <xsl:include href="html-head.xsl"/>

    <xsl:variable name="ref" select="//ref"></xsl:variable>
    <xsl:variable name="fn" select="//*[name()!='table-wrap']//fn"></xsl:variable>
    
    <xsl:variable name="prev"><xsl:apply-templates select="article/back/ref-list" mode="previous"/></xsl:variable>
    <xsl:variable name="next"><xsl:apply-templates select="article/back/ref-list" mode="next"/></xsl:variable>
    <xsl:variable name="reflist_position"><xsl:apply-templates select="article/back/*" mode="position"><xsl:with-param name="name">ref-list</xsl:with-param></xsl:apply-templates></xsl:variable>
    
    <xsl:variable name="q_abstract_title"><xsl:apply-templates select="article" mode="count_abstract_title"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_abstract"><xsl:apply-templates select="article" mode="count_abstracts"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_front"><xsl:choose>
        <xsl:when test="$q_abstract_title=0"><xsl:value-of select="$q_abstract"/></xsl:when>
        <xsl:otherwise><xsl:value-of select="$q_abstract_title"/></xsl:otherwise>
    </xsl:choose></xsl:variable>
    <xsl:variable name="q_back"><xsl:apply-templates select="article" mode="count_back_elements"></xsl:apply-templates></xsl:variable>
    <xsl:variable name="q_body_fn">0<!--xsl:apply-templates select="article" mode="count_body_fn"></xsl:apply-templates--></xsl:variable>
    <xsl:variable name="q_history"><xsl:apply-templates select="article" mode="count_history"/></xsl:variable>
    <xsl:variable name="q_subarticle"><xsl:apply-templates select="article" mode="count_subarticle"></xsl:apply-templates></xsl:variable>
    
    <xsl:template match="/">
        <!--[if lt IE 7]>      <html class="no-js lt-ie9 lt-ie8 lt-ie7"> <![endif]-->
        <!--[if IE 7]>         <html class="no-js lt-ie9 lt-ie8"> <![endif]-->
        <!--[if IE 8]>         <html class="no-js lt-ie9"> <![endif]-->
        <!--[if gt IE 8]><!-->
        <html class="no-js">
            <!--<![endif]-->
            <head>
                <meta charset="utf-8"/>
                <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1"/>
                <xsl:apply-templates select="." mode="html-head-title"/>
                <xsl:apply-templates select="." mode="html-head-meta"/>
                <xsl:apply-templates select="." mode="css"/>
                <link rel="alternate" type="application/rss+xml" title="SciELO" href=""/>
            </head>
            <body class="journal article">
                <a name="top"/>
                <xsl:apply-templates select="." mode="article"/>
                <xsl:apply-templates select="." mode="article-modals"/>
                <xsl:apply-templates select="." mode="js"/>
            </body>
        </html>
    </xsl:template>
    <xsl:template match="/" mode="css">

        <xsl:choose>
            <xsl:when test="substring($CSS_PATH,string-length($CSS_PATH)-3)='.css'">
                <link rel="stylesheet" href="{$CSS_PATH}"/>
            </xsl:when>
            <xsl:otherwise>
                <link rel="stylesheet" href="{$CSS_PATH}/css/bootstrap.min.css"/>
                <link rel="stylesheet" href="{$CSS_PATH}/css/article-styles.css"/>
                <link rel="stylesheet" href="{$CSS_PATH}/css/scielo-print.css" media="print"/>
             </xsl:otherwise>
        </xsl:choose>
        <xsl:if test="$PRINT_CSS_PATH!=''">
            <link rel="stylesheet" href="{$PRINT_CSS_PATH}" media="print"/>
        </xsl:if>
    </xsl:template>
    <xsl:template match="/" mode="js">
        <xsl:choose>
            <xsl:when test="substring($JS_PATH,string-length($JS_PATH)-2)='.js'">
                <script src="{$JS_PATH}"/>
            </xsl:when>
            <xsl:otherwise>
                <script src="{$JS_PATH}/js/vendor/jquery-1.11.0.min.js"></script>
                <script src="{$JS_PATH}/js/vendor/bootstrap.min.js"></script>
                <script src="{$JS_PATH}/js/vendor/jquery-ui.min.js"></script>

                <script src="{$JS_PATH}/js/plugins.js"></script>
                <script src="{$JS_PATH}/js/min/main-min.js"></script>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="article" mode="article">
        <section class="articleCtt">
            <div class="container">
                <div class="articleTxt">
                    <div class="editionMeta">
                        <span>
                            <xsl:apply-templates select="." mode="journal-meta-bibstrip-title"/>
                            <xsl:text> </xsl:text>
                            <xsl:apply-templates select="." mode="journal-meta-bibstrip-issue"/>
                            <!-- FIXME location -->
                            <xsl:apply-templates select="." mode="issue-meta-pub-dates"/>
                        </span>
                        <xsl:text> </xsl:text>
                        <xsl:apply-templates select="." mode="journal-meta-issn"/>
                    </div>
                    <h1 class="article-title">
                        <xsl:apply-templates select="." mode="article-meta-title"/>
                    </h1>
                    <div class="articleMeta">
                        <div>
                            <!-- FIXME -->
                            <span>
                                <xsl:apply-templates select="." mode="article-meta-pub-dates"/></span>
                            <xsl:apply-templates select="." mode="article-meta-license"/>
                        </div>
                        <div>
                            <xsl:apply-templates select="." mode="article-meta-doi"/>

                        </div>
                    </div>

                    <xsl:apply-templates select="." mode="article-meta-contrib"/>

                    <div class="row">
                        <ul class="col-md-2 hidden-sm articleMenu">

                        </ul>

                        <article id="articleText" class="col-md-10 col-md-offset-2 col-sm-12 col-sm-offset-0">
                            <xsl:apply-templates select="." mode="article-meta-product"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="article-meta-abstract"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="text-body"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="text-back"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="text-fn"></xsl:apply-templates>
                            <xsl:apply-templates select=".//article-meta" mode="generic-history"/>
                            <xsl:apply-templates select="." mode="article-text-sub-articles"></xsl:apply-templates>
                        </article>
                    </div>
                </div>
            </div>
        </section>
    </xsl:template>
    <xsl:template match="article" mode="article">
        <xsl:comment> LANG=<xsl:value-of select="$TEXT_LANG"/> </xsl:comment>
        <section class="articleCtt">
            <div class="container">
                <div class="articleTxt">
                    <div class="row">
                        <!--div>
                            <xsl:attribute name="class">hidden-sm<xsl:if test=".//product//*[@xlink:href]"> articleFigure</xsl:if></xsl:attribute>
                            <xsl:apply-templates select=".//product//*[@xlink:href]"/>
                        </div-->
                        <div class="col-md-10 col-md-offset-2 col-sm-12 col-sm-offset-0">
                            <div class="articleBadge">
                                <span><xsl:apply-templates select="." mode="article-meta-subject"/></span>
                            </div>
                           <div class="editionMeta">
                                <span>
                                    <xsl:apply-templates select="." mode="journal-meta-bibstrip-title"/>
                                    <xsl:text> </xsl:text>
                                    <xsl:apply-templates select="." mode="journal-meta-bibstrip-issue"/>
                                    <!-- FIXME location -->
                                    <xsl:apply-templates select="." mode="issue-meta-pub-dates"/>
                                </span>
                                <xsl:text> </xsl:text>
                                <xsl:apply-templates select="." mode="journal-meta-issn"/>
                            </div>
                            <h1 class="article-title">
                                <xsl:apply-templates select="." mode="article-meta-title"/>
                            </h1>
                            <div class="articleMeta">
                                <div>
                                    <!-- FIXME -->
                                    <span>
                                        <xsl:apply-templates select="." mode="article-meta-pub-dates"/></span>
                                    <xsl:apply-templates select="." mode="article-meta-license"/>
                                </div>
                                <div>
                                    <xsl:apply-templates select="." mode="article-meta-doi"/>

                                </div>
                            </div>
                            <xsl:apply-templates select="." mode="article-meta-contrib"/>
                        </div>
                    </div>
                    <div class="row">
                        <ul class="col-md-2 hidden-sm articleMenu">

                        </ul>

                        <article id="articleText" class="col-md-10 col-md-offset-2 col-sm-12 col-sm-offset-0">
                            <xsl:apply-templates select="." mode="article-meta-product"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="article-meta-abstract"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="text-body"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="article-meta-no-abstract-keywords"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="text-back"></xsl:apply-templates>
                            <xsl:apply-templates select="." mode="text-fn"></xsl:apply-templates>
                            <xsl:apply-templates select=".//article-meta" mode="generic-history"/>
                            <xsl:apply-templates select="." mode="article-text-sub-articles"></xsl:apply-templates>
                        </article>
                    </div>

                </div>
            </div>
        </section>
        <xsl:comment> $q_abstract_title=<xsl:value-of select="$q_abstract_title"/></xsl:comment>
        <xsl:comment> $q_abstract=<xsl:value-of select="$q_abstract"/></xsl:comment>
        <xsl:comment> $q_front=<xsl:value-of select="$q_front"/></xsl:comment>
        <xsl:comment> $q_back=<xsl:value-of select="$q_back"/></xsl:comment>
        <xsl:comment> $q_body_fn=<xsl:value-of select="$q_body_fn"/></xsl:comment>
        <xsl:comment> $q_history=<xsl:value-of select="$q_history"/></xsl:comment>
        <xsl:comment> $q_subarticle=<xsl:value-of select="$q_subarticle"/></xsl:comment>
        
    </xsl:template>

</xsl:stylesheet>
