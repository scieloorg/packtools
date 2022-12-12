<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-xref.xsl"/>

    <xsl:template match="xref[@ref-type='equation' or @ref-type='disp-formula']">
        <!-- <a href="#{@rid}" class="goto"><span class="sci-ico-fileFormula"></span> <xsl:apply-templates select="*|text()"></xsl:apply-templates></a> -->
        <a href="" class="open-asset-modal" data-bs-toggle="modal" data-bs-target="#ModalScheme{translate(@rid,'.','_')}">
            <span class="sci-ico-fileFormula"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='fig']">
        <a href="" class="open-asset-modal" data-bs-toggle="modal" data-bs-target="#ModalFig{translate(@rid,'.','_')}">
            <span class="sci-ico-fileFigure"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
    
    <xsl:template match="xref[@ref-type='table']">
        <a href="" class="open-asset-modal" data-bs-toggle="modal" data-bs-target="#ModalTable{translate(@rid,'.','_')}">
            <span class="sci-ico-fileTable"></span> 
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </a>        
    </xsl:template>
</xsl:stylesheet>