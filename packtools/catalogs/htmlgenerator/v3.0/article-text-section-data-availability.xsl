<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-section-data-availability.xsl"/>

    <xsl:template match="article" mode="data-availability-menu-title">
        <xsl:variable name="title">
            <xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">Data availability</xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable>
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:value-of select="$title"/></xsl:attribute>
            <h3 class="articleSectionTitle"><xsl:value-of select="$title"/></h3>
        </div>
    </xsl:template>

    <xsl:template match="ref-list" mode="data-availability">
        <xsl:if test=".//element-citation[@publication-type='data' or @publication-type='database']">
            <h3><xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">Data citations</xsl:with-param>
                </xsl:apply-templates></h3>
            <xsl:apply-templates select=".//element-citation[@publication-type='data' or @publication-type='database']" mode="data-availability"/>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>