<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="table-wrap">
        <div class="row table" id="{@id}">
        <a name="{@id}"/>
            
            <div class="col-md-4 col-sm-4">
                <a data-toggle="modal" data-target="#ModalTable{@id}">
                    <div class="thumbOff">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <xsl:apply-templates select="." mode="label-caption-thumb"></xsl:apply-templates>
            </div>
        </div>
    </xsl:template>
    <xsl:template match="table-wrap/table/@*">
        <xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
    </xsl:template>
    <xsl:template match="table-wrap/table">
        <div class="table table-hover">
            <xsl:element name="{name()}">
                <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
            </xsl:element>
        </div>
    </xsl:template>
    <xsl:template match="table/* | table/*/* | table/*/*/*">
        <xsl:element name="{name()}">
            <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
        </xsl:element>
    </xsl:template>
    <xsl:template match="table-wrap/caption">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="table-wrap/caption/p">
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="table-wrap/caption/title"><xsl:text> </xsl:text>
        <xsl:apply-templates select="*|text()"></xsl:apply-templates>
    </xsl:template>
    <xsl:template match="table-wrap/label">
        <strong><xsl:apply-templates></xsl:apply-templates> </strong>
    </xsl:template>
    <xsl:template match="table-wrap-foot">
        <div class="ref-list">
            <ul class="refList footnote">
                <xsl:apply-templates select="*"></xsl:apply-templates>
            </ul>
        </div>
    </xsl:template>
    <xsl:template match="table-wrap-foot/fn">
        <li>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </li>     
    </xsl:template>
    <xsl:template match="table-wrap-foot/fn/label">
        <sup class="xref big"><xsl:value-of select="."/></sup>
    </xsl:template>
    <xsl:template match="table-wrap-foot/fn/p">
        <div>
            <xsl:apply-templates select="*|text()"></xsl:apply-templates>
        </div>
    </xsl:template>
   
    
</xsl:stylesheet>