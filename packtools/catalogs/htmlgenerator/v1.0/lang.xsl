<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="article-title">
        <xsl:apply-templates select=".//article-meta//article-title"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="issn/@pub-type">
        <xsl:value-of select="."/>
    </xsl:template>
</xsl:stylesheet>