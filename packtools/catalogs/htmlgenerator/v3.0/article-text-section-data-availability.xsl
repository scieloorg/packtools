<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-section-data-availability.xsl"/>

    <xsl:template match="article | sub-article" mode="doc-version-data-availability">
        <xsl:apply-templates select="body | back" mode="bottom-of-the-page-data-availability"/>
    </xsl:template>

    <xsl:template match="article" mode="bottom-of-the-page-data-availability">
        <xsl:choose>
            <xsl:when test="body/sec[@sec-type='data-availability']">
                <!-- ficará destacado naturalmente por ser uma seção -->
            </xsl:when>
            <xsl:when test=".//*[@fn-type='data-availability'] or .//article-meta/supplementary-material or .//element-citation[@publication-type='data' or @publication-type='database'] or .//sec/sec[@sec-type='data-availability']">
                <xsl:apply-templates select="." mode="data-availability-menu-title"/>
                <xsl:choose>
                    <xsl:when test="sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                        <!-- sub-article -->
                        <xsl:apply-templates select="sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']" mode="doc-version-data-availability"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <!-- article -->
                        <xsl:apply-templates select="." mode="doc-version-data-availability"/>
                    </xsl:otherwise>
                </xsl:choose>
                <xsl:apply-templates select=".//article-meta/supplementary-material" mode="bottom-of-the-page-data-availability"/>
                <xsl:apply-templates select="back//ref-list" mode="bottom-of-the-page-data-availability"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="body | back" mode="bottom-of-the-page-data-availability">
        <!-- Deixa em destaque nota ou seção referente à disponibilidade de dados no final da página -->
        <xsl:apply-templates select=".//*[@fn-type='data-availability']" mode="bottom-of-the-page-data-availability"/>
        <xsl:apply-templates select="sec//sec[@sec-type='data-availability']" mode="bottom-of-the-page-data-availability"/>
    </xsl:template>

    <xsl:template match="sec[@sec-type='data-availability']" mode="bottom-of-the-page-data-availability">
        <xsl:apply-templates select="*[name()!='title']|text()"/>
    </xsl:template>

    <xsl:template match="article" mode="data-availability-menu-title">
        <xsl:variable name="title">
            <xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">Data availability</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div>
            <xsl:call-template name="article-section-header">
                <xsl:with-param name="title" select="$title"/>
            </xsl:call-template>
        </div>
    </xsl:template>

    <xsl:template match="ref-list" mode="bottom-of-the-page-data-availability">
        <xsl:if test=".//element-citation[@publication-type='data' or @publication-type='database']">
            <h2 class="h5"><xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">Data citations</xsl:with-param>
                </xsl:apply-templates></h2>
            <xsl:apply-templates select=".//element-citation[@publication-type='data' or @publication-type='database']" mode="bottom-of-the-page-data-availability"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="fn" mode="bottom-of-the-page-data-availability">
        <div class="row">
            <div class="col-md-12 col-sm-12">
                <xsl:apply-templates select="p" mode="bottom-of-the-page-data-availability"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="fn/label" mode="bottom-of-the-page-data-availability">
        <p>
            <strong><xsl:apply-templates select="*|text()"/></strong>
        </p>
    </xsl:template>
    <xsl:template match="fn/p" mode="bottom-of-the-page-data-availability">
        <p>
            <xsl:apply-templates select="*|text()"/>
        </p>
    </xsl:template>
</xsl:stylesheet>