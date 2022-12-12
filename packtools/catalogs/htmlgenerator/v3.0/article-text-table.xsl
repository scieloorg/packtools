<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-table.xsl"/>

    <xsl:template match="table-wrap[@id] | table-wrap-group[@id]">
        <xsl:variable name="id"><xsl:apply-templates select="." mode="table-id"/></xsl:variable>
        <div class="row table" id="{$id}">
        <a name="{$id}"/>
            
            <div class="col-md-4 col-sm-4">
                <a data-bs-toggle="modal" data-bs-target="#ModalTable{$id}">
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
</xsl:stylesheet>