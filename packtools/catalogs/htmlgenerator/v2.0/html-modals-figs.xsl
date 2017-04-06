<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    <xsl:template match="fig" mode="modal">
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
                        <!-- FIXME -->
                        <a class="link-newWindow showTooltip" href="../static/trash/1516-1439-mr-1516-1439321614-sch01.jpg" target="_blank" data-placement="left" title="Abrir em nova janela">
                            <span class="sci-ico-newWindow"></span>
                        </a>
                        <h4 class="modal-title"><span class="sci-ico-fileFormula"></span> <xsl:apply-templates select="label"></xsl:apply-templates></h4>
                        
                    </div>
                    <div class="modal-body">
                        <xsl:apply-templates select="graphic"></xsl:apply-templates>
                    </div>
                    <div class="modal-footer">
                        <xsl:apply-templates select="caption"></xsl:apply-templates>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    
</xsl:stylesheet>
