<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="lang-article-title">
        <xsl:apply-templates select=".//article-meta//article-title"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="issn/@pub-type">
        <!-- FIXME -->
        <xsl:value-of select="."/> 
    </xsl:template>
    
    <xsl:template match="month" mode="lang-month">
        <xsl:choose>
            <xsl:when test="$ARTICLE_LANG='es'">
                <xsl:apply-templates select="." mode="lang-es"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="$ARTICLE_LANG='pt'">
                <xsl:apply-templates select="." mode="lang-pt"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="lang-en"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="month" mode="lang-pt">
        <xsl:choose>
            <xsl:when test="number(.)=1">Jan</xsl:when>
            <xsl:when test="number(.)=2">Fev</xsl:when>
            <xsl:when test="number(.)=3">Mar</xsl:when>
            <xsl:when test="number(.)=4">Abr</xsl:when>
            <xsl:when test="number(.)=5">Maio</xsl:when>
            <xsl:when test="number(.)=6">Jun</xsl:when>
            <xsl:when test="number(.)=7">Jul</xsl:when>
            <xsl:when test="number(.)=8">Ago</xsl:when>
            <xsl:when test="number(.)=9">Set</xsl:when>
            <xsl:when test="number(.)=10">Out</xsl:when>
            <xsl:when test="number(.)=11">Nov</xsl:when>
            <xsl:when test="number(.)=12">Dez</xsl:when>           
        </xsl:choose>
    </xsl:template>
    <xsl:template match="month" mode="lang-es">
        <xsl:choose>
            <xsl:when test="number(.)=1">Ene</xsl:when>
            <xsl:when test="number(.)=2">Feb</xsl:when>
            <xsl:when test="number(.)=3">Mar</xsl:when>
            <xsl:when test="number(.)=4">Abr</xsl:when>
            <xsl:when test="number(.)=5">Mayo</xsl:when>
            <xsl:when test="number(.)=6">Jun</xsl:when>
            <xsl:when test="number(.)=7">Jul</xsl:when>
            <xsl:when test="number(.)=8">Ago</xsl:when>
            <xsl:when test="number(.)=9">Set</xsl:when>
            <xsl:when test="number(.)=10">Oct</xsl:when>
            <xsl:when test="number(.)=11">Nov</xsl:when>
            <xsl:when test="number(.)=12">Dic</xsl:when>           
        </xsl:choose>
    </xsl:template>
    <xsl:template match="month" mode="lang-en">
        <xsl:choose>
            <xsl:when test="number(.)=1">Jan</xsl:when>
            <xsl:when test="number(.)=2">Feb</xsl:when>
            <xsl:when test="number(.)=3">Mar</xsl:when>
            <xsl:when test="number(.)=4">Apr</xsl:when>
            <xsl:when test="number(.)=5">May</xsl:when>
            <xsl:when test="number(.)=6">June</xsl:when>
            <xsl:when test="number(.)=7">July</xsl:when>
            <xsl:when test="number(.)=8">Aug</xsl:when>
            <xsl:when test="number(.)=9">Sep</xsl:when>
            <xsl:when test="number(.)=10">Oct</xsl:when>
            <xsl:when test="number(.)=11">Nov</xsl:when>
            <xsl:when test="number(.)=12">Dec</xsl:when>           
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="lang-license">
        <xsl:choose>
            <xsl:when test="//article-meta//license[@xml:lang=$ARTICLE_LANG]">
                <xsl:apply-templates select="//article-meta//license[@xml:lang=$ARTICLE_LANG]"></xsl:apply-templates>
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