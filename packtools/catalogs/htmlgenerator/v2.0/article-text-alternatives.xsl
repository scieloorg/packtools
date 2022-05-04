<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    exclude-result-prefixes="xlink mml"
    version="1.0">

    <xsl:template match="table-wrap/alternatives | table-wrap-group/alternatives">
        <!-- 
            Em caso de haver somente elementos gráficos, seleciona a imagem ampliada
            Em caso de tabela codificada e gráfico, selecionar o primeiro
        -->
        <xsl:choose>
            <xsl:when test="count(*[@xlink:href])=count(*)">
                <xsl:apply-templates select="." mode="display-graphic"/>
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
            <xsl:when test="tex-math and (math or mml:math)">
                <!-- obtém o primeiro -->
                <xsl:apply-templates select="*[1]" />
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
                <xsl:apply-templates select="." mode="display-graphic"/>
            </xsl:otherwise>
        </xsl:choose>    
    </xsl:template>

</xsl:stylesheet>