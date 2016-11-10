<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="front-affiliations">
        <div class="rowBlock">
            <ul>
                <xsl:apply-templates select=".//article-meta//aff"></xsl:apply-templates>
            </ul>
        </div>
    </xsl:template>
    <xsl:template match="aff">
        <li>
            <xsl:choose>
                <xsl:when test="institution[@content-type='original']">
                    <xsl:apply-templates select="label"/>
                    <xsl:apply-templates select="institution[@content-type='original']"></xsl:apply-templates>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </xsl:otherwise>
            </xsl:choose>
        </li>
    </xsl:template>
    <xsl:template match="aff/label">
        <sup class="xref big"><xsl:apply-templates></xsl:apply-templates></sup>
    </xsl:template>    
</xsl:stylesheet>