<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="fig[graphic]|fig-group">
        <xsl:variable name="location"><xsl:apply-templates select="." mode="fig-file-location"></xsl:apply-templates></xsl:variable>
        <div class="articleSection">
        <div class="row fig" id="{@id}">
            <a name="{@id}"></a>
            <div class="col-md-3 col-sm-4">
                <div class="thumb" style="background-image: url({$location});">Thumbnail</div>
                <div class="figInfo">
                    <span class="glyphBtn zoom"></span> Passe o mouse sobre a figura para visualizar
                </div>
            </div>
            <div class="col-md-9 col-sm-8">
                <xsl:apply-templates select="." mode="fig-label-caption"></xsl:apply-templates>
            </div>
            <div class="preview col-md-offset-3 col-md-9" style="display: none;"><img src="{$location}">
                <xsl:attribute name="alt"><xsl:apply-templates select="." mode="fig-label"></xsl:apply-templates></xsl:attribute>
            </img></div>
        </div>
        </div>
    </xsl:template>
    <xsl:template match="fig-group" mode="fig-file-location">
        <xsl:apply-templates select="fig[graphic]" mode="fig-file-location"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="fig[graphic]" mode="fig-file-location"><xsl:value-of select="graphic/@xlink:href"/></xsl:template>
    <xsl:template match="fig-group" mode="fig-label-caption">
        <xsl:apply-templates select="fig[@xml:lang=$PAGE_LANG]"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="fig" mode="fig-label-caption">
        <xsl:apply-templates select="label|caption"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="fig-group" mode="fig-label">
        <xsl:apply-templates select="fig[@xml:lang=$PAGE_LANG]"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="fig" mode="fig-label">
        <xsl:apply-templates select="label"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="fig/caption">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="fig/caption/title">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>