<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="contrib-group">
        <div class="contribGroup">
            <xsl:apply-templates select="contrib" mode="front-contrib"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="contrib" mode="front-contrib">
        <span> <xsl:apply-templates select="name|xref"/></span><xsl:if test="position()!=last()">; </xsl:if>
    </xsl:template>
    
    <xsl:template match="contrib/name">
        <xsl:apply-templates select="given-names"/><xsl:text> </xsl:text><xsl:apply-templates select="surname"/>
    </xsl:template>
    
    <xsl:template match="contrib/xref">
        <sup class="xref trigger" data-rel="#authorInfoBtn"><xsl:apply-templates></xsl:apply-templates></sup>
    </xsl:template>
    
    <xsl:template match="article" mode="front-author-notes">
        <div class="rowBlock">
            <xsl:apply-templates select=".//article-meta/author-notes"></xsl:apply-templates>    
        </div>
    </xsl:template>    
    <xsl:template match="author-notes">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="corresp/label">
        <span><xsl:apply-templates></xsl:apply-templates></span>
    </xsl:template>
    <xsl:template match="corresp">
        <p><xsl:apply-templates></xsl:apply-templates></p>
    </xsl:template>
    <xsl:template match="author-notes/fn/label">
        <h3><xsl:apply-templates></xsl:apply-templates></h3>
    </xsl:template>
    <xsl:template match="author-notes/fn">
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>