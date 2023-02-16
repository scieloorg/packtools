<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-figs.xsl"/>

    <xsl:template match="fig" mode="fig-label-caption">
        <xsl:apply-templates select="." mode="label-caption"/>
        <xsl:if test="position()!=last()"><br/></xsl:if>
    </xsl:template>

    <xsl:template match="fig | fig-group" mode="modal">
        <xsl:variable name="figid"><xsl:apply-templates select="." mode="figure-id"/></xsl:variable>    
        <div class="modal fade ModalFigs" id="ModalFig{$figid}" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <span class="material-icons-outlined">image</span> 
                            <xsl:apply-templates select="." mode="fig-label-caption"></xsl:apply-templates>

                            <xsl:variable name="location"><xsl:apply-templates select="." mode="original-file-location"/></xsl:variable>
                            <xsl:if test="$location!=''">
                            <a class="link-newWindow showTooltip" target="_blank" data-placement="left">
                                <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Open new window</xsl:with-param>
                                </xsl:apply-templates></xsl:attribute>
                                <xsl:attribute name="href"><xsl:value-of select="$location"/></xsl:attribute>
                                <span class="material-icons-outlined">open_in_new</span>
                            </a>
                            </xsl:if>
                        </h5>
                        <button class="btn-close" data-bs-dismiss="modal">
                            <xsl:attribute name="aria-label">
                                 <xsl:apply-templates select="." mode="interface">
                                     <xsl:with-param name="text">Close</xsl:with-param>
                                 </xsl:apply-templates>
                            </xsl:attribute>
                        </button>                 
                    </div>
                    <div class="modal-body">
                        <xsl:apply-templates select="." mode="fig-modal-body"/>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>