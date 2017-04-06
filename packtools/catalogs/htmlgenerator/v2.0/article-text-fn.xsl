<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="fn" mode="xref">
        <xsl:apply-templates select="*|text()" mode="xref"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fn/label" mode="xref">
        <strong class="fn-title"><xsl:apply-templates select="*|text()" mode="xref"/></strong>
    </xsl:template>
    
    <xsl:template match="fn/p" mode="xref">
        <xsl:apply-templates select="*|text()" mode="xref"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fn">
        <xsl:param name="position"></xsl:param>
        
        <a name="{@id}"/>
        <div id="{@id}" class="footnote">
            <xsl:apply-templates select="*|text()">
                <xsl:with-param name="position" select="position()"></xsl:with-param>
            </xsl:apply-templates>
        </div>
    </xsl:template>
   
    
</xsl:stylesheet>