<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:param name="article_lang" />
    <xsl:param name="is_translation" />
    <xsl:param name="issue_label" />
    <xsl:param name="styles_css_path" />
    
    <xsl:variable name="INTERFACE_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="TEXT_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="ARTICLE_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    
    <xsl:variable name="CSS_PATH"><xsl:choose>
        <xsl:when test="$styles_css_path!=''"><xsl:value-of select="$styles_css_path"/></xsl:when>
        <xsl:otherwise>/Users/roberta.takenaka/github.com/scieloorg/packtools/packtools/catalogs/htmlgenerator/v2.0/2017-03-31-Artigo-Correcoes/static/css</xsl:otherwise>
    </xsl:choose></xsl:variable>
    
    <xsl:variable name="JS_PATH"><xsl:choose>
        <xsl:when test="$styles_css_path!=''"><xsl:value-of select="$styles_css_path"/>/../js</xsl:when>
        <xsl:otherwise>/Users/roberta.takenaka/github.com/scieloorg/packtools/packtools/catalogs/htmlgenerator/v2.0/2017-03-31-Artigo-Correcoes/static/js</xsl:otherwise>
    </xsl:choose></xsl:variable>
    
</xsl:stylesheet>