<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="article-meta-abstract">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]/*/abstract" mode="layout"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-meta//abstract|.//article-meta//trans-abstract" mode="layout"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="abstract | trans-abstract" mode="layout">
        <xsl:variable name="lang" select="@xml:lang"/>
        
        <div class="articleSection">
            <xsl:if test="@xml:lang='ar'">
                <xsl:attribute name="dir">rtl</xsl:attribute>
            </xsl:if>
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
            <a name="articleSection{position()-1}"></a>
            <div class="row">
                <a name="resumo-heading-01"></a>
                <div class="col-md-8 col-sm-8">
                    <h1><xsl:apply-templates select="." mode="title"></xsl:apply-templates></h1>
                </div>
            </div>
            <xsl:apply-templates select="*[name()!='title']"/>
            <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"></xsl:apply-templates>
            <xsl:if test="not(../kwd-group[@xml:lang=$lang])">
                <xsl:apply-templates select="../kwd-group[1]" mode="keywords"/>
            </xsl:if>
        </div>
    </xsl:template>
    
    <xsl:template match="abstract/title | trans-abstract/title">
        <xsl:apply-templates select="*|text()"/>
    </xsl:template>
    
    <xsl:template match="abstract/sec/title | trans-abstract/sec/title">
        <h2><xsl:apply-templates select="*|text()"/></h2>
    </xsl:template>
    
    <xsl:template match="kwd-group"></xsl:template>
    <xsl:template match="kwd-group" mode="keywords">
        <p><xsl:if test="not(title)"><strong><xsl:apply-templates select="." mode="generated-label"></xsl:apply-templates>: </strong></xsl:if>
            <xsl:apply-templates select="*"/></p>
    </xsl:template>
    
    <xsl:template match="kwd-group/title">
        <strong><xsl:value-of select="."/></strong> 
    </xsl:template>
    
    <xsl:template match="kwd"><xsl:apply-templates select="*|text()"></xsl:apply-templates><xsl:if test="position()!=last()">; </xsl:if>
    </xsl:template>
    
    
      
</xsl:stylesheet>