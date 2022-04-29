<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">

    <xsl:template match="alternatives">
        <!-- primeiro -->
        <xsl:apply-templates select="*[1]"/>
    </xsl:template>

    <xsl:template match="alternatives" mode="enlarged_image">
        <!-- 
            Apresentar a imagem ampliada (ampliada.png)

            Padrão de alternatives esperado, mas não necessariamente ocorre 100% das vezes

            <alternatives>
                <graphic xlink:href="original.tif"/>
                <graphic xlink:href="ampliada.png" specific-use="scielo-web"/>
                <graphic xlink:href="mini.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>
            </alternatives>
        -->
        <xsl:choose>
            <xsl:when test="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)]">
                <!-- imagem ampliada -->
                <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and not(@content-type)][1]" />
            </xsl:when>
            <xsl:when test="*[@xlink:href!='' and not(@specific-use) and @content-type]">
                <!-- imagem miniatura -->
                <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and @content-type][1]" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[@xlink:href!=''][1]"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="table-wrap/alternatives | table-wrap-group/alternatives">
        <!-- 
            Em caso de haver somente elementos gráficos, seleciona a imagem ampliada
            Em caso de tabela codificada e gráfico, selecionar o primeiro
        -->
        <xsl:choose>
            <xsl:when test="count(*[@xlink:href])=count(*)">
                <xsl:apply-templates select="." mode="enlarged_image"/>
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[1]"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="disp-formula/alternatives | inline-formula/alternatives">
        <xsl:choose>
            <xsl:when test="$MATH_ELEM_PREFERENCE='tex-math' and tex-math">
                <xsl:apply-templates select="tex-math" />
            </xsl:when>
            <xsl:when test="$MATH_ELEM_PREFERENCE='math' and math">
                <xsl:apply-templates select="math" />
            </xsl:when>
            <xsl:when test="$MATH_ELEM_PREFERENCE='mml:math' and mml:math">
                <xsl:apply-templates select="mml:math" />
            </xsl:when>
            <xsl:when test="tex-math">
                <xsl:apply-templates select="tex-math" />
            </xsl:when>
            <xsl:when test="mml:math">
                <xsl:apply-templates select="mml:math" />
            </xsl:when>
            <xsl:when test="math">
                <xsl:apply-templates select="math" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="." mode="enlarged_image"/>
            </xsl:otherwise>
        </xsl:choose>    
    </xsl:template>

    <xsl:template match="fig/alternatives | fig-group/alternatives">
        <!-- 
            Apresentar a imagem padrão 
        -->
        <xsl:choose>
            <xsl:when test="inline-graphic[@specific-use='scielo-web']">
                <xsl:apply-templates select="inline-graphic[@specific-use='scielo-web']" />
            </xsl:when>
            <xsl:when test="graphic[@specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-')) and @xlink:href!='']">
                <xsl:apply-templates select="graphic[@specific-use='scielo-web' and not(starts-with(@content-type, 'scielo-')) and @xlink:href!='']" />
            </xsl:when>
            <xsl:when test=".//graphic[not(@specific-use) and not(@content-type) and @xlink:href!='']">
                <xsl:apply-templates select=".//graphic[not(@specific-use) and not(@content-type) and @xlink:href!=''][1]" />
            </xsl:when>
            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='graphic'][1]"></xsl:apply-templates>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="alternatives" mode="file-location">
        <xsl:choose>

            <xsl:when test="inline-graphic[@specific-use='scielo-web']">
                <xsl:apply-templates select="inline-graphic[@specific-use='scielo-web']" mode="file-location"/>
            </xsl:when>

            <xsl:when test="graphic[@specific-use='scielo-web' and starts-with(@content-type, 'scielo-') and @xlink:href!='']">
                <xsl:apply-templates select="graphic[@specific-use='scielo-web' and starts-with(@content-type, 'scielo-') and @xlink:href!='']" mode="file-location" />
            </xsl:when>

            <xsl:when test="graphic[not(@specific-use) and not(@content-type) and @xlink:href!='']">
                <xsl:apply-templates select=".//graphic[not(@specific-use) and not(@content-type) and @xlink:href!=''][1]" mode="file-location" />
            </xsl:when>

            <xsl:otherwise>
                <xsl:apply-templates select="*[name()!='graphic' and @xlink:href!=''][1]" mode="file-location"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="alternatives" mode="file-location-thumb">
        <xsl:if test="*[@xlink:href!='' and @specific-use='scielo-web' and starts-with(@content-type, 'scielo-')]">
            <xsl:apply-templates select="*[@xlink:href!='' and @specific-use='scielo-web' and starts-with(@content-type, 'scielo-')][1]" mode="file-location-thumb"/>
        </xsl:if>
    </xsl:template>

</xsl:stylesheet>