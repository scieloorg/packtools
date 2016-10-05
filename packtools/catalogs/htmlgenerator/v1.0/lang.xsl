<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="lang-article-title">
        <xsl:apply-templates select=".//article-meta//article-title"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="issn/@pub-type">
        <xsl:value-of select="."/> 
    </xsl:template>
    
    <xsl:template match="article" mode="lang-license">
        <xsl:choose>
            <xsl:when test="//article-meta//license[@xml:lang=$PAGE_LANG]">
                <xsl:apply-templates select="//article-meta//license[@xml:lang=$PAGE_LANG]"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="//article-meta//license[1]"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="lang-abstract">
        <xsl:apply-templates select=".//article-meta/abstract"></xsl:apply-templates>
    </xsl:template>
    
</xsl:stylesheet>