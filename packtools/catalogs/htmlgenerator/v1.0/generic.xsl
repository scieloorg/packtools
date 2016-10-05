<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="*">
        <xsl:element name="{name()}">
            <xsl:apply-templates select="@*|*|text()"/>
        </xsl:element>
    </xsl:template>
    <xsl:template match="text()">
        <xsl:value-of select="."/>
    </xsl:template>
    <xsl:template match="@*">
        <xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
    </xsl:template>
    
    <xsl:template match="bold">
        <b><xsl:apply-templates></xsl:apply-templates></b>
    </xsl:template>
    <xsl:template match="italic">
        <i><xsl:apply-templates></xsl:apply-templates></i>
    </xsl:template>
    
    <xsl:template match="*[not(sup)]/xref">
        <sup class="xref big"><xsl:apply-templates></xsl:apply-templates></sup>
    </xsl:template>
    <xsl:template match="sup[xref]">
        <sup class="xref big"><xsl:apply-templates></xsl:apply-templates></sup>
    </xsl:template>
    <xsl:template match="email">
        <a href="mailto:{.}"><xsl:value-of select="."/></a>
    </xsl:template>
</xsl:stylesheet>
