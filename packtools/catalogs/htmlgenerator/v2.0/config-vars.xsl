<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:param name="article_lang"/>
    <xsl:param name="is_translation" />
    <xsl:param name="issue_label" />
    <xsl:param name="styles_css_path" />
    <xsl:param name="print_styles_css_path" />
    <xsl:param name="js_path" />
    
    <xsl:variable name="INTERFACE_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="TEXT_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="ARTICLE_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    
    <xsl:variable name="PRINT_CSS_PATH"><xsl:value-of select="$print_styles_css_path"/></xsl:variable>
    <xsl:variable name="CSS_PATH"><xsl:value-of select="$styles_css_path"/></xsl:variable>
    <xsl:variable name="JS_PATH"><xsl:value-of select="$js_path"/></xsl:variable>
    
    
</xsl:stylesheet>