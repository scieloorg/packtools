<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="bold">
        <b><xsl:apply-templates></xsl:apply-templates></b>
    </xsl:template>
    <xsl:template match="italic">
        <i><xsl:apply-templates></xsl:apply-templates></i>
    </xsl:template>
    <xsl:template match="break">
        <br/>
    </xsl:template>
    <xsl:template match="*[not(sup)]/xref">
        <sup><xsl:apply-templates></xsl:apply-templates></sup>
            
    </xsl:template>
    <!--xsl:template match="sup[xref]">
        <sup class="xref big"></sup>
        <xsl:apply-templates></xsl:apply-templates>
    </xsl:template-->
</xsl:stylesheet>