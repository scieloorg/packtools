<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="p | sec" mode="graphic-modal">
        <!--
            MODAL PARA GRAPHIC NAO ASSOCIADO COM FIGURA
        -->
        <xsl:apply-templates select="alternatives | graphic | p" mode="graphic-modal"/>
    </xsl:template>

    <xsl:template match="alternatives" mode="graphic-modal">
        <!--
            MODAL PARA GRAPHIC NAO ASSOCIADO COM FIGURA
        -->
        <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)][1]" mode="graphic-modal">
            <xsl:with-param name="original_location"><xsl:apply-templates select="." mode="original-file-location"/></xsl:with-param>
        </xsl:apply-templates>
    </xsl:template>

    <xsl:template match="graphic" mode="graphic-modal">
        <!--
            MODAL PARA GRAPHIC NAO ASSOCIADO COM FIGURA
        -->
        <xsl:variable name="img_id">
            <xsl:apply-templates select="." mode="image-id">
                <xsl:with-param name="regular_size_img_location"><xsl:value-of select="@xlink:href"/></xsl:with-param>
            </xsl:apply-templates>
        </xsl:variable> 
        <xsl:variable name="original_location"><xsl:apply-templates select=".." mode="original-file-location"/></xsl:variable>
        <div class="modal fade ModalFigs" id="ModalImg{$img_id}" tabindex="-1" role="dialog" aria-hidden="true">
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

    <xsl:template match="graphic" mode="graphic-modal-body">
        <!-- APRESENTA GRAPHIC -->
        <xsl:apply-templates select="." mode="display-graphic"/>
    </xsl:template>

    <xsl:template match="alternatives" mode="image-id">
        <!-- OBTEM O ID DA IMAGEM PARA O MODAL, RETORNANDO SOMENTE O NOME DO ARQUIVO SEM EXTENSAO -->
        <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)][1]" mode="image-id"/>

        <xsl:if test="not(*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)])">
            <xsl:apply-templates select="*[@xlink:href!='' and not(@content-type)][1]" mode="image-idS"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="graphic" mode="image-id">
        <!-- OBTEM O ID DA IMAGEM PARA O MODAL, RETORNANDO SOMENTE O NOME DO ARQUIVO SEM EXTENSAO -->
        <xsl:param name="path" select="@xlink:href"/>
        <xsl:choose>
            <xsl:when test="contains($path, '/')">
                <xsl:apply-templates select="." mode="image-id">
                    <xsl:with-param name="path"><xsl:value-of select="substring-after($path, '/')"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:when test="contains($path, '.')">
                <xsl:apply-templates select="." mode="image-id">
                    <xsl:with-param name="path"><xsl:value-of select="substring-before($path, '.')"/></xsl:with-param>
                </xsl:apply-templates>
            </xsl:when>
            <xsl:otherwise><xsl:value-of select="$path"/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
