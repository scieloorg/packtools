<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="fig-group" mode="label-caption">
        <xsl:apply-templates select="fig[@xml:lang=$TEXT_LANG]" mode="label-caption"></xsl:apply-templates>
    </xsl:template>
    
    <xsl:template match="fig[@id] | fig-group[@id]" mode="modal">
        <div class="modal fade ModalFigs" id="ModalFig{@id}" tabindex="-1" role="dialog" aria-hidden="true">
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
                        <!-- FIXME -->
                        <xsl:if test="graphic">
                        <a class="link-newWindow showTooltip" target="_blank" data-placement="left">
                            <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">Open new window</xsl:with-param>
                            </xsl:apply-templates></xsl:attribute>
                            <xsl:attribute name="href"><xsl:apply-templates select="." mode="file-location"/></xsl:attribute>
                            <span class="sci-ico-newWindow"></span>
                        </a>
                        </xsl:if>
                        <h4 class="modal-title"><span class="sci-ico-fileFigure"></span> <xsl:apply-templates select="." mode="label-caption"></xsl:apply-templates></h4>                 
                    </div>
                    <div class="modal-body">
                        <xsl:apply-templates select="graphic"/>
                        <xsl:apply-templates select="disp-formula"></xsl:apply-templates>
                        <xsl:apply-templates select="attrib"></xsl:apply-templates>
                    </div>
                    <div class="modal-footer">
                        <!-- 
                        <h4 class="modal-title"><span class="sci-ico-fileFigure"></span> <xsl:apply-templates select="." mode="label-caption"></xsl:apply-templates></h4>
                        -->                        
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    
</xsl:stylesheet>
