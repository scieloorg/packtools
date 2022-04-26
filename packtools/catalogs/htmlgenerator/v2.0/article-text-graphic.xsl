<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="graphic | inline-graphic">
        <xsl:variable name="location"><xsl:apply-templates select="@xlink:href"></xsl:apply-templates></xsl:variable>
        <xsl:variable name="s"><xsl:value-of select="substring($location,string-length($location)-3)"/></xsl:variable>
        <xsl:variable name="ext"><xsl:if test="contains($s,'.')">.<xsl:value-of select="substring-after($s,'.')"/></xsl:if></xsl:variable>

        <xsl:choose>
            <xsl:when test="$ext='.svg'">
                <a>
                    <xsl:attribute name="href"><xsl:value-of select="$location"/></xsl:attribute>
                    <object type="image/svg+xml">
                        <xsl:attribute name="style">max-width:100%</xsl:attribute>
                        <xsl:attribute name="data"><xsl:value-of select="$location"/></xsl:attribute>
                    </object>
                </a>
            </xsl:when>
            <xsl:otherwise>
                <a>
                    <xsl:attribute name="href"><xsl:value-of select="$location"/></xsl:attribute>
                    <img>
                        <xsl:attribute name="style">max-width:100%</xsl:attribute>
                        <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                    </img>
                </a>
            </xsl:otherwise>
        </xsl:choose>
        <!--
        <xsl:comment><xsl:value-of select="$s"/> </xsl:comment>
        -->
    </xsl:template>

    <xsl:template match="graphic | inline-graphic" mode="file-location"><xsl:apply-templates select="@xlink:href"/></xsl:template>

    <xsl:template match="graphic | inline-graphic" mode="file-location-thumb"><xsl:apply-templates select="@xlink:href"/></xsl:template>

    <xsl:template match="graphic/@xlink:href | inline-graphic/@xlink:href">
        <xsl:variable name="s"><xsl:value-of select="substring(.,string-length(.)-4)"/></xsl:variable>
        <xsl:variable name="ext"><xsl:if test="contains($s,'.')">.<xsl:value-of select="substring-after($s,'.')"/></xsl:if></xsl:variable>
        <xsl:choose>
            <xsl:when test="$ext='.tif' or $ext='.tiff'"><xsl:value-of select="substring-before(.,$ext)"/>.jpg</xsl:when>
            <xsl:when test="$ext=''"><xsl:value-of select="."/>.jpg</xsl:when>
            <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="@xlink:href" mode="original-file-location"><xsl:apply-templates select="." mode="fix-original-file-location"/></xsl:template>

    <xsl:template match="*" mode="original-file-location">
        <xsl:choose>
            <xsl:when test="*">
                <xsl:apply-templates select="*" mode="original-file-location"/>
            </xsl:when>
            <xsl:when test="@xlink:href!='' and not(@specific-use)">
                <xsl:apply-templates select="@xlink:href" mode="original-file-location"/>
            </xsl:when>
            <xsl:otherwise>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="@xlink:href" mode="fix-original-file-location">
        <xsl:variable name="tail"><xsl:value-of select="substring(.,string-length(.)-5)"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="contains($tail, '.')">
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="."/>.jpg</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
