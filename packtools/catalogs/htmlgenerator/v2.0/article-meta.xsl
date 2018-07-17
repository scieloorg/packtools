<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <xsl:template match="article" mode="article-meta-subject">
        <!--
        <xsl:comment> <xsl:value-of select="$TEXT_LANG"/> </xsl:comment>
        -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//subject" mode="display"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta//subject"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-title">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//*/title-group/article-title"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta//trans-title-group[@xml:lang=$TEXT_LANG]/trans-title">
                <xsl:apply-templates select="front/article-meta//trans-title-group[@xml:lang=$TEXT_LANG]/trans-title"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta//article-title"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-trans-title">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
            </xsl:when>
            <xsl:when test="front/article-meta//trans-title-group[@xml:lang=$TEXT_LANG]/trans-title">
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="front/article-meta//trans-title-group//trans-title" mode="translation"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="trans-title" mode="translation">
        <h2 class="article-title"><xsl:apply-templates select="*|text()"></xsl:apply-templates></h2>
    </xsl:template>
    
    <xsl:template match="*" mode="article-meta-doi">
        <xsl:apply-templates select="front/article-meta//article-id[@pub-id-type='doi']" mode="display"></xsl:apply-templates>        
    </xsl:template>
   
    <xsl:template match="article-id[@pub-id-type='doi']" mode="display">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <span class="_doi"><xsl:value-of select="$link"/></span>
        &#160;
        <a class="copyLink" data-clipboard-text="{$link}">
            <span class="sci-ico-link"/> 
            <xsl:apply-templates select="." mode="interface">
                <xsl:with-param name="text">copy</xsl:with-param>
            </xsl:apply-templates>
        </a>
    </xsl:template>
    
    <xsl:template match="article" mode="issue-meta-pub-dates">
        
        <xsl:choose>
            <xsl:when test="front/article-meta/pub-date[@pub-type='collection']">
                <xsl:apply-templates  select="front/article-meta/pub-date[@pub-type='collection']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta/pub-date[@pub-type='ppub']">
                <xsl:apply-templates  select="front/article-meta/pub-date[@pub-type='ppub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta/pub-date[@pub-type='ppub-epub']">
                <xsl:apply-templates  select="front/article-meta/pub-date[@pub-type='ppub-epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta/pub-date[@pub-type='epub-ppub']">
                <xsl:apply-templates  select="front/article-meta/pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select="front/article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-pub-dates">
        <xsl:apply-templates select="front/article-meta/pub-date[1]" mode="generated-label"></xsl:apply-templates>&#160;
        
        <xsl:choose>
            <xsl:when test="front/article-meta/pub-date[@pub-type='epub']">
                <xsl:apply-templates  select="front/article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select="front/article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
