<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:param name="article_lang"/>
    <xsl:param name="is_translation" />
    <xsl:param name="issue_label" />
    <xsl:param name="styles_css_path" />
    <xsl:param name="print_styles_css_path" />
    <xsl:param name="js_path" />
    <!-- google scholar abstract -->
    <xsl:param name="gs_abstract_lang" />

    <xsl:param name="permlink" />
    <xsl:param name="url_article_page" />
    <xsl:param name="url_download_ris" />
    <xsl:param name="legendary"></xsl:param>
    <xsl:param name="abbr_contrib"></xsl:param>

    <xsl:param name="math_elem_preference" select="''"/>
    <xsl:param name="math_js" select="''"/>

    <xsl:param name="output_style"/>
    
    <xsl:variable name="MATH_ELEM_PREFERENCE">
        <xsl:choose>
            <xsl:when test="$math_elem_preference='tex-math'">tex-math</xsl:when>
            <xsl:when test="$math_elem_preference='mml:math'">mml:math</xsl:when>
            <xsl:otherwise></xsl:otherwise>
        </xsl:choose>
    </xsl:variable>
    <xsl:variable name="MATHJAX">
        <xsl:choose>
            <xsl:when test="$math_js!=''"><xsl:value-of select="$math_js"/></xsl:when>
            <xsl:otherwise>https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-svg.js</xsl:otherwise>


        </xsl:choose>
    </xsl:variable>

    <xsl:variable name="ABBR_CONTRIB"><xsl:choose>
        <xsl:when test="$abbr_contrib!=''"><xsl:value-of select="$abbr_contrib"/></xsl:when>
        <xsl:otherwise>false</xsl:otherwise>
    </xsl:choose></xsl:variable>
    <xsl:variable name="URL_PERMLINK"><xsl:value-of select="$permlink"/></xsl:variable>
    <xsl:variable name="URL_ARTICLE_PAGE"><xsl:value-of select="$url_article_page"/></xsl:variable>
    <xsl:variable name="URL_DOWNLOAD_RIS"><xsl:value-of select="$url_download_ris"/></xsl:variable>
    <xsl:variable name="INTERFACE_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="TEXT_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="ARTICLE_LANG"><xsl:value-of select="$article_lang"/></xsl:variable>
    <xsl:variable name="ARTICLE_BIBSTRIP"><xsl:value-of select="$legendary"/></xsl:variable>

    <xsl:variable name="PRINT_CSS_PATH"><xsl:value-of select="$print_styles_css_path"/></xsl:variable>
    <xsl:variable name="CSS_PATH"><xsl:value-of select="$styles_css_path"/></xsl:variable>
    <xsl:variable name="JS_PATH"><xsl:value-of select="$js_path"/></xsl:variable>

    

</xsl:stylesheet>
