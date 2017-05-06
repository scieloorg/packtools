<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="article-meta-abstract">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//abstract">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="article-meta-abstract"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test=".//article-meta//abstract">
                <xsl:if test="$q_abstract_title=0">
                    <xsl:apply-templates select="." mode="abstract-anchor"></xsl:apply-templates>
                </xsl:if>
                <xsl:apply-templates select=".//article-meta//abstract|.//article-meta//trans-abstract" mode="layout"></xsl:apply-templates>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type='translation']" mode="article-meta-abstract">
        <xsl:if test="$q_abstract_title=0">
            <xsl:apply-templates select="." mode="abstract-anchor"></xsl:apply-templates>
        </xsl:if>
        <xsl:apply-templates select=".//abstract|.//trans-abstract" mode="layout"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="*" mode="abstract-anchor">
        <div class="articleSection">
            <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">Abstract</xsl:with-param>
            </xsl:apply-templates></xsl:attribute>
            <a name="articleSection0"></a>
            <h1><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text">Abstract</xsl:with-param>
            </xsl:apply-templates></h1>
        </div>
    </xsl:template>
    
    <xsl:template match="*[contains(name(),'abstract')]" mode="index">
        <xsl:param name="lang"/>
        <xsl:if test="normalize-space(@xml:lang)=normalize-space($lang)"><xsl:value-of select="position()"/></xsl:if>
    </xsl:template>
    
    <xsl:template match="abstract | trans-abstract" mode="layout">
        <xsl:variable name="lang" select="@xml:lang"/>
        
        <xsl:variable name="index"><xsl:apply-templates select="..//*[contains(name(),'abstract') and title]" mode="index"><xsl:with-param name="lang" select="$lang"></xsl:with-param></xsl:apply-templates></xsl:variable>
        <xsl:if test="$q_abstract_title &gt; 0">
           <a name="articleSection{$index - 1}"></a>
        </xsl:if>
        
        <div class="articleSection">
            <xsl:if test="@xml:lang='ar'">
                <xsl:attribute name="dir">rtl</xsl:attribute>
            </xsl:if>
            <xsl:if test="title">
                <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
            </xsl:if>
            <div class="row">
                <a name="resumo-heading-01"></a>
                <div class="col-md-8 col-sm-8">
                    <xsl:if test="title">
                        <h1><xsl:apply-templates select="." mode="title"></xsl:apply-templates></h1>
                    </xsl:if>
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
        <p><xsl:apply-templates select="*"/></p>
    </xsl:template>
    
    <xsl:template match="kwd-group/title">
        <strong><xsl:value-of select="."/></strong> 
    </xsl:template>
    
    <xsl:template match="kwd"><xsl:apply-templates select="*|text()"></xsl:apply-templates><xsl:if test="position()!=last()">; </xsl:if>
    </xsl:template>
    
    
      
</xsl:stylesheet>