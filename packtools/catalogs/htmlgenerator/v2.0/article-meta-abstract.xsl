<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="article-meta-abstract">
        <xsl:choose>
            <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//abstract">
                <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]" mode="article-meta-abstract"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="front/article-meta//abstract">
                <xsl:if test="$q_abstract_title=0">
                    <xsl:apply-templates select="." mode="abstract-anchor"></xsl:apply-templates>
                </xsl:if>
                <xsl:apply-templates select="front/article-meta//abstract|front/article-meta//trans-abstract" mode="layout"></xsl:apply-templates>
            </xsl:when>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="article" mode="article-meta-no-abstract-keywords">
        <xsl:if test="not(.//abstract)">
            <xsl:choose>
                <xsl:when test=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//kwd-group">
                    <xsl:apply-templates select=".//sub-article[@article-type='translation' and @xml:lang=$TEXT_LANG]//kwd-group" mode="keywords"/>
                </xsl:when>
                <xsl:when test="front/article-meta//kwd-group">
                    <xsl:apply-templates select="front/article-meta//kwd-group" mode="keywords"/>
                </xsl:when>
            </xsl:choose>
        </xsl:if>
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
                <xsl:with-param name="text"><xsl:choose>
                    <xsl:when test="count(.//abstract)+count(.//trans-abstract) &gt; 1">Abstracts</xsl:when>
                    <xsl:otherwise>Abstract</xsl:otherwise>
                </xsl:choose></xsl:with-param>
            </xsl:apply-templates></xsl:attribute>
            <h1 class="articleSectionTitle"><xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text"><xsl:choose>
                    <xsl:when test="count(.//abstract)+count(.//trans-abstract) &gt; 1">Abstracts</xsl:when>
                    <xsl:otherwise>Abstract</xsl:otherwise>
                </xsl:choose></xsl:with-param>
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
        <div>
            <xsl:if test="title">
                <xsl:attribute name="class">articleSection</xsl:attribute>
                <xsl:attribute name="data-anchor"><xsl:apply-templates select="." mode="title"/></xsl:attribute>
            </xsl:if>
            <xsl:if test="@xml:lang='ar'">
                <xsl:attribute name="dir">rtl</xsl:attribute>
            </xsl:if>
                
            <xsl:if test="title">
                <h1>
                    <xsl:attribute name="class">articleSectionTitle</xsl:attribute>
                    <xsl:apply-templates select="." mode="title"></xsl:apply-templates>
                </h1>
            </xsl:if>
            <xsl:apply-templates select="*[name()!='title']"/>
            <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"></xsl:apply-templates>
            <xsl:if test="not(../kwd-group[@xml:lang=$lang])">
                <xsl:apply-templates select="../kwd-group[1]" mode="keywords"/>
            </xsl:if>
        </div>
        <xsl:if test="not(title)">
        <hr/>
        </xsl:if>
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
        <strong><xsl:value-of select="."/></strong><br/>
    </xsl:template>
    
    <xsl:template match="kwd"><xsl:apply-templates select="*|text()"></xsl:apply-templates><xsl:if test="position()!=last()">; </xsl:if>
    </xsl:template>
    
    
      
</xsl:stylesheet>