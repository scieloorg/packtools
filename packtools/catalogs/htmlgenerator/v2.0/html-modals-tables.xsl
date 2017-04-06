<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
    
    <xsl:template match="table-wrap" mode="modal">
        <div class="modal fade ModalTables" id="ModalTable{@id}" tabindex="-1" role="dialog" aria-hidden="true">
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
                        <a class="link-newWindow showTooltip" href="article-table2.html" target="_blank"  data-placement="left">
                            <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">Open new window</xsl:with-param>
                            </xsl:apply-templates></xsl:attribute>
                            <span class="sci-ico-newWindow"></span></a>
                        <h4 class="modal-title"><span class="sci-ico-fileTable"></span> <xsl:apply-templates select="label"/></h4>
                    </div>
                    <div class="modal-body">
                        <xsl:choose>
                            <xsl:when test="table">
                                <xsl:copy-of select="table"/>
                            </xsl:when>
                            <xsl:when test="graphic">
                                <xsl:apply-templates select="graphic"></xsl:apply-templates>
                            </xsl:when>
                            <xsl:when test="alternatives">
                                <!-- FIXME -->
                                <xsl:copy-of select="alternatives/table"/>
                            </xsl:when>
                        </xsl:choose>
                    </div>
                </div>
            </div>
        </div>          
    </xsl:template>
    
    
</xsl:stylesheet>