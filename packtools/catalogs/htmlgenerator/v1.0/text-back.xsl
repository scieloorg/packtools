<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="text-back">
        <xsl:apply-templates select="./back/*" mode="text-back"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="back/*" mode="text-back">
        <div class="articleSection" data-anchor="Texto">
            <xsl:apply-templates select="."></xsl:apply-templates>
        </div>
    </xsl:template>
</xsl:stylesheet>