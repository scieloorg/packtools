<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="table-wrap[@id] | table-wrap-group[@id]">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="table-id"/></xsl:variable>
        <div class="row table" id="{$id}">
        <a name="{$id}"/>
            
            <div class="col-md-4 col-sm-4">
                <a data-toggle="modal" data-target="#ModalTable{$id}">
                    <div class="thumbOff">
                        Thumbnail
                        <div class="zoom"><span class="sci-ico-zoom"></span></div>
                    </div>
                </a>
            </div>
            <div class="col-md-8 col-sm-8">
                <!-- apresenta a legenda -->
                <xsl:apply-templates select="." mode="table-label-caption-thumb"/>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="table-wrap-group[@id]" mode="table-label-caption-thumb">
        <!-- apresenta as legendas -->
        <xsl:apply-templates select="table-wrap" mode="table-label-caption-thumb"/>
    </xsl:template>

    <xsl:template match="table-wrap" mode="table-label-caption-thumb">
        <!-- apresenta a legenda -->
        <xsl:apply-templates select="." mode="label-caption-thumb"/><br/>
    </xsl:template>

    <xsl:template match="table-wrap/table/@*">
        <xsl:attribute name="{name()}"><xsl:value-of select="."/></xsl:attribute>
    </xsl:template>
    <xsl:template match="table-wrap/table | table-wrap/alternatives/table">
        <div class="table table-hover">
            <xsl:element name="{name()}">
                <xsl:apply-templates select="@*|*|text()"></xsl:apply-templates>
            </xsl:element>
        </div>
    </xsl:template>

    <xsl:template match="tr | td | th | col | colgroup | thead | tfoot | tbody">
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