<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <xsl:template match="article" mode="article-meta-title">
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG]/*/title-group/article-title"></xsl:apply-templates>
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
        <xsl:apply-templates select=".//article-meta//article-id[@pub-id-type='doi']"></xsl:apply-templates>        
    </xsl:template>
   
    <xsl:template match="article-id[@pub-id-type='doi']">
        <xsl:variable name="link">https://doi.org/<xsl:value-of select="."/></xsl:variable>
        <span class="doi"><a href="{$link}"><xsl:value-of select="$link"/></a></span>
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
        <xsl:apply-templates select=".//article-meta/pub-date[1]" mode="label"></xsl:apply-templates>&#160;
        
        <xsl:choose>
            <xsl:when test=".//article-meta/pub-date[@pub-type='epub']">
                <xsl:apply-templates  select=".//article-meta/pub-date[@pub-type='epub']"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates  select=".//article-meta/pub-date"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article-meta/pub-date">
        <xsl:choose>
            <xsl:when test="season">
                <xsl:apply-templates select="season"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="day">
                <xsl:apply-templates select="month" mode="label"></xsl:apply-templates>
                <xsl:text> </xsl:text>
                <xsl:apply-templates select="day"></xsl:apply-templates>, 
            </xsl:when>
            <xsl:otherwise><xsl:apply-templates select="month" mode="label"></xsl:apply-templates></xsl:otherwise>
        </xsl:choose>
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="year"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-license">
        <!-- FIXME -->
        <xsl:apply-templates select=".//article-meta//license[1]/@xlink:href"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="license/@xlink:href">
        <xsl:value-of select="."/>
    </xsl:template>
    
    
</xsl:stylesheet>