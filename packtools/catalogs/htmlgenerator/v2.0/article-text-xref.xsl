<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:variable name="ref" select="//ref"></xsl:variable>
    
    <xsl:template match="xref">
        <a href="#{@rid}" class="goto"><xsl:apply-templates></xsl:apply-templates></a>
    </xsl:template>
    <xsl:template match="xref[@ref-type='equation' or @ref-type='disp-formula']">
        <a href="#{@rid}" class="goto"><span class="sci-ico-fileFormula"></span> <xsl:apply-templates select="*|text()"></xsl:apply-templates></a>
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='fig']">
        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalFig{@rid}">
            <span class="sci-ico-fileFigure"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='table']">
        <a href="" class="open-asset-modal" data-toggle="modal" data-target="#ModalTable{@rid}">
            <span class="sci-ico-fileTable"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='fn']">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <span class="ref footnote">
            <sup class="xref"><xsl:apply-templates select="sup|text()"></xsl:apply-templates></sup>
            <span class="refCtt closed">
                <xsl:apply-templates select="$document//fn[@id=$id]" mode="xref"></xsl:apply-templates>
            </span>
        </span>
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='bibr']">
        <xsl:variable name="id"><xsl:value-of select="@rid"/></xsl:variable>
        <xsl:variable name="text"><xsl:value-of select="text()"/></xsl:variable>
        <xsl:variable name="elem"><xsl:choose>
            <xsl:when test="contains('1234567890',substring($text,1,1))">sup</xsl:when>
            <xsl:otherwise>strong</xsl:otherwise>
        </xsl:choose></xsl:variable>
        <span class="ref">
            <xsl:element name="{$elem}">
                <xsl:attribute name="class">xref</xsl:attribute>
                <xsl:apply-templates select="sup|text()"></xsl:apply-templates>
            </xsl:element>
            <span class="refCtt closed">
                <xsl:apply-templates select="$document//ref[@id=$id]" mode="xref"></xsl:apply-templates>
            </span>
        </span>
    </xsl:template>
    
    
</xsl:stylesheet>