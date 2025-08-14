<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:xlink="http://www.w3.org/1999/xlink"
  xmlns:mml="http://www.w3.org/1998/Math/MathML"
  exclude-result-prefixes="xlink mml">

    <xsl:template match="graphic | inline-graphic">
        <!-- APRESENTA UM ELEMENTO GRÁFICO EM TAMANHO PADRAO -->
        <xsl:apply-templates select="." mode="display-graphic"/>
    </xsl:template>

    <xsl:template match="p/alternatives[inline-graphic]">
        <!-- CRIA THUMBNAIL DE IMAGEM NAO ASSOCIADA A FIGURAS -->
        <xsl:apply-templates select="." mode="display-graphic"/>
    </xsl:template>

    <xsl:template match="p/alternatives[graphic] | p/graphic">
        <!-- CRIA THUMBNAIL DE IMAGEM NAO ASSOCIADA A FIGURAS -->
        <xsl:apply-templates select="." mode="thumbnail-div"/>
    </xsl:template>

    <xsl:template match="graphic | inline-graphic" mode="display-graphic">
        <xsl:param name="id"/>
        <xsl:param name="alt"/>
        <!-- APRESENTA O ELEMENTO GRÁFICO, NAO IMPORTA O TAMANHO -->
        <xsl:variable name="location"><xsl:apply-templates select="@xlink:href" mode="fix_extension"/></xsl:variable>
        <xsl:variable name="ext"><xsl:value-of select="substring($location,string-length($location)-3)"/></xsl:variable>
        <xsl:choose>
            <xsl:when test="$ext='.svg'">
                <object type="image/svg+xml">
                    <xsl:attribute name="style">max-width:100%</xsl:attribute>
                    <xsl:attribute name="data"><xsl:value-of select="$location"/></xsl:attribute>
                </object>
            </xsl:when>
            <xsl:otherwise>
                <img>
                    <xsl:attribute name="style">max-width:100%</xsl:attribute>
                    <xsl:attribute name="src"><xsl:value-of select="$location"/></xsl:attribute>
                    <xsl:apply-templates select="." mode="alt"/>
                </img>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="*" mode="alt">
        <xsl:choose>
            <xsl:when test=".//alt-text">
                <xsl:apply-templates select=".//graphic[alt-text]" mode="alt"/>
            </xsl:when>
            <xsl:when test=".//long-desc">
                <xsl:apply-templates select=".//graphic[long-desc]" mode="alt"/>
            </xsl:when>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="graphic" mode="alt">
        <xsl:apply-templates select=".." mode="alt"/>
    </xsl:template>

    <xsl:template match="graphic[alt-text]" mode="alt">
        <xsl:attribute name="alt">
            <xsl:apply-templates select="alt-text" mode="alt"/>
        </xsl:attribute>
    </xsl:template>

    <xsl:template match="graphic[long-desc]" mode="alt">
        <xsl:attribute name="alt">
            <xsl:apply-templates select="long-desc" mode="alt"/>
        </xsl:attribute>
    </xsl:template>

    <xsl:template match="alt-text|long-desc" mode="alt">
        <xsl:choose>
            <xsl:when test="string-length(.)&lt;=120">
                <xsl:value-of select="."/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:value-of select="substring(., 1, 120)"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="alternatives" mode="display-graphic">
        <!-- 
            APRESENTA A IMAGEM PADRÃO DENTRE AS ALTERNATIVAS
        -->
        <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)][1]" mode="display-graphic"/>
        <xsl:if test="not(*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)])">
            <xsl:apply-templates select="*[@xlink:href!='' and not(@content-type)][1]" mode="display-graphic"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="alternatives[graphic]" mode="display-thubmnail-graphic">
        <!-- 
            APRESENTA A IMAGEM MINIATURA DENTRE AS ALTERNATIVAS, SE APLICAVEL
        -->
        <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and starts-with(@content-type, 'scielo-')][1]" mode="display-graphic"/>
    </xsl:template>

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
                <a href="" data-toggle="modal" data-target="#ModalImg{$img_id}">
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
                <a href="" data-toggle="modal" data-target="#ModalImg{$img_id}">
                    <div class="thumbImg">
                       <xsl:apply-templates select="." mode="display-graphic"/>
                    </div>
                </a>
            </div>
        </div>
    </xsl:template>

    <!-- MODAL FILE LOCATION -->
    <xsl:template match="*" mode="file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM DO MODAL (TAMANHO NORMAL)
        -->
        <xsl:apply-templates select="*" mode="file-location"/>
    </xsl:template>

    <xsl:template match="alternatives" mode="file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM DO MODAL (TAMANHO NORMAL)
        -->
        <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)][1]" mode="file-location"/>
        <xsl:if test="not(*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)])">
            <xsl:apply-templates select="*[@xlink:href!='' and not(@content-type)][1]" mode="file-location"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="graphic | inline-graphic" mode="file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM DO MODAL (TAMANHO NORMAL)
        -->
        <xsl:apply-templates select="@xlink:href" mode="fix_extension"/>
    </xsl:template>

    <xsl:template match="alternatives/graphic | alternatives/inline-graphic" mode="file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM DO MODAL (TAMANHO NORMAL)
        -->
        <xsl:value-of select="@xlink:href"/>
    </xsl:template>

    <xsl:template match="table-wrap-group | fig-group" mode="original-file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM ORIGINAL (TAMANHO MAIOR)
        -->
        <xsl:apply-templates select="table-wrap | fig" mode="original-file-location"/>
    </xsl:template>

    <xsl:template match="table-wrap | fig | disp-formula" mode="original-file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM ORIGINAL (TAMANHO MAIOR)
        -->
        <xsl:apply-templates select="alternatives | graphic" mode="original-file-location"/>
    </xsl:template>

    <xsl:template match="alternatives" mode="original-file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM ORIGINAL (TAMANHO MAIOR)
        -->
        <xsl:choose>
            <xsl:when test="*[not(@content-type) and not(@specific-use) and @xlink:href!='']">
                <xsl:apply-templates select="*[not(@content-type) and not(@specific-use) and @xlink:href!='']" mode="original-file-location"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[@xlink:href!=''][1]" mode="original-file-location"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="graphic | inline-graphic" mode="original-file-location">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM ORIGINAL (TAMANHO MAIOR | TIFF)
        -->
        <xsl:value-of select="@xlink:href"/>
    </xsl:template>

    <!-- THUMBNAIL FILE LOCATION -->
    <xsl:template match="*" mode="file-location-thumb">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM MINIATURA
        -->
        <xsl:apply-templates select="*" mode="file-location-thumb"/>
    </xsl:template>

    <xsl:template match="alternatives" mode="file-location-thumb">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM MINIATURA
        -->
        <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and starts-with(@content-type, 'scielo-')][1]" mode="file-location-thumb"/>
    </xsl:template>

    <xsl:template match="graphic | inline-graphic" mode="file-location-thumb">
        <!-- 
            CAMINHO DO ARQUIVO DA IMAGEM MINIATURA, SE APLICÁVEL
        -->
        <xsl:if test="@specific-use='scielo-web' and starts-with(@content-type, 'scielo-')">
            <xsl:value-of select="@xlink:href"/>
        </xsl:if>
    </xsl:template>

    <xsl:template match="@xlink:href" mode="fix_extension">
        <!-- 
            CONSERTA A EXTENSÃO
            PARA EXTENSÃO AUSENTE OU PARA TIFF, COLOCAR JPG
            INICIALMENTE NA ADOÇÃO DO SPS, NÃO ERA EXIGIDO A EXTENSÃO, POIS ERA ASSUMIDO QUE HAVIA A JPG E TIFF
            NO ENTANTO, MANTIVEMOS A JPG NO SITE, FICANDO TIFF SÓ EM BACKUP
        -->
        <xsl:variable name="last_five_chars"><xsl:value-of select="substring(.,string-length(.)-5)"/></xsl:variable>
        <xsl:variable name="ext"><xsl:if test="contains($last_five_chars,'.')"><xsl:value-of select="substring-after($last_five_chars,'.')"/></xsl:if></xsl:variable>
        <xsl:choose>
            <xsl:when test="$ext=''"><xsl:value-of select="."/>.jpg</xsl:when>
            <xsl:when test="contains($ext, 'tif')"><xsl:value-of select="substring-before(.,$ext)"/>jpg</xsl:when>
            <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
        </xsl:choose>
    </xsl:template>

</xsl:stylesheet>
