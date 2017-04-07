<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="1.0">
     <xsl:template match="*" mode="modal-contribs">
        <xsl:if test=".//article-meta//contrib[*]">
            <div class="modal fade ModalDefault" id="ModalTutors" tabindex="-1" role="dialog" aria-hidden="true">
                <div class="modal-dialog">
                    <div class="modal-content">
                        <div class="modal-header">
                            <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&#xd7;</span><span class="sr-only"><xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">Close</xsl:with-param>
                            </xsl:apply-templates></span></button>
                            <h4 class="modal-title"><xsl:apply-templates select="." mode="text-labels">
                                <xsl:with-param name="text">About the authors</xsl:with-param>
                            </xsl:apply-templates></h4>
                        </div>
                        <div class="modal-body">
                            <div class="info">
                                <xsl:apply-templates select=".//article-meta//contrib" mode="modal-contrib"></xsl:apply-templates>
                                <xsl:apply-templates select=".//article-meta//author-notes" mode="modal-contrib"></xsl:apply-templates>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
        </xsl:if>    
    </xsl:template>
    
    <xsl:template match="contrib" mode="modal-contrib">
        <div class="tutors">
            <strong><xsl:apply-templates select="name"/></strong>
            <br/>
            <xsl:apply-templates select="role"/>
            <xsl:apply-templates select="xref"/>
            <xsl:apply-templates select="author-notes"/>
            <xsl:if test="contrib-id">
                <ul class="md-list inline">
                    <xsl:apply-templates select="contrib-id" mode="li"></xsl:apply-templates>
                </ul>
            </xsl:if>
            <div class="clearfix"></div>
        </div>
    </xsl:template>
    
    <xsl:template match="contrib-id" mode="li">
        <li><xsl:apply-templates select="."></xsl:apply-templates></li>
    </xsl:template>
    
    <xsl:template match="author-notes" mode="modal-contrib">
        <div class="info">
            <h3><xsl:apply-templates select="title"></xsl:apply-templates></h3>
            <xsl:apply-templates select="*[name()!='title']|text()"></xsl:apply-templates>
        </div>
    </xsl:template>

</xsl:stylesheet>