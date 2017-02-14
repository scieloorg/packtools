<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="aff">
            <xsl:choose>
                <xsl:when test="institution[@content-type='original']">
                    <xsl:apply-templates select="institution[@content-type='original']"></xsl:apply-templates>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="*[name()!='label']|text()"></xsl:apply-templates>
                </xsl:otherwise>
            </xsl:choose>
    </xsl:template>
     
</xsl:stylesheet>