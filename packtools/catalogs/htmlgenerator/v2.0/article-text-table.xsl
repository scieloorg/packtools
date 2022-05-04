<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  exclude-result-prefixes="xlink">

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
        <xsl:apply-templates select="." mode="label-br-caption"/><br/>
    </xsl:template>

    <xsl:template match="table">
        <!--
            table-wrap-group/table-wrap/table 
            table-wrap-group/table 
            table-wrap/table
        -->
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

    <xsl:template match="table-wrap/alternatives | table-wrap-group/alternatives">
        <!-- 
            Em caso de haver somente elementos gráficos, seleciona a imagem ampliada
            Em caso de tabela codificada e gráfico, selecionar o primeiro
        -->
        <xsl:choose>
            <xsl:when test="count(*[@xlink:href])=count(*)">
                <xsl:apply-templates select="." mode="display-graphic"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[1]"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>