<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article" mode="data-availability">
        <xsl:if test="article-meta/supplementary-material or .//element-citation[@publication-type='data' or @publication-type='database']">
            <xsl:variable name="title">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text">Data availability</xsl:with-param>
                </xsl:apply-templates>
            </xsl:variable>
            <div class="articleSection">
                <xsl:attribute name="data-anchor"><xsl:value-of select="$title"/></xsl:attribute>
                <h1 class="articleSectionTitle"><xsl:value-of select="$title"/></h1>
                <xsl:apply-templates select=".//article-meta" mode="data-availability"/>
                <xsl:apply-templates select=".//ref-list" mode="data-availability"/>
             </div>
       </xsl:if>
    </xsl:template>

    <xsl:template match="article-meta" mode="data-availability">
        <xsl:apply-templates select="element-citation[@publication-type='data' or @publication-type='database']" mode="data-availability"/>
    </xsl:template>

    <xsl:template match="ref-list" mode="data-availability">
        <xsl:if test=".//element-citation[@publication-type='data' or @publication-type='database']">
            <xsl:apply-templates select=".//element-citation[@publication-type='data' or @publication-type='database']" mode="data-availability"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="article-meta/supplementary-material" mode="data-availability">
        <div class="row">
            <div class="col-md-12 col-sm-12">
                <p>
                    <xsl:apply-templates select="."/>
                </p>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="element-citation[@publication-type='data' or @publication-type='database']" mode="data-availability">
        <div class="row">
            <div class="col-md-12 col-sm-12">
                <p>
                    <xsl:apply-templates select="../mixed-citation"/>
                </p>
            </div>
        </div>
    </xsl:template>

</xsl:stylesheet>