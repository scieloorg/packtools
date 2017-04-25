<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" 
    version="1.0">
    <xsl:template match="inline-supplementary-material">
        <a target="_blank" href="{@xlink:href}">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>
    </xsl:template>
    <xsl:template match="supplementary-material">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
</xsl:stylesheet>