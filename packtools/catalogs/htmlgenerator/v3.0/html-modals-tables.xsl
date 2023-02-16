<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-tables.xsl"/>

    <xsl:template match="table-wrap[@id] | table-wrap-group[@id]" mode="modal-header">
        <!--
        Template para criar a área do título da tabela
        -->
        <div class="modal-header">
            <h5 class="modal-title">
                <span class="material-icons-outlined">table_chart</span>
                <xsl:apply-templates select="." mode="modal-header-label-caption"/>
            </h5>
            <button class="btn-close" data-bs-dismiss="modal">
                <xsl:attribute name="aria-label">
                     <xsl:apply-templates select="." mode="interface">
                         <xsl:with-param name="text">Close</xsl:with-param>
                     </xsl:apply-templates>
                </xsl:attribute>
            </button>
            <xsl:variable name="location"><xsl:apply-templates select="." mode="original-file-location"/></xsl:variable>
            <xsl:if test="$location!=''">
                <a class="link-newWindow showTooltip" href="{$location}" target="_blank"  data-placement="left">
                <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                    <xsl:with-param name="text">Open new window</xsl:with-param>
                </xsl:apply-templates></xsl:attribute>
                <span class="sci-ico-newWindow"></span></a>
            </xsl:if>
        </div>
    </xsl:template>

</xsl:stylesheet>