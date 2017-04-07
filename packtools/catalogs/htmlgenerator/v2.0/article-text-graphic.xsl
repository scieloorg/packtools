<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="graphic">
        <xsl:choose>
            <xsl:when test="substring(@xlink:href,string-length(@xlink:href)-2)='svg'">
                <object type="image/svg+xml">
                    <xsl:attribute name="data"><xsl:value-of select="@xlink:href"/></xsl:attribute>
                </object>
            </xsl:when>
            <xsl:otherwise>
                <img>
                    <xsl:attribute name="src"><xsl:value-of select="@xlink:href"/></xsl:attribute>
                </img>
            </xsl:otherwise>
        </xsl:choose>       
    </xsl:template>

</xsl:stylesheet>
