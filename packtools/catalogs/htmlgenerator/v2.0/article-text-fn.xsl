<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="fn" mode="xref">
        <xsl:apply-templates select="*|text()" mode="xref"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fn/label" mode="xref">
        <strong class="fn-title"><xsl:apply-templates select="*|text()" mode="xref"/></strong>
    </xsl:template>
    
    <xsl:template match="fn/p" mode="xref">
        <xsl:apply-templates select="*|text()" mode="xref"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fn">
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>
    </xsl:template>
    
    <xsl:template match="fn/label">
        <sup class="xref big"><xsl:value-of select="."></xsl:value-of></sup>
    </xsl:template>
    
    <xsl:template match="fn/p">
        <div>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="back/fn" mode="content">
        <ul class="refList footnote">
            <xsl:apply-templates select="."></xsl:apply-templates>
        </ul>
    </xsl:template>
    
    <xsl:template match="fn-group/title" mode="content">
    </xsl:template>
    
    <xsl:template match="back/fn-group" mode="content">
        <ul class="refList footnote">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </ul>
    </xsl:template>
</xsl:stylesheet>