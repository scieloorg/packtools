<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

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
    
    <xsl:template match="sub-article[@article-type='translation']" mode="sub-article-not-translation">
        <xsl:param name="reflist"/>
        <xsl:apply-templates select="sub-article[@article-type!='translation']" mode="sub-article-not-translation">
            <xsl:with-param name="reflist" select="$reflist"/>
        </xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type!='translation'] | response" mode="sub-article-not-translation">
        <xsl:param name="reflist"/>

        <!-- Bloco do sub-article (not translation) ou response -->
        <xsl:apply-templates select="." mode="sub-article-not-translation-components"/>
        <xsl:if test="$reflist">
            <xsl:apply-templates select="$reflist"/>
        </xsl:if>
        <xsl:apply-templates select="." mode="generic-history"></xsl:apply-templates>    
    </xsl:template>
    
    <xsl:template match="sub-article[@article-type!='translation'] | response" mode="sub-article-not-translation-components">
        <!-- Componentes do Bloco do sub-article (not translation) ou response -->
        <xsl:apply-templates select="*|text()" mode="sub-article-not-translation-component"/>
    </xsl:template>

    <xsl:template match="*" mode="sub-article-not-translation-component">
        <!-- Apresentação padrão de um compontente do Bloco do sub-article (not translation) ou response -->
        <xsl:apply-templates select="."/>
    </xsl:template>

    <xsl:template match="front-stub" mode="sub-article-not-translation-component">
        <xsl:apply-templates select="title-group" mode="sub-article-not-translation-component"/>
        <xsl:apply-templates select="contrib-group" mode="sub-article-not-translation-component"/>
    </xsl:template>

    <xsl:template match="title-group" mode="sub-article-not-translation-component">
        <!-- Apresentação padrão de um compontente do Bloco do sub-article (not translation) ou response -->
        <!-- manter pareado class="articleSection" e data-anchor="nome da seção no menu esquerdo" -->
        <div class="articleSection">
            <xsl:attribute name="data-anchor">
                <xsl:apply-templates select=".//article-title"/>
            </xsl:attribute> 
        </div>
        <xsl:apply-templates select="*" mode="sub-article-not-translation-component"/>
    </xsl:template>

    <xsl:template match="sub-article[@article-type!='translation']/back | response/back">
        <xsl:apply-templates select="*" mode="back-section"></xsl:apply-templates>
    </xsl:template>

</xsl:stylesheet>