<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article" mode="article-text-sub-articles">
        <xsl:apply-templates select="response[@xml:lang=$TEXT_LANG] | sub-article[@xml:lang=$TEXT_LANG and @article-type!='translation']"></xsl:apply-templates>
    </xsl:template>

    <xsl:template match="front-stub//article-title">
        <h2>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </h2>
    </xsl:template>
    <xsl:template match="front-stub//trans-title">
        <h3>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </h3>
    </xsl:template>
    
</xsl:stylesheet>