<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:mml="http://www.w3.org/1998/Math/MathML"
    >
    <!-- APRESENTA CAIXA DE TEXTO DESTACANDO O RELACIONAMENTO ENTRE DOCUMENTOS -->

    <xsl:template match="article" mode="article-meta-related-article">
        <!-- seleciona dados de article ou sub-article -->
        <xsl:choose>
            <xsl:when test=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']//related-article">
                <!-- sub-article -->
                <xsl:apply-templates select=".//sub-article[@xml:lang=$TEXT_LANG and @article-type='translation']" mode="article-meta-related-article-box"/>
            </xsl:when>
            <xsl:otherwise>
                <!-- article -->
                <xsl:apply-templates select="." mode="article-meta-related-article-box"/>
            </xsl:otherwise>
        </xsl:choose>
    </xsl:template>

     <xsl:template match="article | sub-article" mode="article-meta-related-article-box">
        <!-- APRESENTA CAIXA DE TEXTO DESTACANDO O RELACIONAMENTO ENTRE DOCUMENTOS -->
        <xsl:variable name="message">
            <xsl:apply-templates select="@article-type" mode="article-meta-related-article-message"/>
        </xsl:variable>
        <div class="panel article-correction-title">
            <div class="panel-heading">
                <xsl:apply-templates select="." mode="text-labels">
                    <xsl:with-param name="text"><xsl:value-of select="$message"/></xsl:with-param>
                </xsl:apply-templates>:
            </div>

            <div class="panel-body">
                <ul>
                   <xsl:apply-templates select=".//related-article" mode="article-meta-related-article-item"/>
                </ul>
            </div>
        </div>
    </xsl:template>

    <xsl:template match="@article-type" mode="article-meta-related-article-message">
        <!-- MESSAGE -->
        <xsl:choose>
            <xsl:when test="contains(.,'retraction')">This retraction retracts</xsl:when>
            <xsl:when test="contains(.,'corrected-article')">This erratum corrects</xsl:when>
            <xsl:when test="contains(.,'commentary')">This document comments</xsl:when>
            <xsl:when test="contains(.,'addendum')">This document is an addendum of</xsl:when>
            <xsl:when test=".//related-article[@related-article-type='preprint']">This article has preprint version</xsl:when>
            <xsl:when test=".//related-article[@related-article-type='peer-reviewed-material']">Peer reviewed article</xsl:when>
            <xsl:otherwise>Related to</xsl:otherwise>
        </xsl:choose>
    </xsl:template>
    
    <xsl:template match="related-article" mode="article-meta-related-article-li">
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
        <xsl:choose>
            <xsl:when test="@xlink:href">
                <xsl:apply-templates select="@xlink:href"></xsl:apply-templates>
            </xsl:when>
            <xsl:when test="normalize-space(.//text())=''">
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
    </xsl:template>
    
    <xsl:template match="related-article[@ext-link-type='doi']/@xlink:href">
        <a href="https://doi.org/{.}" target="_blank">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>
    <xsl:template match="related-article[@ext-link-type='scielo-pid']/@xlink:href">
        <a href="/article/{.}" target="_blank">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>
    <xsl:template match="related-article[@ext-link-type='scielo-aid']/@xlink:href">
        <a href="/article/{.}" target="_blank">
            <xsl:value-of select="."/>
        </a>
    </xsl:template>

    <xsl:template match="body//related-article">
        <xsl:apply-templates select="." mode="article-meta-related-article-link"/>
    </xsl:template>

</xsl:stylesheet>