<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="article" mode="article-text-sub-articles">
        <xsl:apply-templates select="response[@xml:lang=$TEXT_LANG] | sub-article[@xml:lang=$TEXT_LANG and @article-type!='translation']"></xsl:apply-templates>
    </xsl:template>
    
    
    <xsl:template match="sub-article[@article-type!='translation']//subject | response//subject">
    </xsl:template>
    
    
    <xsl:template match="sub-article[@article-type!='translation']//subject | response//subject">
        <h1 class="articleSectionTitle"><xsl:apply-templates select="*|text()"></xsl:apply-templates></h1>
     </xsl:template>
    
    <xsl:template match="sub-article[@article-type!='translation']//article-title | response//article-title">
        <h1 class="article-title">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </h1>
    </xsl:template>
    <xsl:template match="sub-article[@article-type!='translation']//trans-title | response//trans-title">
        <h1 class="article-title">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </h1>
    </xsl:template>
    <xsl:template match="sub-article[@article-type!='translation']//aff | response//aff">
    </xsl:template>
    <xsl:template match="sub-article[@article-type!='translation']//history | response//history">
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type!='translation'] | response">
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text" select="concat(@article-type,@response-type)"/>
            </xsl:apply-templates></xsl:attribute> 
        </div>
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        <xsl:apply-templates select="." mode="generic-history"></xsl:apply-templates>    
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type!='translation']/back | response/back">
        <xsl:apply-templates select="*" mode="back-section"></xsl:apply-templates>
    </xsl:template>

</xsl:stylesheet>