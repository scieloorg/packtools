<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    version="1.0" >
    <xsl:template match="bio//fig" mode="modal"></xsl:template>
    
    <xsl:template match="bio" mode="bio-picture">
        <xsl:apply-templates select=".//fig" mode="bio-picture"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="bio//fig" mode="bio-picture">
        <xsl:apply-templates select=".//graphic"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="bio//fig">
    </xsl:template>
    
    <xsl:template match="back/bio" mode="back-section-content">
        <div>
            <xsl:attribute name="class">articleBibliography<xsl:if test="not(.//graphic)"> noPicture</xsl:if></xsl:attribute>
            <xsl:apply-templates select="." mode="bio-picture"></xsl:apply-templates>
            <xsl:apply-templates select="*"></xsl:apply-templates>
        </div>        
    </xsl:template>
</xsl:stylesheet>