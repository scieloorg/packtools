<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-fig.xsl"/>

    <xsl:template match="fig | fig-group[@id]">
        <!--
        Cria a miniatura no texto completo, que ao ser clicada mostra a figura
        ampliada
        -->

        <!-- LOCATION OF EXPLICIT THUMBNAIL IMAGE -->
        <xsl:variable name="location">
            <xsl:apply-templates select=".//alternatives" mode="file-location-thumb"/>
        </xsl:variable>

        <xsl:variable name="figid"><xsl:apply-templates select="." mode="figure-id"/></xsl:variable>
        <div class="row fig" id="{$figid}">
            <a name="{$figid}"></a>
            <div class="col-md-4 col-sm-4">
                <!-- manter href="" -->
                <a data-bs-toggle="modal" data-bs-target="#ModalFig{$figid}">
                    <div>
                        <xsl:choose>
                            <xsl:when test="$location != ''">
                                <xsl:attribute name="class">thumbImg</xsl:attribute>
                                <img>
                                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                                    <xsl:apply-templates select="." mode="alt-text"/>
                                </img>
                            </xsl:when>
                            <xsl:otherwise>
                                <xsl:attribute name="class">thumbOff</xsl:attribute>
                            </xsl:otherwise>
                        </xsl:choose>
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <xsl:apply-templates select="." mode="fig-label-caption-thumb"/>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>