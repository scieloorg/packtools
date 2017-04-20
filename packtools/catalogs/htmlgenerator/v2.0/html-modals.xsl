<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="*" mode="article-modals">
        <xsl:apply-templates select="." mode="modal-contribs"/>
        <xsl:apply-templates select="." mode="modal-tables"/>
        <xsl:apply-templates select="." mode="modal-figs"/>
    </xsl:template>
    
    <xsl:template match="*" mode="modal-tables">
        <xsl:apply-templates select=".//table-wrap" mode="modal"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="*" mode="modal-figs">
        <xsl:apply-templates select=".//fig-group[fig] | .//*[not(fig-group)]/fig" mode="modal"></xsl:apply-templates>
    </xsl:template>
    
</xsl:stylesheet>