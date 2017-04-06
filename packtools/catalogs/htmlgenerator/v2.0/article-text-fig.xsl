<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="fig[graphic]|fig-group">
        <xsl:variable name="location"><xsl:apply-templates select="." mode="fig-file-location"></xsl:apply-templates></xsl:variable>
        <div class="row fig" id="{@id}">
            <a name="{@id}"></a>
            <div class="col-md-4">
                <a href="" data-toggle="modal" data-target="#ModalFig{@id}">
                    <div class="thumb" style="background-image: url({$location});">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8">
                <strong><xsl:value-of select="label"/></strong><br/>
                <xsl:apply-templates select="caption"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="fig-group" mode="fig-file-location">
        <xsl:apply-templates select="fig[graphic]" mode="fig-file-location"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig[graphic]" mode="fig-file-location"><xsl:apply-templates select="graphic/@xlink:href" mode="generic-href-content"/></xsl:template>
    
    <xsl:template match="fig-group" mode="fig-label-caption">
        <xsl:apply-templates select="fig[@xml:lang=$ARTICLE_LANG]"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig" mode="fig-label-caption">
        <xsl:apply-templates select="label|caption"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig-group" mode="fig-label">
        <xsl:apply-templates select="fig[@xml:lang=$ARTICLE_LANG]"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig" mode="fig-label">
        <xsl:apply-templates select="label"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig/caption">
        <xsl:text> </xsl:text>
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig/caption/title">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>