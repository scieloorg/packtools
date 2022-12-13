<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-graphics.xsl"/>

    <xsl:template match="graphic" mode="graphic-modal">
        <xsl:param name="original_location"/>
        <!--
            MODAL PARA GRAPHIC NAO ASSOCIADO COM FIGURA
        -->
        <xsl:variable name="img_id"><xsl:apply-templates select="." mode="image-id"/></xsl:variable> 
        <div class="modal fade ModalFigs" id="ModalImg{$img_id}" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <button class="btn-close" data-bs-dismiss="modal">
                            <xsl:attribute name="aria-label">
                                 <xsl:apply-templates select="." mode="interface">
                                     <xsl:with-param name="text">Close</xsl:with-param>
                                 </xsl:apply-templates>
                            </xsl:attribute>
                        </button>
                        <a class="link-newWindow showTooltip" target="_blank" data-placement="left">
                            <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">Open new window</xsl:with-param>
                            </xsl:apply-templates></xsl:attribute>
                            <xsl:attribute name="href"><xsl:value-of select="$original_location"/><xsl:if test="$original_location=''"><xsl:apply-templates select="@xlink:href" mode="fix_extension"/></xsl:if></xsl:attribute>
                            <span class="sci-ico-newWindow"></span>
                        </a>          
                    </div>
                    <div class="modal-body">
                        <xsl:apply-templates select="." mode="graphic-modal-body"/>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>