<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">

    <xsl:template match="fig[@id] | fig-group[@id]">
        <!--
        Cria a miniatura no texto completo, que ao ser clicada mostra a figura
        ampliada
        -->
        <xsl:variable name="location">
            <xsl:apply-templates select="alternatives | graphic" mode="file-location-thumb"/>
        </xsl:variable>
        <xsl:variable name="figid"><xsl:apply-templates select="." mode="figure-id"/></xsl:variable>
        <div class="row fig" id="{$figid}">
            <a name="{$figid}"></a>
            <div class="col-md-4 col-sm-4">
                <a href="" data-toggle="modal" data-target="#ModalFig{$figid}">
                    <xsl:attribute name="href"><xsl:value-of select="$location"/></xsl:attribute>
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location != ''">
                                <xsl:attribute name="class">thumbImg</xsl:attribute>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="class">thumbOff</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <img>
                            <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                        </img>
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <xsl:apply-templates select="." mode="fig-label-caption-thumb"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="fig-group[@id]" mode="fig-label-caption-thumb">
        <xsl:apply-templates select="fig" mode="fig-label-caption-thumb"/>
    </xsl:template>

    <xsl:template match="fig" mode="fig-label-caption-thumb">
        <xsl:apply-templates select="." mode="label-caption-thumb"/><br/>
    </xsl:template>

    <xsl:template match="fig[@id] | fig-group[@id]" mode="figure-id">
        <xsl:value-of select="@id"/>
    </xsl:template>

</xsl:stylesheet>
