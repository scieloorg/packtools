<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/html-modals-contribs.xsl"/>

    <xsl:template match="article-meta | front | front-stub" mode="modal-contrib">
        <xsl:if test="contrib-group/contrib or contrib-group/author-notes">
            <xsl:variable name="id"><xsl:apply-templates select="." mode="modal-id"></xsl:apply-templates></xsl:variable>
            <div class="modal fade ModalDefault ModalTutors" id="ModalTutors{$id}" tabindex="-1" role="dialog" aria-hidden="true">            
                
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                             <xsl:apply-templates select="." mode="interface">
                                 <xsl:with-param name="text">About the author<xsl:if test="count(contrib-group/contrib[@contrib-type='author'])&gt;1">s</xsl:if></xsl:with-param>
                             </xsl:apply-templates>
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
                        <div class="info">
                            <xsl:apply-templates select="contrib-group/contrib" mode="modal-contrib"></xsl:apply-templates>
                            <xsl:if test="not(contrib-group/contrib) and ../@article-type='translation'">
                                <xsl:apply-templates select="$article//article-meta/front/contrib-group/contrib" mode="modal-contrib"></xsl:apply-templates>
                            </xsl:if>
                        </div>
                        <xsl:apply-templates select=".//author-notes" mode="modal-contrib"></xsl:apply-templates>
                    </div>
                </div>
            </div>
            </div>
        </xsl:if>    
    </xsl:template>
</xsl:stylesheet>