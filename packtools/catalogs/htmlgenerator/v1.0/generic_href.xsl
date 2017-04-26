<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="ext-link">
        <a href="{@xlink:href}" target="_blank"><xsl:apply-templates select="*|text()"></xsl:apply-templates></a>
    </xsl:template>
    <xsl:template match="email">
        <a href="mailto:{.}"><xsl:value-of select="."/></a>
    </xsl:template>
    <xsl:template match="graphic">
        <img>
            <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
        </img>
    </xsl:template>
    
    <xsl:template match="xref">
        <a href="#{@rid}" class="goto"><xsl:apply-templates></xsl:apply-templates></a>
    </xsl:template>
    
    <!-- -->
    <xsl:template match="graphic/@xlink:href">
        <xsl:attribute name="src"><xsl:apply-templates select="." mode="generic-href-content"></xsl:apply-templates></xsl:attribute>
    </xsl:template>
    <xsl:template match="graphic/@xlink:href" mode="generic-href-content">
        <xsl:variable name="last4char"><xsl:value-of select="substring(.,string-length(.)-3)"/></xsl:variable>
        <xsl:variable name="name"><xsl:choose>
            <xsl:when test="$last4char='tiff'"><xsl:value-of select="substring-before(.,'.tiff')"/>.jpg</xsl:when>
            <xsl:when test="$last4char='.tif'"><xsl:value-of select="substring-before(.,'.tif')"/>.jpg</xsl:when>
            <xsl:when test="substring($last4char,1,1)='.'"><xsl:value-of select="."/></xsl:when>
            <xsl:otherwise><xsl:value-of select="."/>.jpg</xsl:otherwise>
        </xsl:choose></xsl:variable>
        <xsl:value-of select="concat($IMAGES_PATH,$name)"/>
    </xsl:template>
    

</xsl:stylesheet>
