<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-meta-abstract.xsl"/>

    <xsl:template match="article" mode="create-anchor-and-title-for-abstracts-without-title">
        <xsl:variable name="q_titles" select="count(.//abstract[title])+count(.//trans-abstract[title])"/>
        <xsl:if test="$q_titles = 0">
            <xsl:variable name="q_abstracts" select="count(.//abstract[.//text()])+count(.//trans-abstract[.//text()])"/>

            <!-- obtém o título traduzido para Abstracts ou Abstract -->
            <xsl:variable name="title">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">
                        <xsl:choose>
                            <xsl:when test="$q_abstracts=1">Abstract</xsl:when>
                            <xsl:otherwise>Abstracts</xsl:otherwise>
                        </xsl:choose>
                    </xsl:with-param>
                </xsl:apply-templates>
            </xsl:variable>
            
            <!-- insere a âncora e o título -->
            <div class="articleSection" data-anchor="{$title}">
                <h3 class="articleSectionTitle"><xsl:value-of select="$title"/></h3>
            </div>
        </xsl:if>
    </xsl:template>

    <xsl:template match="abstract[title] | trans-abstract[title]" mode="anchor-and-title">
        <!-- Apresenta a âncora e o título, ou seja, Abstract, Resumo, ou Resumen -->

        <!-- âncora -->
        <xsl:attribute name="class">articleSection</xsl:attribute>
        <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
        <xsl:if test="@xml:lang='ar'">
            <xsl:attribute name="dir">rtl</xsl:attribute>
        </xsl:if>

        <!-- título -->
        <h3>
            <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
            <xsl:apply-templates select="." mode="title"></xsl:apply-templates>
        </h3>
    </xsl:template>
</xsl:stylesheet>