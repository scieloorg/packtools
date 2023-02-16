<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/config-labels.xsl"/>

    <xsl:template match="label">
        <xsl:variable name="text"><xsl:apply-templates select=".//text()"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="contains('123456789',substring(normalize-space($text),1,1))">
                <sup><strong><xsl:apply-templates select="*|text()"/></strong></sup>
            </xsl:when>
            <xsl:otherwise>
                <strong><xsl:apply-templates select="*|text()"/></strong>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="label[sup]">
        <strong><xsl:apply-templates select="*|text()"/></strong>
    </xsl:template>
</xsl:stylesheet>