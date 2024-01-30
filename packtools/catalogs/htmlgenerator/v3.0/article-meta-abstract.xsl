<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta-abstract.xsl"/>

    <xsl:template match="article" mode="create-anchor-and-title-for-abstracts-without-title-div-h-number">
        <xsl:param name="title"/>
        <div class="articleSection" data-anchor="{$title}">
            <h3 class="articleSectionTitle"><xsl:value-of select="$title"/></h3>
        </div>
    </xsl:template>

    <xsl:template match="abstract/sec/title | trans-abstract/sec/title">
        <strong><xsl:apply-templates select="*|text()"/></strong>
    </xsl:template>

    <xsl:template match="abstract[title] | trans-abstract[title]" mode="anchor-and-title">
        <!-- Apresenta a âncora e o título, ou seja, Abstract, Resumo, ou Resumen -->

        <xsl:if test="not($gs_abstract_lang)">
            <!-- âncora -->

            <xsl:variable name="title"><xsl:apply-templates select="." mode="title"/></xsl:variable>
            <xsl:attribute name="class">articleSection articleSection--<xsl:value-of select="translate($title,'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/></xsl:attribute>
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
            <xsl:if test="@xml:lang='ar'">
                <xsl:attribute name="dir">rtl</xsl:attribute>
            </xsl:if>
        </xsl:if>

        <!-- título -->
        <h3>
            <xsl:attribute name="class">articleSectionTitle h5</xsl:attribute>
            <xsl:apply-templates select="." mode="title"></xsl:apply-templates>
        </h3>
    </xsl:template>

    <xsl:template match="abstract/sec | trans-abstract/sec">
        <p>
            <xsl:apply-templates select="*|text()"/>
        </p>
    </xsl:template>

    <xsl:template match="abstract/sec/p | trans-abstract/sec/p">
        <xsl:text>&#160;</xsl:text><xsl:apply-templates select="*|text()"/>
    </xsl:template>
</xsl:stylesheet>