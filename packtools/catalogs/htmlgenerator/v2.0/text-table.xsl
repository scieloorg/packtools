<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="table-wrap">
        <div class="row table" id="{@id}">
        <a name="{@id}"/>
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="table-wrap//*">
        <xsl:element name="{name()}">
            <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
        </xsl:element>
    </xsl:template>
    <xsl:template match="table-wrap/caption">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="table-wrap/caption/p">
        <div>
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="table-wrap/caption/title"><xsl:text> </xsl:text>
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="table-wrap/label">
        <strong><xsl:apply-templates></xsl:apply-templates> </strong>
    </xsl:template>
    <xsl:template match="table-wrap/table-wrap-foot">
        <div class="footnotes">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    
</xsl:stylesheet>