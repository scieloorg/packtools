<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-sub-article.xsl"/>

    <xsl:template match="article" mode="article-text-sub-articles">
        <xsl:choose>
            <xsl:when test="sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']">
                <!-- apply sub-article[@article-type='translation']/sub-article (not translation) -->
                <xsl:apply-templates select="sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']" mode="sub-article-not-translation">
                    <xsl:with-param name="reflist" select="sub-article[@article-type!='translation']//ref-list"/>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <!-- article/sub-article[@article-type!='translation'] -->
                <!-- sub-article não necessariamente deve corresponder ao idioma do TEXT_LANG ex.: "O corpo da dança como arena de valores e o cronotopo do teatro exercício de análise" tem peer-review em espanhol e português -->
                <xsl:apply-templates select="response[@xml:lang=$TEXT_LANG] | sub-article[@article-type!='translation']" mode="sub-article-not-translation"/>        
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="response | sub-article[@article-type!='translation']" mode="sub-article-not-translation-components">
        <xsl:apply-templates select="front|front-stub" mode="sub-article-title"/>
        <xsl:apply-templates select="." mode="contrib-group"/>
        <xsl:apply-templates select="." mode="text-body"/>
        <xsl:apply-templates select="back" mode="back"/>
    </xsl:template>
 
    <xsl:template match="front|front-stub" mode="sub-article-title">
        <xsl:choose>
            <xsl:when test="title-group">
                <xsl:apply-templates select=".//article-title" mode="sub-article-title"/>
            </xsl:when>
            <xsl:when test=".//subject-group">
                <xsl:apply-templates select=".//subject" mode="sub-article-title"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select=".//article-title" mode="sub-article-title"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
 
    <xsl:template match="article-title|subject" mode="sub-article-title">
        <!-- Apresentação padrão de um compontente do Bloco do sub-article (not translation) ou response -->
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div class="articleSection">
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select="*|text()"/>
            </xsl:attribute> 
        </div>
        <h2 class="h5"><xsl:apply-templates select="*|text()"/></h2>
    </xsl:template>

</xsl:stylesheet>