<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="article" mode="text-back">
        <xsl:apply-templates select="./back" mode="text-back"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="back" mode="text-back">
        <xsl:apply-templates select="*"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="back/*">
        <div class="articleSection" data-anchor="{name()}">
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
    <xsl:template match="back//*/title">
        <div class="row">
            <div class="col-md-12 col-sm-12">
                <h1><xsl:apply-templates select="*|text()"></xsl:apply-templates></h1>
            </div>
        </div>
        <xsl:apply-templates select="p"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="back/ack">
        <div class="articleSection" data-anchor="ack">
            <xsl:if test="not(title)">
                <div class="row">
                    <div class="col-md-12 col-sm-12">
                        <h1>Acknowledgements</h1>
                    </div>
                </div>
            </xsl:if>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
</xsl:stylesheet>