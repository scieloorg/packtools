<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">
    
    <xsl:template match="fig-group">
        <xsl:choose>
            <xsl:when test="fig[@xml:lang=$TEXT_LANG]">
                <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]"></xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="fig[1]"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="fig[graphic]">
        <xsl:variable name="location"><xsl:apply-templates select="." mode="file-location"></xsl:apply-templates></xsl:variable>
        <div class="row fig" id="{@id}">
            <a name="{@id}"></a>
            <div class="col-md-4 col-sm-4">
                <a href="" data-toggle="modal" data-target="#ModalFig{@id}">
                    <div class="thumb" style="background-image: url({$location});">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="fig-group" mode="file-location">
        <xsl:apply-templates select="fig[graphic]" mode="file-location"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig[disp-formula and not(graphic)]">
        <div class="row fig" id="{@id}">
            <a name="{@id}"></a>
            <div class="col-md-4 col-sm-4">
                <xsl:apply-templates select="disp-formula"></xsl:apply-templates>
            </div>
            <div class="col-md-8 col-sm-8">
                <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="*[graphic]" mode="file-location"><xsl:apply-templates select="graphic/@xlink:href"/></xsl:template>
    
    <xsl:template match="fig-group" mode="label-caption">
        <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="label-caption"></xsl:apply-templates>
    </xsl:template>
      
</xsl:stylesheet>