<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
>

    <xsl:template match="fig-group[@id]" mode="fig-label-caption">
        <xsl:apply-templates select="fig" mode="fig-label-caption"/>
    </xsl:template>

    <xsl:template match="fig" mode="fig-label-caption">
        <xsl:apply-templates select="." mode="label-caption"/><br/>
    </xsl:template>
    
    <xsl:template match="fig | fig-group" mode="modal">
        <xsl:variable name="figid"><xsl:apply-templates select="." mode="figure-id"/></xsl:variable>    
        <div class="modal fade ModalFigs" id="ModalFig{$figid}" tabindex="-1" role="dialog" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title"><span class="sci-ico-fileFigure"></span> <xsl:apply-templates select="." mode="fig-label-caption"></xsl:apply-templates></h5>
                        <button type="button" class="close" data-dismiss="modal">
                            <span aria-hidden="true">&#xd7;</span>
                            <span class="sr-only">
                                <xsl:apply-templates select="." mode="interface">
                                    <xsl:with-param name="text">Close</xsl:with-param>
                                </xsl:apply-templates>
                            </span>
                        </button>
                        <xsl:variable name="location"><xsl:apply-templates select="." mode="original-file-location"/></xsl:variable>
                        <xsl:if test="$location!=''">
                        <a class="link-newWindow showTooltip" target="_blank" data-placement="left">
                            <xsl:attribute name="title"><xsl:apply-templates select="." mode="interface">
                                <xsl:with-param name="text">Open new window</xsl:with-param>
                            </xsl:apply-templates></xsl:attribute>
                            <xsl:attribute name="href"><xsl:value-of select="$location"/></xsl:attribute>
                            <span class="sci-ico-newWindow"></span>
                        </a>
                        </xsl:if>
                    </div>
                    <div class="modal-body">
                        <xsl:apply-templates select="." mode="fig-modal-body"/>
                    </div>
                </div>
            </div>
        </div>
    </xsl:template>
    
    <xsl:template match="*" mode="fig-modal-body">
        <!-- graphic | alternatives | disp-formula -->
        <xsl:apply-templates select="*" mode="fig-modal-body"/>
    </xsl:template>

    <xsl:template match="fig-group" mode="fig-modal-body">
        <!--
            <img/>
        -->
        <xsl:apply-templates select="fig | graphic | alternatives | disp-formula" mode="fig-modal-body"/>
    </xsl:template>

    <xsl:template match="fig" mode="fig-modal-body">
        <!--
            <img/>
        -->
        <xsl:apply-templates select="alternatives | graphic | disp-formula" mode="fig-modal-body"/>
        <xsl:apply-templates select="attrib"/>
    </xsl:template>

    <xsl:template match="disp-formula" mode="fig-modal-body">
        <xsl:apply-templates select="."/>
    </xsl:template>

    <xsl:template match="alternatives" mode="fig-modal-body">
        <xsl:choose>
            <xsl:when test="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)]">
                <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)][1]" mode="fig-modal-body"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[@xlink:href != '' and not(@content-type)][1]" mode="fig-modal-body"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="graphic" mode="fig-modal-body">
        <!--
            <img/>
        -->
        <xsl:apply-templates select="." mode="display-graphic"/>
    </xsl:template>
</xsl:stylesheet>
