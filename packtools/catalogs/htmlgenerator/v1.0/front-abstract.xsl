<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="front-abstract">
        <xsl:apply-templates select="." mode="lang-abstract"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="abstract | trans-abstract" mode="attribute-data-anchor">
        <!-- FIXME: data-anchor Resumo -->
        <xsl:attribute name="data-anchor">Resumo</xsl:attribute>
    </xsl:template>
    <xsl:template match="abstract | trans-abstract">
        <xsl:variable name="lang" select="@xml:lang"/>
        <div class="articleSection">
            <xsl:apply-templates select="." mode="attribute-data-anchor"></xsl:apply-templates>
            <!-- FIXME -->
            <a name="articleSection0"></a>
            <xsl:apply-templates select="*"></xsl:apply-templates>
            <xsl:apply-templates select="../kwd-group[@xml:lang=$lang]" mode="keywords"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="abstract/title | trans-abstract/title">
        <div class="row">
            <a name="resumo-heading-01"></a>
            <div class="col-md-8 col-sm-8">
                <h1><xsl:apply-templates></xsl:apply-templates></h1>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="abstract/sec/title | trans-abstract/sec/title">
        <div class="row">
            <a name="resumo-heading-{position()}"></a>
            <div class="col-md-8 col-sm-8">
                <h2><xsl:apply-templates></xsl:apply-templates></h2>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="abstract//p | trans-abstract//p">
        <div class="row paragraph">
            <div class="col-md-8 col-sm-8">
                <p>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates></p>
            </div>
            <div class="col-md-4 col-sm-4">
                
            </div>
        </div>
    </xsl:template>
    <xsl:template match="kwd-group"></xsl:template>
    <xsl:template match="kwd-group" mode="kwd-group-title">
        <!-- FIXME: Keywords -->
        Keywords
    </xsl:template>
    <xsl:template match="kwd-group" mode="keywords">
        <div class="row paragraph">
            <div class="col-md-8 col-sm-9">
                <p><strong><xsl:apply-templates select="." mode="kwd-group-title"></xsl:apply-templates></strong>: 
                    <xsl:apply-templates select="*"></xsl:apply-templates></p>
            </div>
            <div class="col-md-4 col-sm-2">
                
            </div>
        </div>
    </xsl:template>
    <xsl:template match="kwd"><xsl:apply-templates select="*|text()"></xsl:apply-templates><xsl:if test="position()!=last()">; </xsl:if>
    </xsl:template>
</xsl:stylesheet>