<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <!-- APRESENTA CAIXA DE TEXTO DESTACANDO O RELACIONAMENTO ENTRE DOCUMENTOS -->

    <xsl:template match="article" mode="article-meta-related-article">
        <!-- seleciona dados de article ou sub-article -->
        <xsl:if test=".//related-article[@related-article-type!='preprint']">
            <!-- preprint não deve tanto destaque quanto os demais tipos -->
            <!-- caixa amarela -->
            <div class="panel article-correction-title">
                <xsl:choose>
                    <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//related-article">
                        <!-- sub-article -->
                        <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//related-article[@related-article-type!='preprint']" mode="article-meta-related-article-box-item"/>
                    </xsl:when>
                    <xsl:otherwise>
                        <!-- article -->
                        <xsl:apply-templates select=".//article-meta//related-article[@related-article-type!='preprint']" mode="article-meta-related-article-box-item"/>
                        <xsl:apply-templates select="body//related-article[@related-article-type!='preprint']" mode="article-meta-related-article-box-item"/>
                    </xsl:otherwise>
                </xsl:choose>
            </div>            
        </xsl:if>
    </xsl:template>

    <xsl:template match="related-article" mode="article-meta-related-article-box-item">
        <xsl:apply-templates select="." mode="article-meta-related-article-message"/>
        <div class="panel-body">
            <ul>
                <xsl:apply-templates select="." mode="article-meta-related-article-item"/>
            </ul>
        </div>
    </xsl:template>
            
    <xsl:template match="@related-article-type" mode="article-meta-related-article-message">
        <!-- MESSAGE -->
        <!-- 
            OBS.: geralmente somente um dos documentos possui related-article.
            O artigo mencionando geralmente não possui related-article. Mas
            foi sugerido que passe a ser inserido para que o XML seja autossuficiente. Atualmente o link da volta é feito via aplicação
            do site.
        -->
        <xsl:choose>
            <xsl:when test="$article/@article-type='addendum'">This addendum adds information to the following document</xsl:when>
            <xsl:when test=".='corrected-article'">This erratum corrects</xsl:when>
            <xsl:when test=".='retracted-article'">This retraction retracts</xsl:when>
            <xsl:when test=".='commentary-article'">This document comments</xsl:when>
            <xsl:when test=".='addendum'">This document has an addendum</xsl:when>
            <xsl:when test=".='retraction'">This document was retracted by</xsl:when>
            <xsl:when test=".='correction'">This document has corrections</xsl:when>
            <xsl:when test=".='preprint'">This document has a preprint version</xsl:when>
            <xsl:when test=".='peer-reviewed-material'">This recommendation refers to the article</xsl:when>
            <xsl:otherwise>This document is related to</xsl:otherwise>
        </xsl:choose>
    </xsl:template>

    <xsl:template match="related-article" mode="article-meta-related-article-message">
        <xsl:variable name="message">
            <xsl:apply-templates select="@related-article-type" mode="article-meta-related-article-message"/>
        </xsl:variable>

        <div class="panel-heading">
            <xsl:apply-templates select="." mode="text-labels">
                <xsl:with-param name="text"><xsl:value-of select="$message"/></xsl:with-param>
            </xsl:apply-templates>:
        </div>
    </xsl:template>

    <xsl:template match="related-article" mode="article-meta-related-article-item">
        <li>
            <xsl:apply-templates select="." mode="article-meta-related-article-link"/>
        </li>
    </xsl:template>
    
    <xsl:template match="related-article" mode="article-meta-related-article-link">
        <!-- 
        <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/0102-311X00064615"></related-article>
        <related-article id="RA1" page="142" related-article-type="corrected-article" vol="39">
            <bold>2016;39(3):142–8</bold>
        </related-article>
        -->
        <xsl:variable name="text"><xsl:apply-templates select="*|text()"/></xsl:variable>
        <a target="_blank">
            <xsl:attribute name="href"><xsl:apply-templates select="." mode="article-meta-related-article-href"/></xsl:attribute>
            <xsl:choose>
                <xsl:when test="normalize-space($text)='' and @xlink:href">
                    <xsl:value-of select="@xlink:href"/>
                </xsl:when>
                <xsl:when test="normalize-space($text)=''">
                    <xsl:if test="@vol">
                        <xsl:apply-templates select="@vol"></xsl:apply-templates>
                    </xsl:if>
                    <xsl:if test="@issue">
                        (<xsl:apply-templates select="@issue"></xsl:apply-templates>)
                    </xsl:if>
                    <xsl:if test="(@vol or @issue) and (@page or @elocation-id)">: </xsl:if>
                    
                    <xsl:if test="@page">
                        <xsl:apply-templates select="@page"></xsl:apply-templates>
                    </xsl:if>
                    <xsl:if test="@page and @elocation-id">, </xsl:if>
                    <xsl:if test="@elocation-id">
                        <xsl:apply-templates select="@elocation-id"></xsl:apply-templates>
                    </xsl:if>
                </xsl:when>
                <xsl:otherwise>
                    <xsl:apply-templates select="*|text()"></xsl:apply-templates>
                </xsl:otherwise>
            </xsl:choose>            
        </a>
    </xsl:template>
    
    <xsl:template match="related-article[@ext-link-type='doi']" mode="article-meta-related-article-href">https://doi.org/<xsl:value-of select="@xlink:href"/></xsl:template>
    <xsl:template match="related-article[@ext-link-type='scielo-pid']" mode="article-meta-related-article-link">/article/<xsl:value-of select="@xlink:href"/></xsl:template>
    <xsl:template match="related-article[@ext-link-type='scielo-aid']" mode="article-meta-related-article-link">/article/<xsl:value-of select="@xlink:href"/></xsl:template>

    <xsl:template match="body//related-article">
        <xsl:apply-templates select="." mode="article-meta-related-article-link"/>
    </xsl:template>

    <xsl:template match="related-article[@related-article-type='preprint']" mode="hidden-box">
        <!-- para evitar que a caixa seja inserida via javascript -->
        <div class="panel article-correction-title" style="visibility: hidden"></div>
    </xsl:template>
</xsl:stylesheet>