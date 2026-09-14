<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-back.xsl"/>

    <xsl:template match="*" mode="back-section-menu">
        <xsl:variable name="title"><xsl:apply-templates select="." mode="back-section-title"/></xsl:variable>
        
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <xsl:attribute name="class">articleSection</xsl:attribute>
        <xsl:attribute name="data-anchor">
            <xsl:choose>
                <xsl:when test="contains($title, ':')">
                    <xsl:value-of select="substring($title, 1, string-length($title)-1)"/>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:value-of select="$title"/>
                </xsl:otherwise>
            </xsl:choose>
        </xsl:attribute>
    </xsl:template>

    <xsl:template match="*" mode="back-section-h">
        <h2 class="h5">
            <xsl:apply-templates select="." mode="back-section-title"/>
        </h2>
    </xsl:template>

</xsl:stylesheet>