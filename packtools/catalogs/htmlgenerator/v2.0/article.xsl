<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">


    <xsl:output method="html" indent="yes" encoding="UTF-8" omit-xml-declaration="no"/>

    <xsl:include href="config-vars.xsl"/>

    <xsl:variable name="document" select="./article"/>
    <xsl:include href="generic.xsl"/>

    <xsl:include href="config-labels.xsl"/>

    <xsl:include href="functions-block.xsl"/>

    <xsl:include href="journal-meta.xsl"/>
    
    <xsl:include href="article-meta.xsl"/>
    <xsl:include href="article-meta-contrib.xsl"/>
    <xsl:include href="article-meta-abstract.xsl"/>

    <xsl:include href="article-text.xsl"/>
    <xsl:include href="article-text-graphic.xsl"/>
    <xsl:include href="article-text-table.xsl"/>
    <xsl:include href="article-text-formula.xsl"/>
    <xsl:include href="article-text-fig.xsl"/>
    <xsl:include href="article-text-xref.xsl"/>
    <xsl:include href="article-text-fn.xsl"/>
    <xsl:include href="article-text-ref.xsl"/>
    <xsl:include href="article-text-back.xsl"/>
    
    <xsl:include href="html-modals.xsl"/>
    <xsl:include href="html-modals-contribs.xsl"/>
    <xsl:include href="html-modals-tables.xsl"/>
    <xsl:include href="html-modals-figs.xsl"/>
    
    <xsl:include href="html-head.xsl"/>

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
        <!--FIXME-->
        <link rel="stylesheet" href="{$CSS_PATH}/bootstrap.min.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/article-styles.css"/>
        <link rel="stylesheet" href="{$CSS_PATH}/scielo-print.css" media="print"/>
    </xsl:template>
    <xsl:template match="/" mode="js">
        <!--FIXME-->
        <script src="{$JS_PATH}/vendor/jquery-1.11.0.min.js"/>
        <script src="{$JS_PATH}/vendor/bootstrap.min.js"/>
        <script src="{$JS_PATH}/vendor/jquery-ui.min.js"/>
        <script src="{$JS_PATH}/plugins.js"/>
        <script src="{$JS_PATH}/min/main-min.js"/>
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
                            <xsl:apply-templates select="." mode="article-meta-pub-dates"/>
                            <xsl:apply-templates select="." mode="article-meta-license"/>
                        </div>
                        <div>
                            <xsl:apply-templates select="." mode="article-meta-doi"/>
                            
                        </div>
                    </div>

                    <xsl:apply-templates select="." mode="article-meta-contrib"/>

                    <div class="row">
                        <ul class="col-md-2 hidden-sm articleMenu">
                            <xsl:comment> </xsl:comment>
                        </ul>

                        <xsl:apply-templates select="." mode="text"/>
                    </div>
                </div>
            </div>
        </section>
    </xsl:template>
</xsl:stylesheet>
