<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="boxed-text">
        <a name="{@id}"/>
        <div style="padding: 25px;
            border: 2px solid black;
            margin: 25px;
            ">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
    <xsl:template match="boxed-text/label">
        <strong><xsl:apply-templates select="*|text()"/></strong>
    </xsl:template>
    <xsl:template match="boxed-text/caption">
        &#160;<strong><xsl:apply-templates select="*|text()"/></strong>
    </xsl:template>
</xsl:stylesheet>