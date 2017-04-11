<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="graphic | inline-graphic">
        <xsl:variable name="location"><xsl:apply-templates select="@xlink:href"></xsl:apply-templates></xsl:variable>
        <xsl:variable name="s"><xsl:value-of select="substring(.,string-length(.)-4)"/></xsl:variable>
        <xsl:variable name="ext"><xsl:if test="contains($s,'.')">.<xsl:value-of select="substring-after($s,'.')"/></xsl:if></xsl:variable>
        <xsl:choose>
            <xsl:when test="$ext='.svg'">
                <object type="image/svg+xml">
                    <xsl:attribute name="data"><xsl:value-of select="$location"/></xsl:attribute>
                </object>
            </xsl:when>
            <xsl:otherwise>
                <img>
                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                </img>
            </xsl:otherwise>
        </xsl:choose>      
        <xsl:comment> <xsl:value-of select="$s"> </xsl:value-of></xsl:comment>
    </xsl:template>

    <xsl:template match="@xlink:href">
        <xsl:variable name="s"><xsl:value-of select="substring(.,string-length(.)-4)"/></xsl:variable>
        <xsl:variable name="ext"><xsl:if test="contains($s,'.')">.<xsl:value-of select="substring-after($s,'.')"/></xsl:if></xsl:variable>
        <xsl:choose>
            <xsl:when test="$ext='.tif' or $ext='.tiff'"><xsl:value-of select="substring-before(.,$ext)"/>.jpg</xsl:when>
            <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        </xsl:choose>      
    </xsl:template>
</xsl:stylesheet>
