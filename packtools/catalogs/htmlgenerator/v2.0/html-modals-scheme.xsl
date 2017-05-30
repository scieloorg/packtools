<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    version="1.0">
    <xsl:template match="disp-formula" mode="modal">
        <xsl:if test="@id">
            <div class="modal fade ModalFigs" id="ModalScheme{@id}" tabindex="-1" role="dialog" aria-hidden="true">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal">
                                <span aria-hidden="true">&#xd7;</span>
                                <span class="sr-only">
                                    <xsl:apply-templates select="." mode="interface">
                                        <xsl:with-param name="text">Close</xsl:with-param>
                                    </xsl:apply-templates>
                                </span>
                            </button>
                            <h4 class="modal-title"><span class="sci-ico-fileFormula"></span> <xsl:apply-templates select="." mode="label-caption"/></h4>
                        </div>
                        <div class="modal-body">
                            <xsl:choose>
                                <xsl:when test="mml:math">
                                    <xsl:apply-templates select="mml:math"></xsl:apply-templates>
                                </xsl:when>
                                <xsl:when test="tex-math">
                                    <xsl:apply-templates select="tex-math"></xsl:apply-templates>
                                </xsl:when>
                                <xsl:when test="graphic">
                                    <xsl:apply-templates select="graphic"></xsl:apply-templates>
                                </xsl:when>
                                <xsl:when test="alternatives">
                                    <xsl:apply-templates select="alternatives"/>
                                </xsl:when>
                            </xsl:choose>
                        </div>                        
                    </div>
                </div>
            </div>
        </xsl:if>
    </xsl:template>
</xsl:stylesheet>