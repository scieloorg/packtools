<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <!--xsl:include href="../v2.0/article-text-media.xsl"/-->

    <xsl:template match="media">
        <a target="_blank">
            <xsl:attribute name="href"><xsl:value-of select="@xlink:href"/></xsl:attribute>
            <xsl:apply-templates select="*|text()"/>
        </a>
    </xsl:template>

    <xsl:template match="sec/media">
        <p>
            <xsl:apply-templates select="*|text()" mode="sec-media"/>
        </p>
    </xsl:template>

    <xsl:template match="media/label" mode="sec-media">
        <xsl:apply-templates select="."/><br/>
    </xsl:template>

    <xsl:template match="media/caption" mode="sec-media">
        <a target="_blank" href="{../@xlink:href}" alt="{../alt-text}">
            <xsl:apply-templates select="."/>
        </a>
    </xsl:template>
</xsl:stylesheet>