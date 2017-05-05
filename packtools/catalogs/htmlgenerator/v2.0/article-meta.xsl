<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <xsl:template match="article" mode="article-meta-subject">
        <xsl:comment> <xsl:value-of select="$TEXT_LANG"/> </xsl:comment>
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//subject" mode="display"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta//subject"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-title">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']/*/title-group/article-title"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta//trans-title-group[@xml:lang=$TEXT_LANG]/trans-title">
                <xsl:apply-templates select=".//article-meta//trans-title-group[@xml:lang=$TEXT_LANG]/trans-title"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta//article-title"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="*" mode="article-meta-doi">
        <xsl:apply-templates select=".//article-meta//article-id[@pub-id-type='doi']" mode="display"></xsl:apply-templates>        
    </xsl:template>
   
    <xsl:template match="article-id[@pub-id-type='doi']" mode="display">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <span>
            <span class="doi"><xsl:value-of select="$link"/></span></span>
            <a class="copyLink" data-clipboard-text="{$link}">
                <span class="sci-ico-link hidden-sm hidden-md"></span> 
                <xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">copy URL</xsl:with-param>
                </xsl:apply-templates>
        </a>
    </xsl:template>
    
    <xsl:template match="article" mode="issue-meta-pub-dates">
        
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='collection']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='collection']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='ppub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='ppub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='ppub-epub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='ppub-epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub-ppub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='epub-ppub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select=".//article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-pub-dates">
        <xsl:apply-templates select=".//article-meta/pub-date[1]" mode="generated-label"></xsl:apply-templates>&#160;
        
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select=".//article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-license">
        <xsl:choose>
            <xsl:when test=".//article-meta//license[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//article-meta//license[@xml:lang=$TEXT_LANG]"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta//license[@xml:lang='en']">
                <xsl:apply-templates select=".//article-meta//license[@xml:lang='en']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta//license[1]"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>        
    </xsl:template>
    
    <xsl:template match="license">
        <xsl:variable name="url">https://licensebuttons.net/l/</xsl:variable>
        <xsl:variable name="icon_path"><xsl:value-of select="substring-after(@xlink:href,'creativecommons.org/licenses/')"/></xsl:variable>
        <xsl:variable name="icon"><xsl:choose>
            <xsl:when test="contains($icon_path,'/deen')"><xsl:value-of select="substring-before($icon_path,'/deen')"/></xsl:when>
            <xsl:otherwise><xsl:value-of select="$icon_path"/></xsl:otherwise>
        </xsl:choose></xsl:variable>
        • <a href="{@xlink:href}" target="_blank"><img src="{$url}{$icon}/80x15.png" alt="Creative Common - {$icon}"/> </a>
    </xsl:template>
       
</xsl:stylesheet>