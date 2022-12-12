<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml">

    <xsl:include href="../v2.0/article-text-graphic.xsl"/>

    <xsl:template match="alternatives[graphic]" mode="thumbnail-div">
        <!-- 
            CRIA UM BLOCO PARA A IMAGEM NO TEXTO (IMAGEM NAO ASSOCIADO A UMA FIGURA)
            APRESENTA PREFERENCIALMENTE A MINIATURA PARA EXPANDIR OU
            NA AUSÊNCIA DA MINIATURA, APRESENTA A IMAGEM PADRÃO
        -->
        <xsl:variable name="img_id"><xsl:apply-templates select="." mode="image-id"/></xsl:variable> 
        <div class="row fig" id="{$img_id}">
            <a name="{$img_id}"></a>
            <div class="col-md-4 col-sm-4">
                <!-- manter href="" -->
                <a href="" data-bs-toggle="modal" data-bs-target="#ModalImg{$img_id}">
                    <div class="thumbImg">
                        <xsl:apply-templates select="." mode="display-thubmnail-graphic"/>
                    </div>
                </a>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="graphic" mode="thumbnail-div">
        <!-- 
            CRIA UM BLOCO PARA A IMAGEM NO TEXTO (IMAGEM NAO ASSOCIADO A UMA FIGURA)
            APRESENTA PREFERENCIALMENTE A MINIATURA PARA EXPANDIR OU
            NA AUSÊNCIA DA MINIATURA, APRESENTA A IMAGEM PADRÃO
        -->
        <xsl:variable name="img_id"><xsl:apply-templates select="." mode="image-id"/></xsl:variable> 
        <div class="row fig" id="{$img_id}">
            <a name="{$img_id}"></a>
            <div class="col-md-4 col-sm-4">
                <!-- manter href="" -->
                <a href="" data-bs-toggle="modal" data-bs-target="#ModalImg{$img_id}">
                    <div class="thumbImg">
                       <xsl:apply-templates select="." mode="display-graphic"/>
                    </div>
                </a>
            </div>
        </div>
    </xsl:template>
</xsl:stylesheet>