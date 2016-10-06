<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">

    <xsl:template match="person-group">
        <xsl:apply-templates select="name"></xsl:apply-templates><xsl:choose>
            <xsl:when test="position()=last()">. </xsl:when>
            <xsl:otherwise>; </xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    <xsl:template match="person-group/name">
        <xsl:apply-templates select="surname"></xsl:apply-templates>, <xsl:apply-templates select="given-names"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>